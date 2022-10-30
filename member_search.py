import sys

import psycopg2
import operator

### Member Search ###

# define any local helper functions here
def update_dict(info):
    for item in info:
        dict[item[0].strip()] += int(item[1])



# set up some globals

usage = "Usage: member_search.py 'Member_Search'"
db = None

# process command-line args

argc = len(sys.argv)

# manipulate database

try:
	db = psycopg2.connect("dbname=nlpt22")
	cur = db.cursor()
	if argc == 1:
		print("No Member included")
	else:
		insert = sys.argv[1:]
		instring = ''
		for i in insert:
			instring += i + ' '
		instring = instring.strip()
		qry = f"""
		SELECT role
		FROM Members
		WHERE name = '{instring}'
		"""
		cur.execute(qry)
		role = cur.fetchone()
		if role is None:
			print(f"{instring} is not a member of the Praise Team")
			exit()
		
		role = role[0].strip()

		countqry = ""
		sleaderqry = ""
		instqry = ""
		vqry = ""
		r = ""

		if "Vocal" in role:
			if "Guitar" in role:
				countqry = f"""
				SELECT count(*)
				FROM Roster
				WHERE Song_leader1 = '{instring}'
				OR Song_leader2 = '{instring}'
				OR Vocal = '{instring}'
				OR Guitar_1 = '{instring}'
				OR Guitar_2 = '{instring}'
				"""
				sleaderqry = f"""
				SELECT count(*)
				FROM Roster
				WHERE Song_leader1 = '{instring}'
				OR Song_leader2 = '{instring}'
				"""

				vqry = f"""
				SELECT count(*)
				FROM Roster
				WHERE Vocal = '{instring}'
				"""
				r = "VG"
			elif "Keys" in role:
				countqry = f"""
				SELECT count(*)
				FROM Roster
				WHERE Song_leader1 = '{instring}'
				OR Song_leader2 = '{instring}'
				OR Vocal = '{instring}'
				OR Keys = '{instring}'
				OR Pads = '{instring}'
				"""
				sleaderqry = f"""
				SELECT count(*)
				FROM Roster
				WHERE Song_leader1 = '{instring}'
				OR Song_leader2 = '{instring}'
				"""
				vqry = f"""
				SELECT count(*)
				FROM Roster
				WHERE Vocal = '{instring}'
				"""

				instqry = f"""
				SELECT count(*)
				FROM Roster
				WHERE Keys = '{instring}'
				AND Song_leader1 != '{instring}'
				AND Song_leader2 != '{instring}'
				AND Vocal is NULL
				"""
				r = "VK"

			else:
				countqry = f"""
				SELECT count(*)
				FROM Roster
				WHERE Song_leader1 = '{instring}'
				OR Song_leader2 = '{instring}'
				OR Vocal = '{instring}'
				"""
				sleaderqry = f"""
				SELECT count(*)
				FROM Roster
				WHERE Song_leader1 = '{instring}'
				OR Song_leader2 = '{instring}'
				"""
				vqry = f"""
				SELECT count(*)
				FROM Roster
				WHERE Vocal = '{instring}'
				"""
				r = "V"

		elif "Keys" in role and "Vocal" not in role:
			countqry = f"""
			SELECT count(*)
			FROM Roster
			WHERE keys = '{instring}'
			OR pads = '{instring}'
			"""
			r = "K"
		else:
			countqry = f"""
			SELECT count(*)
			FROM Roster
			WHERE Drum = '{instring}'
			"""
			r = "D"

		cur.execute(countqry)
		total = cur.fetchone()
		total = total[0]
		total_s = ""
		total_v = ""
		total_i = ""

		if vqry != "":
			cur.execute(vqry)
			total_v = cur.fetchone()
			total_v = total_v[0]
		if sleaderqry != "":
			cur.execute(sleaderqry)
			total_s = cur.fetchone()
			total_s = total_s[0]
		if instqry != "":
			cur.execute(instqry)
			total_i = cur.fetchone()
			total_i = total_i[0]
   
   
   
		print(f"\nMember Name: {instring}")
		print(f"Role: {role}")
		if total_s == "" and total_v == "":
			print(f"In 2022, {instring} stood {total} times")
		else:
			print(f"In 2022, {instring} stood {total} times")
			if total_i == "":
				print(f"{total_s} times as a Song Leader and {total_v} times as a Vocal")
			else:
				print(f"{total_s} times as a Song Leader and {total_v} times as a Vocal and {total_i} times as an Instrumentalist")
    
		cur.execute("SELECT name FROM Members")
		members = cur.fetchall()
		
		dict = {}
		for item in members:
			dict[item[0].strip()] = 0
		dict.pop(instring)
		
		if r == "VG":
			qry = f"""
   			SELECT Song_leader2, COUNT(Song_leader2) 
   			FROM Roster 
      		WHERE Song_leader1 = '{instring}'
        	GROUP BY Song_leader2
         	ORDER BY COUNT(Song_leader2) DESC
          	"""
			cur.execute(qry)
			update_dict(cur.fetchall())
			qry = f"""
   			SELECT Vocal, COUNT(Vocal)
			FROM Roster
			WHERE Song_leader1 = '{instring}'
			AND Vocal != ''
			GROUP BY Vocal
			ORDER BY COUNT(Vocal) DESC
      		"""
			cur.execute(qry)
			update_dict(cur.fetchall())
			qry = f"""
   			SELECT Song_leader1, COUNT(Song_leader1)
			FROM Roster
			WHERE Song_leader2 = '{instring}'
			GROUP BY Song_leader1
			ORDER BY COUNT(Song_leader1) DESC
      		"""
			cur.execute(qry)
			update_dict(cur.fetchall())

			qry = f"""
			SELECT Vocal, COUNT(Vocal)
			FROM Roster
			WHERE Song_leader2 = '{instring}'
			AND Vocal != ''
			GROUP BY Vocal
			ORDER BY COUNT(Vocal) DESC
      		"""
			cur.execute(qry)
			update_dict(cur.fetchall())
			
			qry = f"""
   			SELECT Song_leader1, COUNT(Song_leader1)
			FROM Roster
			WHERE Vocal = '{instring}'
			GROUP BY Song_leader1
			ORDER BY COUNT(Song_leader1) DESC
      		"""
			cur.execute(qry)
			update_dict(cur.fetchall())

			qry = f"""
   			SELECT Song_leader2, COUNT(Song_leader2)
			FROM Roster
			WHERE Vocal = '{instring}'
			GROUP BY Song_leader2
			ORDER BY COUNT(Song_leader2) DESC
      		"""
			cur.execute(qry)
			update_dict(cur.fetchall())
			max_voc_name = max(dict.items(), key=operator.itemgetter(1))[0]
			max_voc_val = dict[max_voc_name]
			dict = dict.fromkeys(dict,0)
			
			qry = f"""
   			SELECT keys, COUNT(keys)
			FROM Roster
			WHERE Song_leader1 = '{instring}'
			OR Song_leader2 = '{instring}'
			OR Vocal = '{instring}'
			GROUP BY Keys
			ORDER BY COUNT(Keys) DESC
      		"""
			cur.execute(qry)
			info = cur.fetchone()
			max_keys_name = info[0].strip()
			max_keys_val = info[1]
			print(f"Below are the name and the frequency of members that {instring} has stood with")
			print(f"Vocal | {max_voc_name} : {max_voc_val}")
			print(f"Keys | {max_keys_name} : {max_keys_val}")
		elif r == 'VK':
			qry = f"""
   			SELECT Song_leader2, COUNT(Song_leader2) 
   			FROM Roster 
      		WHERE Song_leader1 = '{instring}'
        	GROUP BY Song_leader2
         	ORDER BY COUNT(Song_leader2) DESC
          	"""
			cur.execute(qry)
			update_dict(cur.fetchall())
			qry = f"""
   			SELECT Vocal, COUNT(Vocal)
			FROM Roster
			WHERE Song_leader1 = '{instring}'
			AND Vocal != ''
			GROUP BY Vocal
			ORDER BY COUNT(Vocal) DESC
      		"""
			cur.execute(qry)
			update_dict(cur.fetchall())
			qry = f"""
   			SELECT Song_leader1, COUNT(Song_leader1)
			FROM Roster
			WHERE Song_leader2 = '{instring}'
			GROUP BY Song_leader1
			ORDER BY COUNT(Song_leader1) DESC
      		"""
			cur.execute(qry)
			update_dict(cur.fetchall())

			qry = f"""
			SELECT Vocal, COUNT(Vocal)
			FROM Roster
			WHERE Song_leader2 = '{instring}'
			AND Vocal != ''
			GROUP BY Vocal
			ORDER BY COUNT(Vocal) DESC
      		"""
			cur.execute(qry)
			update_dict(cur.fetchall())
			
			qry = f"""
   			SELECT Song_leader1, COUNT(Song_leader1)
			FROM Roster
			WHERE Vocal = '{instring}'
			GROUP BY Song_leader1
			ORDER BY COUNT(Song_leader1) DESC
      		"""
			cur.execute(qry)
			update_dict(cur.fetchall())

			qry = f"""
   			SELECT Song_leader2, COUNT(Song_leader2)
			FROM Roster
			WHERE Vocal = '{instring}'
			GROUP BY Song_leader2
			ORDER BY COUNT(Song_leader2) DESC
      		"""
			cur.execute(qry)
			update_dict(cur.fetchall())
			max_voc_name = max(dict.items(), key=operator.itemgetter(1))[0]
			max_voc_val = dict[max_voc_name]
			dict = dict.fromkeys(dict,0)
   
			qry = f"""
   			SELECT Guitar_1, COUNT(Guitar_1)
			FROM Roster
			WHERE Song_leader1 = '{instring}'
			OR Song_leader2 = '{instring}'
			OR Vocal = '{instring}'
			GROUP BY Guitar_1
			ORDER BY COUNT(Guitar_1) DESC
      		"""
			cur.execute(qry)
			update_dict(cur.fetchall())

			qry = f"""
			SELECT Guitar_2, COUNT(Guitar_2)
			FROM Roster
			WHERE (Song_leader1 = '{instring}'
			OR Song_leader2 = '{instring}'
			OR Vocal = '{instring}')
			AND Guitar_2 != ''
			GROUP BY Guitar_2
			ORDER BY COUNT(Guitar_2) DESC
      		"""
			cur.execute(qry)
			update_dict(cur.fetchall())
			max_guitar_name = max(dict.items(), key=operator.itemgetter(1))[0]
			max_guitar_val = dict[max_guitar_name]
			print(f"Below are the name and the frequency of members that {instring} has stood with")
			print(f"Vocal | {max_voc_name} : {max_voc_val}")
			print(f"Guitar | {max_guitar_name} : {max_guitar_val}")
		elif r == 'V':
      
			qry = f"""
   			SELECT Song_leader2, COUNT(Song_leader2) 
   			FROM Roster 
      		WHERE Song_leader1 = '{instring}'
        	GROUP BY Song_leader2
         	ORDER BY COUNT(Song_leader2) DESC
          	"""
			cur.execute(qry)
			update_dict(cur.fetchall())
			qry = f"""
   			SELECT Vocal, COUNT(Vocal)
			FROM Roster
			WHERE Song_leader1 = '{instring}'
			AND Vocal != ''
			GROUP BY Vocal
			ORDER BY COUNT(Vocal) DESC
      		"""
			cur.execute(qry)
			update_dict(cur.fetchall())
			qry = f"""
   			SELECT Song_leader1, COUNT(Song_leader1)
			FROM Roster
			WHERE Song_leader2 = '{instring}'
			GROUP BY Song_leader1
			ORDER BY COUNT(Song_leader1) DESC
      		"""
			cur.execute(qry)
			update_dict(cur.fetchall())

			qry = f"""
			SELECT Vocal, COUNT(Vocal)
			FROM Roster
			WHERE Song_leader2 = '{instring}'
			AND Vocal != ''
			GROUP BY Vocal
			ORDER BY COUNT(Vocal) DESC
      		"""
			cur.execute(qry)
			update_dict(cur.fetchall())
			
			qry = f"""
   			SELECT Song_leader1, COUNT(Song_leader1)
			FROM Roster
			WHERE Vocal = '{instring}'
			GROUP BY Song_leader1
			ORDER BY COUNT(Song_leader1) DESC
      		"""
			cur.execute(qry)
			update_dict(cur.fetchall())

			qry = f"""
   			SELECT Song_leader2, COUNT(Song_leader2)
			FROM Roster
			WHERE Vocal = '{instring}'
			GROUP BY Song_leader2
			ORDER BY COUNT(Song_leader2) DESC
      		"""
			cur.execute(qry)
			update_dict(cur.fetchall())
			max_voc_name = max(dict.items(), key=operator.itemgetter(1))[0]
			max_voc_val = dict[max_voc_name]
			dict = dict.fromkeys(dict,0)
			qry = f"""
   			SELECT keys, COUNT(keys)
			FROM Roster
			WHERE Song_leader1 = '{instring}'
			OR Song_leader2 = '{instring}'
			OR Vocal = '{instring}'
			GROUP BY Keys
			ORDER BY COUNT(Keys) DESC
      		"""
			cur.execute(qry)
			info = cur.fetchone()
			max_keys_name = info[0].strip()
			max_keys_val = info[1]	
	
			qry = f"""
   			SELECT Guitar_1, COUNT(Guitar_1)
			FROM Roster
			WHERE Song_leader1 = '{instring}'
			OR Song_leader2 = '{instring}'
			OR Vocal = '{instring}'
			GROUP BY Guitar_1
			ORDER BY COUNT(Guitar_1) DESC
      		"""
			cur.execute(qry)
			update_dict(cur.fetchall())

			qry = f"""
			SELECT Guitar_2, COUNT(Guitar_2)
			FROM Roster
			WHERE (Song_leader1 = '{instring}'
			OR Song_leader2 = '{instring}'
			OR Vocal = '{instring}')
			AND Guitar_2 != ''
			GROUP BY Guitar_2
			ORDER BY COUNT(Guitar_2) DESC
      		"""
			cur.execute(qry)
			update_dict(cur.fetchall())
			max_guitar_name = max(dict.items(), key=operator.itemgetter(1))[0]
			max_guitar_val = dict[max_guitar_name]

			print(f"Below are the name and the frequency of members that {instring} has stood with")
			print(f"Vocal | {max_voc_name} : {max_voc_val}")
			print(f"Guitar | {max_guitar_name} : {max_guitar_val}")
			print(f"Keys | {max_keys_name} : {max_keys_val}")
		elif r == 'K':
			qry = f"""
			SELECT Song_leader1, COUNT(Song_leader1)
			FROM Roster
			WHERE Keys = '{instring}'
			OR Pads = '{instring}'
			GROUP BY Song_leader1
			ORDER BY COUNT(Song_leader1) DESC
      		"""
			cur.execute(qry)
			update_dict(cur.fetchall())

			qry = f"""
			SELECT Song_leader2, COUNT(Song_leader2)
			FROM Roster
			WHERE Keys = '{instring}'
			OR Pads = '{instring}'
			GROUP BY Song_leader2
			ORDER BY COUNT(Song_leader2) DESC
      		"""
			cur.execute(qry)
			update_dict(cur.fetchall())

			qry = f"""
   			SELECT Vocal, COUNT(Vocal)
			FROM Roster
			WHERE (Keys = '{instring}'
			OR Pads = '{instring}')
			AND Vocal != ''
			GROUP BY Vocal
			ORDER BY COUNT(Vocal) DESC
      		"""
			cur.execute(qry)
			update_dict(cur.fetchall())

			max_voc_name = max(dict.items(), key=operator.itemgetter(1))[0]
			max_voc_val = dict[max_voc_name]
			dict = dict.fromkeys(dict,0)
   
			qry = f"""
   			SELECT Guitar_1, COUNT(Guitar_1)
			FROM Roster
			WHERE Keys = '{instring}'
			GROUP BY Guitar_1
			ORDER BY COUNT(Guitar_1) DESC
      		"""
			cur.execute(qry)
			update_dict(cur.fetchall())

			qry = f"""
			SELECT Guitar_2, COUNT(Guitar_2)
			FROM Roster
			WHERE Keys = '{instring}'
			AND Guitar_2 != ''
			GROUP BY Guitar_2
			ORDER BY COUNT(Guitar_2) DESC
      		"""
			cur.execute(qry)
			update_dict(cur.fetchall())
			max_guitar_name = max(dict.items(), key=operator.itemgetter(1))[0]
			max_guitar_val = dict[max_guitar_name]

			print(f"Below are the name and the frequency of members that {instring} has stood with")
			print(f"Vocal | {max_voc_name} : {max_voc_val}")
			print(f"Guitar | {max_guitar_name} : {max_guitar_val}")

		elif r == 'D':
			qry = f"""
   			SELECT Song_leader1, COUNT(Song_leader1)
			FROM Roster
			WHERE Drum = '{instring}'
			GROUP BY Song_leader1
			ORDER BY COUNT(Song_leader1) DESC
      		"""
			cur.execute(qry)
			update_dict(cur.fetchall())
   
			qry = f"""
   			SELECT Song_leader2, COUNT(Song_leader2) 
   			FROM Roster 
      		WHERE Drum = '{instring}'
        	GROUP BY Song_leader2
         	ORDER BY COUNT(Song_leader2) DESC
          	"""
			cur.execute(qry)
			update_dict(cur.fetchall())
			qry = f"""
   			SELECT Vocal, COUNT(Vocal)
			FROM Roster
			WHERE Drum = '{instring}'
			AND Vocal != ''
			GROUP BY Vocal
			ORDER BY COUNT(Vocal) DESC
      		"""
			cur.execute(qry)
			update_dict(cur.fetchall())
		
			max_voc_name = max(dict.items(), key=operator.itemgetter(1))[0]
			max_voc_val = dict[max_voc_name]
			dict = dict.fromkeys(dict,0)
			qry = f"""
   			SELECT Keys, COUNT(keys)
			FROM Roster
			WHERE Drum = '{instring}'
			GROUP BY Keys
			ORDER BY COUNT(Keys) DESC
      		"""
			cur.execute(qry)
			info = cur.fetchone()
			max_keys_name = info[0].strip()
			max_keys_val = info[1]	
	
			qry = f"""
   			SELECT Guitar_1, COUNT(Guitar_1)
			FROM Roster
			WHERE Drum = '{instring}'
			GROUP BY Guitar_1
			ORDER BY COUNT(Guitar_1) DESC
      		"""
			cur.execute(qry)
			update_dict(cur.fetchall())

			qry = f"""
			SELECT Guitar_2, COUNT(Guitar_2)
			FROM Roster
			WHERE Drum = '{instring}'
			AND Guitar_2 != ''
			GROUP BY Guitar_2
			ORDER BY COUNT(Guitar_2) DESC
      		"""
			cur.execute(qry)
			update_dict(cur.fetchall())
			max_guitar_name = max(dict.items(), key=operator.itemgetter(1))[0]
			max_guitar_val = dict[max_guitar_name]

			print(f"Below are the name and the frequency of members that {instring} has stood with")
			print(f"Vocal | {max_voc_name} : {max_voc_val}")
			print(f"Guitar | {max_guitar_name} : {max_guitar_val}")
			print(f"Keys | {max_keys_name} : {max_keys_val}")	

		qry = f"""
        SELECT Songs.title 
        FROM Roster, Songs, Sunday_songs 
        WHERE Sunday_songs.sundayid = Roster.id 
        AND ('{instring}' in (roster.song_leader1, roster.song_leader2)) 
        AND Sunday_songs.songid = Songs.id;
        """
		cur.execute(qry)
		song_list = cur.fetchall()
		if song_list != []:
			dict = {}
			for songs in song_list:
				if songs[0].strip() in dict:
					dict[songs[0].strip()] += 1
				else:
					dict[songs[0].strip()] = 1
			picked_freq = max(dict.items(), key=lambda x: x[1])
			listOfKeys = list()

			print(f"    This member is a Song Leader and below are the songs that {instring} has picked the most")
			for key, value in dict.items():
				if value == picked_freq[1]:
					print(f"	{key} : {picked_freq[1]}")
     

			
      
            
   
except psycopg2.Error as err:
	print("DB error: ", err)
finally:
	if db:
		db.close()