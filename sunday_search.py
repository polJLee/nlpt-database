import sys
import psycopg2
import datetime


### Sunday Search ###
#   Given the date as an argument
#   Returns the Sermon Title, Passage and Songs with Artists to the user

# set up some globals

usage = "Usage: sunday_search.py 'Sunday_Search'"
db = None

# process command-line args

argc = len(sys.argv)

# manipulate database

try:
    db = psycopg2.connect("dbname=nlpt22")
    cur = db.cursor()
    if argc == 1:   # if there was no date included as an argument
        print("No date included")
    else:
        insert = sys.argv[1:]
        insert = insert[0]  # Store argument as a string
        date = datetime.date.today()
        date = date.replace(month = int(insert[3:5]), day = int(insert[0:2]))   # Store argument as a datetime form
        
        if date.isoweekday() != 7:  # if the date is not a Sunday, notify the user and exit the program
            print(f"{insert} is not a Sunday")
            exit()
        today = datetime.date.today()
        
        qry = f"""
        SELECT Songs.title, Artists.name 
        FROM Sundays, Songs, Sunday_songs, Artists
        WHERE Sundays.date = '{insert}'
        AND Sunday_songs.sundayid = Sundays.id
        AND Songs.id = Sunday_Songs.songid
        AND Artists.id = Songs.artistid;
        """
        cur.execute(qry)
        sundayinfo = cur.fetchall() # Fetch the title of the songs and artists
        if today < date:    # if the date is ahead of time, notify the user and exit the program
            if not sundayinfo:
                print(f"{insert} is ahead of time and not included in the database")
                exit()

        if not sundayinfo:  # if the Sunday is not part of the database, notify the user and exit the program
            print(f"\nThere are no Songs on this date: {insert}")
            print("===============")
        else:   # if the information about the Sunday exists,
            qry = f"""
            SELECT title, passage
            FROM Sundays
            WHERE date = '{insert}'
            """
            cur.execute(qry)
            sInfo = cur.fetchall()[0]   # Fetch Sermon Title and Sermon Passage
            print(f"\n{insert} | {sInfo[0]} | {sInfo[1].strip()}")  # output date, title, passage
            print(f"\nSongs picked on {insert} are:\n")

            for i in sundayinfo:
                print(f"{i[0]} | {i[1]}")   # Loop through all the songs and artists and outputs to the user
            print('')
            


except psycopg2.Error as err:
    print("DB error: ", err)
finally:
    if db:
        db.close()