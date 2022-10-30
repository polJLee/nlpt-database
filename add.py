# add.py
# Asks for input of which sunday (dd.mm.yy)
# Asks for Sermon Title and Passage
# Ask for song 1,2,3 with artist 1,2,3
# if song exists, add to sunday_songs else, add new song or artist

import sys
import psycopg2
import datetime
import calendar

# define any local helper functions here


# set up some globals

usage = "Usage: add_songs.py 'add_songs'"
db = None

# manipulate database

date = input("Add Date in the form [dd.mm.yy]\n")

day = int(date[0:2])
month = int(date[3:5])
year = int('20' + date[6:8])
d = datetime.date(year, month, day)

if d.isoweekday() != 7:
    print(f"{date} is not a Sunday")
    exit()
        
title = input("Add Sermon Title\n")
passage = input("Add sermon passage\n")
numSongs = int(input("How many songs are there this week?\n"))
songName = [None] * numSongs
artistName = [None] * numSongs
i = 0
while i < numSongs:
    songName[i] = input(f"What's Song number {i+1}?\n")
    artistName[i] = input("Who's the Artist?\n")
    i += 1
print("\n\n")

try:
    db = psycopg2.connect("dbname=nlpt22")
    cur = db.cursor()
    qry = f"SELECT * FROM Sundays WHERE date = '{date}'"
    cur.execute(qry)
    exists_info = cur.fetchall()
    
    if len(exists_info):
        print(f"Sunday data for the date {date} already exists")
        print("Exiting Program...")
        exit()
    
    qry = "SELECT date FROM Sundays WHERE id = (SELECT max(id) FROM Sundays)"
    cur.execute(qry)
    last_sunday = cur.fetchone()
    last_day = calendar.monthrange(year, month)[1]
    d_compare = datetime.date(int('20'+last_sunday[0][6:8]), int(last_sunday[0][3:5]), int(last_sunday[0][0:2]))
    # print(d_compare.isoformat())
    change_day = int(last_sunday[0][0:2]) + 7
    if change_day > last_day:
        change_day = change_day - last_day
        change_month = month + 1
        
        print(change_day)
        print(change_month)
        d_compare = d_compare.replace(day = change_day, month = change_month)
    else:
        d_compare = d_compare.replace(day = change_day)
    
    if d_compare < d:
        print(f"You have skipped a Sunday: {d_compare}")
        exit()
    
    print(f"{date} | {title} | {passage}")
    i = 0
    while i < numSongs:
        print(f"    {songName[i]} by {artistName[i]}")
        i += 1

    confirmation = input("Are these input correct? y/n \n")
    
    
    if confirmation == 'y':
        qry = f"""
        SELECT max(id) from Sundays
        """
        cur.execute(qry)
        sundayID = cur.fetchone()[0] + 1
        qry = f"""
        INSERT INTO Sundays (ID, Date, Title, Passage)
        VALUES ({sundayID}, '{date}', '{title}', '{passage}');
        """
        cur.execute(qry)
        db.commit()
        
        i = 0
        while i < numSongs:
            qry = f"""
            SELECT Songs.id, Songs.title, Artists.name 
            FROM Songs, Artists 
            WHERE Songs.title = '{songName[i]}' 
            AND Artists.name = '{artistName[i]}' 
            AND Songs.artistid = Artists.id
            """
            cur.execute(qry)
            info = cur.fetchall()
            
            if len(info) == 0:
                cur.execute("SELECT MAX(ID) FROM Songs")
                sID = cur.fetchone()[0] + 1
                artistName[i] = artistName[i].strip()
                qry = f"SELECT id FROM Artists WHERE name = '{artistName[i]}'"
                
                cur.execute(qry)
                aID = cur.fetchone()
                if aID == None:
                    aID = input(f"Enter new ID for new artist ({artistName[i]}) in database:\n")
                    
                    qry = f"""
                    INSERT INTO Artists (ID, Name)
                    VALUES ({aID}, {artistName[i]})
                    """
                    cur.execute(qry)
                    db.commit()
                    print(f"{artistName[i]} ({aID}) added as a new artist in the database\n")
                else:
                    aID = aID[0].strip()
                    
                qry = f"""
                INSERT INTO Songs (ID, Title, ArtistID)
                VALUES ({sID}, '{songName[i].strip()}', '{aID}');
                """
                cur.execute(qry)
                db.commit()
                
                print("New Song added\n")
                print(f"song_ID: {sID}  |  Song: {songName[i]}  |  Artist: {artistName[i]}  |  artist_ID: {aID}")
                songID = sID
                songTitle = songName[i]
                songArtist = artistName[i]
            else:
                songID = info[0][0]
                songTitle = info[0][1].strip()
                songArtist = info[0][2].strip()
            
            qry = f"""
            INSERT INTO Sunday_Songs (songID, SundayID)
            VALUES ({songID}, {sundayID})
            """
            cur.execute(qry)
            db.commit()
            i += 1
        
        print(f"{numSongs} Songs added\n")
        
        
    else:
        print("Restart Program\n")

    

except psycopg2.Error as err:
	print("DB error: ", err)
finally:
	if db:
		db.close()