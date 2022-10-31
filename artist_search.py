import sys
import psycopg2

### Artist Search ###
#   The program needs an argument for it to perform the artist search from the database
#   If the artist exists in the database, the program returns the number of songs that the artist have completed
#   Loops through the song title and returns to the user the name of the song.


# define any local helper functions here

# set up some globals

# process command-line args

argc = len(sys.argv)

# manipulate database

usage = "Usage: song_search.py 'Artist_Search'"
db = None

try:
    db = psycopg2.connect("dbname=nlpt22")
    cur = db.cursor()
    if argc == 1:
        print("No Artist included") # if there is no argument, notify the user that there was no input to search for an artist from the database
    else:
        insert = sys.argv[1:]
        instring = ''
        for i in insert:
            instring += i + ' '
        # The Code above grabs the arguments and converts into a readable string for the program to use.
        
        qry = f"""
        SELECT Songs.title
        FROM Songs, Artists
        WHERE Artists.name = '{instring}'
        AND Songs.artistid = Artists.id
        """
        cur.execute(qry)
        songInfo = cur.fetchall()   # Fetch information about songs that the artists have done from the database
        
        if not songInfo:    # if there are no songs that the artist have done, it notifies the user that there are no songs that the artist have done.
            print(f"\nNo songs from | {instring}|")
            print("===============")
        else:   # Notifies the user the number of songs that the artist have done.
            print(f"\nArtist: {instring} | Number of Songs: {len(songInfo)}")
            print("=======================================")
            for songs in songInfo:  # Loops throught the title of the song from the given artist and prints all the songs.
                print(f"    • {songs[0]}")
            print("")
        

            

except psycopg2.Error as err:
    print("DB error: ", err)
finally:
    if db:
        db.close()