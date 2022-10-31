# edit.py
# Asks for input of which sunday (dd.mm.yy)
# Asks what you would like to edit
#   Song Change
#       Replace Song
#       Add Song
#       Remove Song
#   Edit Passage
#   Edit Title
#   


import sys
import psycopg2
import datetime
import calendar
import os

# define any local helper functions here


# set up some globals

usage = "Usage: add_songs.py 'add_songs'"
db = None

# manipulate database

date = input("Add Date in the form [dd.mm.yy]\n")   # Asks for date to edit

day = int(date[0:2])
month = int(date[3:5])
year = int('20' + date[6:8])
d = datetime.date(year, month, day)
# The code above converts the input arguments into the datetime format to check if the given date is actually a Sunday

if d.isoweekday() != 7: # Exits program if the given date is NOT a Sunday.
    print(f"{date} is not a Sunday")
    exit()

options = input("What would you like to do?\n1) Song change\n2) Edit Passage\n3) Edit Title\n") # Otherwise, the program asks what editing you would like to do for the specific date


try:
    db = psycopg2.connect("dbname=nlpt22")
    cur = db.cursor()
    qry = f"SELECT * FROM Sundays WHERE date = '{date}'"
    cur.execute(qry)
    info = cur.fetchall()
    sundayid = info[0][0]
    title = info[0][2]
    passage = info[0][3].strip()
    
    if len(info) != 1:
        print(f"Sunday data for the date {date} doesn't exist")
        print("Exiting Program...")
        exit()
    
    match options:
        case '1':   #Song Change
            options = input("What would you like to do?\n1) Replace Song\n2) Add Song\n3) Remove Song\n")
            match options:
                case '1': # Replace Song: 1 to 1
                    os.system(f"python3 sunday_search.py {date}")   # Run Sunday_search.py to show the current information that is stored in the database.
                    original_title = input("What's the name of the song you would like to replace?\n")  # Asks for the original song that you would like to replace
                    replacement_title = input("What's the name of the new song you would like to insert?\n")    # Asks for the new song that you would like to add
                    replacement_artist = input("Who's the artist for the replacement song?\n")  # Asks for the artist of the new song that you would like to add
                    cur.execute(f"SELECT id FROM Songs WHERE title = '{replacement_title}'")
                    rsongid = cur.fetchone()
                    cur.execute(f"SELECT id FROM Songs WHERE title = '{original_title}'")
                    osongid = cur.fetchone()
                    osongid = int(osongid[0])
                    # Grab the songID for both original and replacement songs.
                    
                    if rsongid is None: # if the replacement songID does not exist in the database, add new song into the database
                        cur.execute("SELECT MAX(ID) FROM Songs")
                        sID = cur.fetchone()[0] + 1
                        
                        qry = f"SELECT id FROM Artists WHERE name = '{replacement_artist}'"
                        cur.execute(qry)
                        aID = cur.fetchone()[0].strip() # Fetch ArtistID for the replacement song
                        
                        if aID == None: # if the artistID does not exist in the database, add new artist into the database
                            aID = input(f"Enter new ID for new artist ({replacement_artist}) in database:\n")   # Ask for new artistID for the new Artist.
                            qry = f"""
                            INSERT INTO Artists (ID, Name)
                            VALUES ('{aID}', '{replacement_artist}')
                            """
                            cur.execute(qry)
                            db.commit() # Commit new artist with the given artistID into the database
                            print(f"{replacement_artist} ({aID}) added as a new artist in the database\n")  # Notifies the user that the artist has been added as a new artist with the given artistID into the database
                        qry = f"""
                        INSERT INTO Songs (ID, Title, ArtistID)
                        VALUES ({sID}, '{replacement_title}', '{aID}')
                        """
                        cur.execute(qry)
                        db.commit() # Commit new song with the relevant artistID
                        print(f"{sID} | {replacement_title} | {aID} added as a new song in the database\n") # Notifies the user that a new song has been added into the database
                        rsongid = sID   # set the replacement songID as sID whether or not if it already existed or it was just created.
                    else:
                        rsongid = int(rsongid[0])   # if the replacement song already exist in the database, update the sunday_songs table from the database with the new songID
                    qry = f"UPDATE Sunday_songs SET songid = {rsongid} WHERE songid = {osongid} AND sundayid = {sundayid}"
                    cur.execute(qry)
                    db.commit()
                    print(f"{original_title} removed\n{replacement_title} by {replacement_artist} added\n") # Notifies the user that the replacement song has been added successfully!
                    os.system(f"python3 sunday_search.py {date}")   # Run Sunday_search.py to allow the user to know that the Sunday has actually been updated with this function.
                case '2':   #Add Song
                    os.system(f"python3 sunday_search.py {date}")   # Run Sunday_search.py to show the current information that is stored in the database.
                    new_title = input("What's the name of the new song you would like to insert?\n")    # Title of the song
                    new_artist = input("Who's the artist for the replacement song?\n")  # Artist of the Song
                    
                    qry = f"SELECT Songs.id FROM Songs, Artists WHERE Songs.title = '{new_title}' AND Artists.name = '{new_artist}' AND Songs.artistid = Artists.id"
                    cur.execute(qry)
                    sID = cur.fetchone()    # Fetch the SongID
                    
                    if sID is None: # If the song doesn't exist in the database, add a new song into the database
                        cur.execute("SELECT MAX(ID) FROM Songs")
                        sID = cur.fetchone()[0] + 1
                        
                        qry = f"SELECT id FROM Artists WHERE name = '{new_artist}'"
                        cur.execute(qry)
                        aID = cur.fetchone()[0].strip() # Fetch ArtistID
                        
                        if aID == None: # if artistID doesn't exist, create a new artist into the datbase
                            aID = input(f"Enter new ID for new artist ({new_artist}) in database:\n")   # Asks for a new ID for the Artist
                            
                            qry = f"""
                            INSERT INTO Artists (ID, Name)
                            VALUES ('{aID}', '{new_artist}')
                            """
                            cur.execute(qry)
                            db.commit() # Add new artist into the database
                            print(f"{new_artist} ({aID}) added as a new artist in the database\n")  # Notifies the user that a new artist has been added to the database
                        qry = f"""
                        VALUES ({sID}, '{new_title}', '{aID}')
                        INSERT INTO Songs (ID, Title, ArtistID)
                        """
                        cur.execute(qry)
                        db.commit() # Add new song into the database with the relevant artistID
                        
                        print(f"{sID} | {new_title} | {aID} added as a new song in the database\n") # Notifies the user that a new song has been added to the database
                    else:   # If the song exists in the database
                        sID = int(sID[0])
                    qry = f"INSERT INTO Sunday_Songs (songID, SundayID) VALUES ({sID}, {sundayid})"
                    cur.execute(qry)
                    db.commit() # add new value into Sunday_songs with the given songID
                    print(f"{new_title} by {new_artist} added\n")   # Notifies the user that the song with the relevant artist has been added to the database for the specific Sunday.
                    os.system(f"python3 sunday_search.py {date}")   # Run Sunday_search.py to allow the user to know that the Sunday has actually been updated with this function. 
                case '3':
                    os.system(f"python3 sunday_search.py {date}")   # Run Sunday_search.py to show the current information that is stored in the database.
                    r_title = input("What's the name of the song you would like to remove?\n")  # Asks for the song you would like to remove
                    r_artist = input("Who's the artist of the song?\n") # Asks for the artist of the song you would like to remove
                    qry = f"""
                    SELECT Songs.id FROM Songs, Artists WHERE Songs.title = '{r_title}' AND Artists.name = '{r_artist}' AND Songs.artistid = Artists.id
                    """
                    cur.execute(qry)
                    sID = cur.fetchone()    # Fetch songID with the given title and artist
                    
                    if sID is None: # if the song doesn't exist, the user has inserted a song that doesn't exist in the database
                        print(f"{r_title} by {r_artist} is not in {date}\n") # prints error message and exits
                        exit()
                    
                    qry = f"DELETE FROM Sunday_songs WHERE sundayid = {sundayid} AND songid = {sID[0]}"
                    cur.execute(qry)
                    db.commit() # Remove the song from the Sunday in the database
                    print(f"{r_title} by {r_artist} removed from {date}\n") # Notifies user that the song has been removed
                    os.system(f"python3 sunday_search.py {date}")   # Run Sunday_search.py to allow the user to know that the Sunday has actually been updated with this function.
                    
                
        case '2':   #edit passage
            os.system(f"python3 sunday_search.py {date}")   # Run Sunday_search.py to show the current information that is stored in the database.
            new_passage = input("What's the replacement passage?\n")    # Asks for the new passage to replace the existing passage
            
            qry = f"UPDATE Sundays SET passage = '{new_passage}' WHERE date = '{date}'"
            cur.execute(qry)
            db.commit() # Update the passage for the given date
            print(f"Updated passage for {date} as {new_passage}\n") # Notifies the user that the new passage has been added
            os.system(f"python3 sunday_search.py {date}")   # Run Sunday_search.py to allow the user to know that the Sunday has actually been updated with this function.
        case '3': #edit title
            os.system(f"python3 sunday_search.py {date}")   # Run Sunday_search.py to show the current information that is stored in the database.
            new_title = input("What's the replacement title?\n")    # Asks for the new title to replace the existing title
            
            qry = f"UPDATE Sundays SET title = '{new_title}' WHERE date = '{date}'"
            cur.execute(qry)
            db.commit() # Update the title for the given date
            print(f"Updated title for {date} as {new_title}\n") # Notifies the user that the title has been updated
            os.system(f"python3 sunday_search.py {date}")   # Run Sunday_search.py to allow the user to know that the Sunday has actually been updated with this function.
    

except psycopg2.Error as err:
	print("DB error: ", err)
finally:
	if db:
		db.close()