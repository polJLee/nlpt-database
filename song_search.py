import sys
import psycopg2

### Song Search ###

# define any local helper functions here

# set up some globals

usage = "Usage: song_search.py 'Song_Search'"
db = None

# process command-line args

argc = len(sys.argv)

# manipulate database

try:
	db = psycopg2.connect("dbname=nlpt22")
	cur = db.cursor()
	if argc == 1:
		print("No title included")
	else:
		insert = sys.argv[1:]
		instring = ''
		for i in insert:
			instring += i + ' '


		if "'" in instring:
			instring = instring.replace("'", "''")
		instring = instring.strip()
		qry = f"""
		SELECT Sundays.date 
		FROM Sundays, Songs, Sunday_songs 
		WHERE UPPER(Songs.title) LIKE UPPER('{instring}') 
		AND Songs.id = Sunday_songs.songid 
		AND Sundays.id = Sunday_songs.sundayid
		ORDER BY Sundays.date ASC
		"""

		cur.execute(qry)
		sundayinfo = cur.fetchall()

		qry = f"""
		SELECT Artists.name 
		FROM Artists, Songs 
		WHERE UPPER(Songs.title) LIKE UPPER('{instring}')
		AND Songs.artistid = Artists.id"""

		cur.execute(qry)
		artistinfo = cur.fetchall()

		if not sundayinfo:
			instring
			print(f"\nNo songs matching | {instring}|")
			print("===============")
		else:
			if len(artistinfo) == 1:
				print(f"\n{instring} by {artistinfo[0][0]}\n")
				print(f"=== This song was picked {len(sundayinfo)} times")
				print("=== Below are the Sundays that the song was picked")
				for i in sundayinfo:
					print(f"    • {i[0]}")
				print('')
			else:
				print(f"This song is covered by multiple artists")

				for i in artistinfo:
					print(f"	{instring} by {i[0].strip()}")
					qry = f"""
					SELECT Sundays.date 
					FROM Sundays, Sunday_songs, Artists, Songs
					WHERE Songs.title = '{instring}'
					AND Artists.name = '{i[0].strip()}'
					AND Sunday_songs.songid = songs.id
					AND Sundays.id = Sunday_songs.sundayid
					AND Songs.artistid = Artists.id
					"""
					cur.execute(qry)
					sundayinfo = cur.fetchall()
					for i in sundayinfo:
						print(f"	• {i[0]}")
					print('')

			


except psycopg2.Error as err:
	print("DB error: ", err)
finally:
	if db:
		db.close()