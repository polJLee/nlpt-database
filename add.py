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

date = input("Add Date in the form [dd.mm.yy]\n")
day = int(date[0:2])
month = int(date[3:5])
year = int('20' + date[6:8])
d = datetime.date(year, month, day) # change argument input into datetime format

if d.isoweekday() != 7: # check if the given date is actually a Sunday
    print(f"{date} is not a Sunday")
    exit()
        
title = input("Add Sermon Title\n") # sermon title
passage = input("Add Sermon Passage\n") # passage
numSongs = int(input("How many songs are there this week?\n")) # number of songs
songName = [None] * numSongs # create list of song title and artist name 
artistName = [None] * numSongs

i = 0
while i < numSongs: # asks for inputs of song title and artist
    songName[i] = input(f"What's Song number {i+1}?\n")
    artistName[i] = input("Who's the Artist?\n")
    i += 1
print("\n\n")


# manipulate database

usage = "Usage: add.py 'add'"
db = None

try:
    db = psycopg2.connect("dbname=nlpt22")
    cur = db.cursor()
    qry = f"SELECT * FROM Sundays WHERE date = '{date}'"
    cur.execute(qry)
    exists_info = cur.fetchall()
    
    if len(exists_info):    # Check if the data already exists
        print(f"Sunday data for the date {date} already exists")
        print("Exiting Program...")
        exit()
    
    # Below checks if a Sunday has been skipped
    qry = "SELECT date FROM Sundays WHERE id = (SELECT max(id) FROM Sundays)"
    cur.execute(qry)
    last_sunday = cur.fetchone()
    last_day = calendar.monthrange(year, month)[1]
    d_compare = datetime.date(int('20'+last_sunday[0][6:8]), int(last_sunday[0][3:5]), int(last_sunday[0][0:2]))
    change_day = int(last_sunday[0][0:2]) + 7
    if change_day > last_day:
        change_day = change_day - last_day
        change_month = month + 1
        d_compare = d_compare.replace(day = change_day, month = change_month)
    else:
        d_compare = d_compare.replace(day = change_day)
    
    # Exits the program if a Sunday has been skipped
    if d_compare < d:
        print(f"You have skipped a Sunday: {d_compare}")
        exit()
    
    # Returns to the user the given date, sermon title and the sermon passage of the specific Sunday
    print(f"{date} | {title} | {passage}")
    i = 0
    while i < numSongs: # Prints all the song title and artist of the Sunday
        print(f"    {songName[i]} by {artistName[i]}")
        i += 1

    confirmation = input("Are these input correct? y/n \n") # Confirmation of inputs to the database
        
    if confirmation == 'y':
        qry = f"""
        SELECT max(id) from Sundays
        """
        cur.execute(qry)    # Fetches a new id for the Sunday
        sundayID = cur.fetchone()[0] + 1
        qry = f"""
        INSERT INTO Sundays (ID, Date, Title, Passage)
        VALUES ({sundayID}, '{date}', '{title}', '{passage}');
        """
        cur.execute(qry)
        db.commit() # insert new sunday information to the database
        
        i = 0
        while i < numSongs: #Loop through each song and artists
            if "'" in songName[i]:
                songName[i] = songName[i].replace("'", "''")	# if an apostrophe is used as part of the song, replace it as '' to be used for queries
            songName[i] = songName[i].strip()
            
            if "'" in artistName[i]:
                artistName[i] = artistName[i].replace("'", "''")    # if an apostrophe is used as part of the artist name, replace it as '' to be used for queries
            artistName[i] = artistName[i].strip()
            
            qry = f"""
            SELECT Songs.id, Songs.title, Artists.name 
            FROM Songs, Artists 
            WHERE Songs.title = '{songName[i]}'
            AND Artists.name = '{artistName[i]}' 
            AND Songs.artistid = Artists.id
            """
            cur.execute(qry)
            info = cur.fetchall()   # Fetch song information from the database
            
            if len(info) == 0:  # if the song information does not exist in the database, insert new song information with new id
                cur.execute("SELECT MAX(ID) FROM Songs")
                sID = cur.fetchone()[0] + 1
                artistName[i] = artistName[i].strip()
                qry = f"SELECT id FROM Artists WHERE name = '{artistName[i]}'"  # Fetch Artist ID to insert the information for new song variable
                cur.execute(qry)
                aID = cur.fetchone()
                
                if aID == None: # if the artist is not part of the database, create new artist and add it to the database
                    aID = input(f"Enter new ID for new artist ({artistName[i]}) in database:\n")    # Asks for input for an artist ID for the new artist
                    
                    qry = f"""
                    INSERT INTO Artists (ID, Name)
                    VALUES ({aID}, {artistName[i]})
                    """
                    cur.execute(qry)
                    db.commit()
                    print(f"{artistName[i]} ({aID}) added as a new artist in the database\n")   # Notify the user that a new artist has been added to the database
                else:
                    aID = aID[0].strip()    # if the artist already exists, strip away whitespaces
                    
                qry = f"""
                INSERT INTO Songs (ID, Title, ArtistID)
                VALUES ({sID}, '{songName[i].strip()}', '{aID}');
                """
                cur.execute(qry)
                db.commit() # commit new song information with the relevant information to the database
                
                print("New Song added\n")   # Notifies the user that a new song has been added with the relevant information
                print(f"song_ID: {sID}  |  Song: {songName[i]}  |  Artist: {artistName[i]}  |  artist_ID: {aID}")
                songID = sID
                songTitle = songName[i]
                songArtist = artistName[i]
            else:   # if song exists in the database, add it to the relevant variables in order to update sunday_songs
                songID = info[0][0] 
                songTitle = info[0][1].strip()
                songArtist = info[0][2].strip()
            
            qry = f"""
            INSERT INTO Sunday_Songs (songID, SundayID)
            VALUES ({songID}, {sundayID})
            """
            cur.execute(qry)
            db.commit() # commit songID and sundayID into the table Sunday_Songs so that the user is able use Sunday_search.py to search what song we have done on a specific Sunday.
            i += 1
        
        print(f"{numSongs} Songs added\n")  # Notifies user that all the songs have been added successfully!
        
        
    else:
        print("Restart Program\n")  # if the confirmation input is not a 'y', it notifies the user to restart the program and exits.

    

except psycopg2.Error as err:
	print("DB error: ", err)
finally:
	if db:
		db.close()