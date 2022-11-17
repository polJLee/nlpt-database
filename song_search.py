import sys
import psycopg2

### Song Search ###
#	Include the title of the song as part of an argument
#	Returns the number of times the song was used
# 	Returns the date the song was used


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
    if argc == 1:	# if no song title was included, notify the user and exit the program
        print("No title included")
    else:
        insert = sys.argv[1:]
        instring = ''
        for i in insert:
            instring += i + ' '
        # Code above stores the title of the song as a string to be processed later on in the program

        if "'" in instring:
            instring = instring.replace("'", "''")	# if an apostrophe is used as part of the song, replace it as '' to be used for queries
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
        sundayinfo = cur.fetchall() # Fetch dates of Sundays the song appeared

        qry = f"""
        SELECT Artists.name 
        FROM Artists, Songs 
        WHERE UPPER(Songs.title) LIKE UPPER('{instring}')
        AND Songs.artistid = Artists.id"""
        cur.execute(qry)
        artistinfo = cur.fetchall() # Fetch the Artist of the song

        if not sundayinfo:  # if the song is not in the database
            print(f"\nNo songs matching | {instring}|\n===============")
        else:   # if the song exists in the database
            if len(artistinfo) == 1:    # if there is only one artist for the song
                print(f"\n{instring} by {artistinfo[0][0]}\n")
                print(f"=== This song was picked {len(sundayinfo)} times")
                print("=== Below are the Sundays that the song was picked")
                for i in sundayinfo:
                    print(f"    • {i[0]}")  # loop through all the dates and returns it to the user
                print('')
            else:   # if the song is covered by more than one artist
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
                    sundayinfo = cur.fetchall() # Fetch the dates that the song was done by the specific artist
                    for i in sundayinfo:
                        print(f"	• {i[0]}")  # loop and return to the user the dates that the song was done by the specific artist
                    print('')

            


except psycopg2.Error as err:
    print("DB error: ", err)
finally:
    if db:
        db.close()