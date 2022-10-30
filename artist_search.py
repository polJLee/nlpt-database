import sys
import psycopg2

### Artist Search ###

# define any local helper functions here

# set up some globals

usage = "Usage: song_search.py 'Artist_Search'"
db = None

# process command-line args

argc = len(sys.argv)

# manipulate database

try:
    db = psycopg2.connect("dbname=nlpt22")
    cur = db.cursor()
    if argc == 1:
        print("No Artist included")
    else:
        insert = sys.argv[1:]
        instring = ''
        for i in insert:
            instring += i + ' '
        qry = f"""
        SELECT Songs.title
        FROM Songs, Artists
        WHERE Artists.name = '{instring}'
        AND Songs.artistid = Artists.id
        """
        
        cur.execute(qry)
        songInfo = cur.fetchall()
        
        if not songInfo:
            print(f"\nNo songs from | {instring}|")
            print("===============")
        else:
            print(f"\nArtist: {instring} | Number of Songs: {len(songInfo)}")
            print("=======================================")
            for songs in songInfo:
                print(f"    • {songs[0]}")
            print("")
        

            

except psycopg2.Error as err:
    print("DB error: ", err)
finally:
    if db:
        db.close()