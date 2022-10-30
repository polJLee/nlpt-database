import sys
import psycopg2
import datetime
import calendar

### Sunday Search ###

# define any local helper functions here




# set up some globals

usage = "Usage: sunday_search.py 'Sunday_Search'"
db = None

# process command-line args

argc = len(sys.argv)

# manipulate database

try:
    db = psycopg2.connect("dbname=nlpt22")
    cur = db.cursor()
    if argc == 1:
        print("No date included")
    else:
        insert = sys.argv[1:]
        insert = insert[0]
        
        date = datetime.date.today()
        date = date.replace(month = int(insert[3:5]), day = int(insert[0:2]))
        if date.isoweekday() != 7:
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
        sundayinfo = cur.fetchall()
        if today < date:
            if not sundayinfo:
                print(f"{insert} is ahead of time and not included in the database")
                exit()

        if not sundayinfo:
            print(f"\nThere are no Songs on this date: {insert}")
            print("===============")
        else:
            qry = f"""
            SELECT title, passage
            FROM Sundays
            WHERE date = '{insert}'
            """
            cur.execute(qry)
            sInfo = cur.fetchall()[0]
            print(f"\n{insert} | {sInfo[0]} | {sInfo[1].strip()}")
            print(f"\nSongs picked on {insert} are:\n")

            for i in sundayinfo:
                print(f"{i[0]} | {i[1]}")	
            print('')
            


except psycopg2.Error as err:
    print("DB error: ", err)
finally:
    if db:
        db.close()