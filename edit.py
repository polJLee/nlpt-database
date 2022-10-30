# edit.py
# Asks for input of which sunday (dd.mm.yy)
# Asks what you would like to edit


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

date = input("Add Date in the form [dd.mm.yy]\n")

day = int(date[0:2])
month = int(date[3:5])
year = int('20' + date[6:8])
d = datetime.date(year, month, day)

if d.isoweekday() != 7:
    print(f"{date} is not a Sunday")
    exit()

options = input("What would you like to do?\n1) Song change\n2) Edit Passage\n3) Edit Title\n")


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
                    original_title = input("What's the name of the song you would like to replace?\n")
                    replacement_title = input("What's the name of the new song you would like to insert?\n")
                    replacement_artist = input("Who's the artist for the replacement song?\n")
                    cur.execute(f"SELECT id FROM Songs WHERE title = '{replacement_title}'")
                    rsongid = cur.fetchone()
                    cur.execute(f"SELECT id FROM Songs WHERE title = '{original_title}'")
                    osongid = cur.fetchone()
                    osongid = int(osongid[0])
                    
                    if rsongid is None:
                        cur.execute("SELECT MAX(ID) FROM Songs")
                        sID = cur.fetchone()[0] + 1
                        qry = f"SELECT id FROM Artists WHERE name = '{replacement_artist}'"
                        
                        cur.execute(qry)
                        aID = cur.fetchone()[0].strip()
                        if aID == None:
                            aID = input(f"Enter new ID for new artist ({replacement_artist}) in database:\n")
                            
                            qry = f"""
                            INSERT INTO Artists (ID, Name)
                            VALUES ('{aID}', '{replacement_artist}')
                            """
                            cur.execute(qry)
                            db.commit()
                            print(f"{replacement_artist} ({aID}) added as a new artist in the database\n")
                        qry = f"""
                        INSERT INTO Songs (ID, Title, ArtistID)
                        VALUES ({sID}, '{replacement_title}', '{aID}')
                        """
                        cur.execute(qry)
                        db.commit()
                        print(f"{sID} | {replacement_title} | {aID} added as a new song in the database\n")
                        rsongid = sID
                    else:
                        rsongid = int(rsongid[0])
                    qry = f"UPDATE Sunday_songs SET songid = {rsongid} WHERE songid = {osongid} AND sundayid = {sundayid}"
                    cur.execute(qry)
                    db.commit()
                    print(f"{original_title} removed\n{replacement_title} by {replacement_artist} added\n")
                    os.system(f"python3 sunday_search.py {date}")
                case '2':   #Add Song
                    new_title = input("What's the name of the new song you would like to insert?\n")
                    new_artist = input("Who's the artist for the replacement song?\n")
                    qry = f"""
                    SELECT Songs.id FROM Songs, Artists WHERE Songs.title = '{new_title}' AND Artists.name = '{new_artist}' AND Songs.artistid = Artists.id
                    """
                    cur.execute(qry)
                    sID = cur.fetchone()
                    if sID is None:
                        cur.execute("SELECT MAX(ID) FROM Songs")
                        sID = cur.fetchone()[0] + 1
                        qry = f"SELECT id FROM Artists WHERE name = '{new_artist}'"
                        
                        cur.execute(qry)
                        aID = cur.fetchone()[0].strip()
                        if aID == None:
                            aID = input(f"Enter new ID for new artist ({new_artist}) in database:\n")
                            
                            qry = f"""
                            INSERT INTO Artists (ID, Name)
                            VALUES ('{aID}', '{new_artist}')
                            """
                            cur.execute(qry)
                            db.commit()
                            print(f"{new_artist} ({aID}) added as a new artist in the database\n")
                        qry = f"""
                        INSERT INTO Songs (ID, Title, ArtistID)
                        VALUES ({sID}, '{new_title}', '{aID}')
                        """
                        cur.execute(qry)
                        db.commit()
                        print(f"{sID} | {new_title} | {aID} added as a new song in the database\n")
                    else:
                        sID = int(sID[0])
                    qry = f"INSERT INTO Sunday_Songs (songID, SundayID) VALUES ({sID}, {sundayid})"
                    cur.execute(qry)
                    db.commit()
                    print(f"{new_title} by {new_artist} added\n")
                    os.system(f"python3 sunday_search.py {date}")
                case '3':
                    r_title = input("What's the name of the song you would like to remove?\n")
                    r_artist = input("Who's the artist of the song?\n")
                    qry = f"""
                    SELECT Songs.id FROM Songs, Artists WHERE Songs.title = '{r_title}' AND Artists.name = '{r_artist}' AND Songs.artistid = Artists.id
                    """
                    cur.execute(qry)
                    sID = cur.fetchone()
                    if sID is None:
                        print(f"{r_title} by {r_artist} is not included in the database\n")
                        exit()
                    qry = f"DELETE FROM Sunday_songs WHERE sundayid = {sundayid} AND songid = {sID[0]}"
                    cur.execute(qry)
                    db.commit()
                    print(f"{r_title} by {r_artist} removed from {date}\n")
                    os.system(f"python3 sunday_search.py {date}")
                    
                
        case '2':   #edit passage
            new_passage = input("What's the replacement passage?\n")
            qry = f"UPDATE Sundays SET passage = '{new_passage}' WHERE date = '{date}'"
            cur.execute(qry)
            db.commit()
            print(f"Updated passage for {date} as {new_passage}\n")
            os.system(f"python3 sunday_search.py {date}")
        case '3': #edit title
            new_title = input("What's the replacement title?\n")
            qry = f"UPDATE Sundays SET title = '{new_title}' WHERE date = '{date}'"
            cur.execute(qry)
            db.commit()
            print(f"Updated title for {date} as {new_title}\n")
            os.system(f"python3 sunday_search.py {date}")
    

except psycopg2.Error as err:
	print("DB error: ", err)
finally:
	if db:
		db.close()