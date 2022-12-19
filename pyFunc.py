import os
import psycopg2
import datetime
import operator
import calendar
from sundays import sundays

def song_search(txt):
    ### Song Search ###
    #	Include the title of the song as part of an argument
    #	Returns the number of times the song was used
    # 	Returns the date the song was used


    # define any local helper functions here

    # set up some globals

    usage = "Usage: song_search.py 'Song_Search'"
    db = None


    # manipulate database

    try:
        db = psycopg2.connect("dbname=nlpt22")
        cur = db.cursor()
        if len(txt) == 0:	# if no song title was included, notify the user and exit the program
            returnString = "No title included"
        else:
            instring = txt
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
                returnString = f"No songs matching | {instring}|==============="
            else:   # if the song exists in the database
                if len(artistinfo) == 1:    # if there is only one artist for the song
                    returnString = f"{instring} by {artistinfo[0][0]}\n"
                    returnString += f"=== This song was picked {len(sundayinfo)} times\n"
                    returnString += "=== Below are the Sundays that the song was picked\n"
                    for i in sundayinfo:
                        returnString += (f"    • {i[0]}\n")  # loop through all the dates and returns it to the user
                    returnString += (' ')
                else:   # if the song is covered by more than one artist
                    returnString = f"This song is covered by multiple artists\n"

                    for i in artistinfo:
                        returnString +=  f"{instring} by {i[0].strip()}\n"
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
                            returnString += f"	• {i[0]}\n"  # loop and return to the user the dates that the song was done by the specific artist
    except psycopg2.Error as err:
        returnString = ("DB error: ", err)
    finally:
        if db:
            db.close()

    return returnString

def sunday_search(txt):
    ### Sunday Search ###
    #   Given the date as an argument
    #   Returns the Sermon Title, Passage and Songs with Artists to the user

    # set up some globals

    usage = "Usage: sunday_search.py 'Sunday_Search'"
    db = None
    # manipulate database

    try:
        db = psycopg2.connect("dbname=nlpt22")
        cur = db.cursor()
        if len(txt) == 0:   # if there was no date included as an argument
            returnString = "No date included"
        elif '/' in txt:
            returnString = f"{txt} <- Please try again with the date format: dd.mm.yy"
            return returnString
        else:
            insert = txt
            date = datetime.date.today()
            date = date.replace(month = int(insert[3:5]), day = int(insert[0:2]))   # Store argument as a datetime form
            
            if date.isoweekday() != 7:  # if the date is not a Sunday, notify the user and exit the program
                returnString = f"{insert} is not a Sunday"
                return returnString
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
                    returnString = f"{insert} is ahead of time and not included in the database"
                    return returnString
            if not sundayinfo:  # if the Sunday is not part of the database, notify the user and exit the program
                returnString = f"\nThere are no Songs on this date: {insert}"
                return returnString
            else:   # if the information about the Sunday exists,
                qry = f"""
                SELECT title, passage
                FROM Sundays
                WHERE date = '{insert}'
                """
                cur.execute(qry)
                sInfo = cur.fetchall()[0]   # Fetch Sermon Title and Sermon Passage
                returnString = (f"{insert} | {sInfo[0]} | {sInfo[1].strip()}\n")  # output date, title, passage
                returnString += (f"\nSongs picked on {insert} are:\n")

                for i in sundayinfo:
                    returnString += (f"{i[0]} | {i[1]}\n")   # Loop through all the songs and artists and outputs to the user
                return returnString
    except psycopg2.Error as err:
        returnString = ("DB error: ", err)
    finally:
        if db:
            db.close()
             
def month_sunday_search(txt):
    ### Month Sunday Search ###
    #   Given the month as an argument (January, February)
    #   Returns the Sermon Title, Passage and Songs with Artists to the user

    # set up some globals
    # manipulate database
    Months = ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"]
    
    if txt in Months:
        st = int(Months.index(txt)) + 1
        today = datetime.date.today()
        sList = sundays(st, today.year)
    returnString = '\n'
    for sunday in sList:
        date = sunday[8:10] + '.' + sunday[5:7] + '.' + sunday[2:4]
        returnString += sunday_search(date)
    return returnString    

def member_search(txt):
    ### Member Search ###

    # define any local helper functions here

    # This function grabs the items of the given information and updates the dictionary.
    def update_dict(info):
        for item in info:
            dict[item[0].strip()] += int(item[1])
        


    # set up some globals

    usage = "Usage: member_search.py 'Member_Search'"
    db = None

    # manipulate database

    try:
        db = psycopg2.connect("dbname=nlpt22")
        cur = db.cursor()
        if len(txt) == 1:	# if there was no argument included with the program, it notifies the user that there was no member included and exits
            returnString = "No Member included"
            return returnString
        else:	# if the member name was included,
            instring = txt

            # The code above takes in the argument and stores it as a string for the program to access  

            qry = f"""
            SELECT role
            FROM Members
            WHERE name = '{instring}'
            """
            cur.execute(qry)
            role = cur.fetchone()   # Fetch the role of the member

            if role is None:    # if the member does not have a role, they are not part of Praise Team
                returnString = f"{instring} is not a member of the Praise Team"
                return returnString

            role = role[0].strip()
            countqry = ""   # qry that finds the frequency the member has stood
            sleaderqry = "" # qry specific for song_leaders that finds the frequency the member has stood as a song leader
            instqry = "" # qry specific for instrumentalist that finds the frequency the member has stood as an instrumentalist
            vqry = "" # qry specific for vocalists that finds the frequency the member has stood as a vocalist
            r = "" # role of the member specified as an ID

            if "Vocal" in role:
                if "Guitar" in role:    # Role = Vocal + Guitar
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
            total = cur.fetchone()  # Fetch frequency member has stood
            total = total[0]
            total_s = "" # Result for sleaderqry
            total_v = "" # Result for vqry
            total_i = "" # Result for instqry

            # Executes qry if they exist and stores in the relevant variables
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


            # Return information related to the member
            returnString = f"\nMember Name: {instring}\n"
            returnString += f"Role: {role}\n"

            # if the result of song leader and vocal is empty, output relevant information for instrumentalists
            if total_s == "" and total_v == "":
                returnString += f"In 2022, {instring} stood {total} times\n"
            else:
                returnString += f"In 2022, {instring} stood {total} times: "   # output information for song leaders or vocalists
                if total_i == "":   # if the member doesn't have a role as an instrumentalist, output the string below
                    returnString += f"{total_s} times as a Song Leader and {total_v} times as a Vocal\n"
                else:   # output for song leaders who are also vocalist and instrumentalist
                    returnString += f"{total_s} times as a Song Leader and {total_v} times as a Vocal and {total_i} times as an Instrumentalist\n"

            cur.execute("SELECT name FROM Members")
            members = cur.fetchall()    # Fetch names of all members

            # insert these members into a dictionary
            dict = {}
            for item in members:
                dict[item[0].strip()] = 0
            dict.pop(instring)  # Remove the given member from the dictionary

            # Using the roles that was found from the above queries, the code below executes multiple queries to find the member that stood the most with the given member name
            if r == "VG":
                qry = f"""
                SELECT Song_leader2, COUNT(Song_leader2) 
                FROM Roster 
                WHERE Song_leader1 = '{instring}'
                AND Song_leader2 != ''
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
                AND Song_leader2 != ''
                GROUP BY Song_leader2
                ORDER BY COUNT(Song_leader2) DESC
                """
                cur.execute(qry)
                update_dict(cur.fetchall())
                max_voc_name = max(dict.items(), key=operator.itemgetter(1))[0]     # Grab the name of the vocalist member who has stood most with the given member
                max_voc_val = dict[max_voc_name]       # Find the frequency of the vocalist member that stood the most with the given member
                dict = dict.fromkeys(dict,0)           # Reset Dictionary

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
                max_keys_name = info[0].strip()     # Grab the name of the pianist member who ahs stood most with the given member
                max_keys_val = info[1]              # Find the frequency of the pianist member that stood the most with the given member
                returnString += f"Below are the name and the frequency of members that {instring} has stood with\n"    # Output the information from the dictionaries
                returnString += f"   Vocal | {max_voc_name} : {max_voc_val}\n"
                returnString += f"Keys  | {max_keys_name} : {max_keys_val}\n"
            elif r == 'VK':
                qry = f"""
                SELECT Song_leader2, COUNT(Song_leader2) 
                FROM Roster 
                WHERE Song_leader1 = '{instring}'
                AND Song_leader2 != ''
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
                max_voc_name = max(dict.items(), key=operator.itemgetter(1))[0]     # Grab the name of the vocalist member who has stood most with the given member
                max_voc_val = dict[max_voc_name]                                    # Find the frequency of the vocalist member that stood the most with the given member
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
                max_guitar_name = max(dict.items(), key=operator.itemgetter(1))[0] # Grab the name of the vocalist member who has stood most with the given member 
                max_guitar_val = dict[max_guitar_name]                             # Find the frequency of the guitarist member that stood the most with the given member
                returnString += f"Below are the name and the frequency of members that {instring} has stood with\n" # Output the information from the dictionaries
                returnString += f"Vocal  | {max_voc_name} : {max_voc_val}\n"
                returnString += f"Guitar | {max_guitar_name} : {max_guitar_val}\n"
            elif r == 'V':

                qry = f"""
                SELECT Song_leader2, COUNT(Song_leader2) 
                FROM Roster 
                WHERE Song_leader1 = '{instring}'
                AND Song_leader2 != ''
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
                AND Song_leader2 != ''
                GROUP BY Song_leader2
                ORDER BY COUNT(Song_leader2) DESC
                """
                cur.execute(qry)
                update_dict(cur.fetchall())
                max_voc_name = max(dict.items(), key=operator.itemgetter(1))[0] # Grab the name of the vocalist member who has stood most with the given member
                max_voc_val = dict[max_voc_name]                                # Find the frequency of the vocalist member that stood the most with the given member
                dict = dict.fromkeys(dict,0)                                    # Reset dictionary
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
                max_keys_name = info[0].strip()     # Grab the name of the pianist member who has stood most with the given member
                max_keys_val = info[1]	            # Find the frequency of the pianist that stood the most with the given member

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
                max_guitar_name = max(dict.items(), key=operator.itemgetter(1))[0]  # Grab the name of the guitarist who has stood the most with the given member
                max_guitar_val = dict[max_guitar_name]                              # Find the frequency of the guitarist who has stood the most with the given member

                returnString += f"Below are the name and the frequency of members that {instring} has stood with\n"    # Output the information from the dictionaries
                returnString += f" Vocal  | {max_voc_name} : {max_voc_val}\n"
                returnString += f" Guitar | {max_guitar_name} : {max_guitar_val}\n"
                returnString += f"Keys   | {max_keys_name} : {max_keys_val}\n"
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
                WHERE (Keys = '{instring}'
                OR Pads = '{instring}')
                AND Song_leader2 != ''
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

                max_voc_name = max(dict.items(), key=operator.itemgetter(1))[0] # Grab the name of the vocalist who has stood the most with the given member
                max_voc_val = dict[max_voc_name]                                # Find the frequency of the vocalist who has stood the most with the given member
                dict = dict.fromkeys(dict,0)                                    # Reset the dictionary

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
                max_guitar_name = max(dict.items(), key=operator.itemgetter(1))[0]  # Grab the name of the guitarist who has stood the most with the given member
                max_guitar_val = dict[max_guitar_name]                              # Find the frequency of the guitarist who has stood the most with the given member

                returnString += f"Below are the name and the frequency of members that {instring} has stood with\n"    # Output the information from the dictionaries
                returnString += f"Vocal  | {max_voc_name} : {max_voc_val}\n"
                returnString += f"Guitar | {max_guitar_name} : {max_guitar_val}\n"

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
                AND Song_leader2 != ''
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

                max_voc_name = max(dict.items(), key=operator.itemgetter(1))[0] # Grab the name of the vocalist who has stood the most with the given member
                max_voc_val = dict[max_voc_name]                                # Find the frequency of the vocalist who has stood the most with the given member
                dict = dict.fromkeys(dict,0)                                    # Reset dictionary
                qry = f"""
                SELECT Keys, COUNT(keys)
                FROM Roster
                WHERE Drum = '{instring}'
                GROUP BY Keys
                ORDER BY COUNT(Keys) DESC
                """
                cur.execute(qry)
                info = cur.fetchone()
                max_keys_name = info[0].strip()                                # Grab the name of the pianist who has stood the most with the given member
                max_keys_val = info[1]	                                       # Find the frequency of the pianist who has stood the most with the given member

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
                max_guitar_name = max(dict.items(), key=operator.itemgetter(1))[0]  # Grab the name of the guitarist who has stood the most with the given member
                max_guitar_val = dict[max_guitar_name]                              # Find the frequency of the guitarist who has stood the msot with the given member

                returnString += f"Below are the name and the frequency of members that {instring} has stood with\n"    # Output the information from the dictionaries
                returnString += f" Vocal  | {max_voc_name} : {max_voc_val}\n"
                returnString += f" Guitar | {max_guitar_name} : {max_guitar_val}\n"
                returnString += f"Keys   | {max_keys_name} : {max_keys_val}\n"

            qry = f"""
            SELECT Songs.title 
            FROM Roster, Songs, Sunday_songs 
            WHERE Sunday_songs.sundayid = Roster.id 
            AND ('{instring}' in (roster.song_leader1, roster.song_leader2)) 
            AND Sunday_songs.songid = Songs.id;
            """
            cur.execute(qry)
            song_list = cur.fetchall()  # Fetch all songs that the member has done
            if song_list != []: # If they are a song leader
                dict = {}
                for songs in song_list: # Loop through the song list to find the most picked song by the song leader
                    if songs[0].strip() in dict:
                        dict[songs[0].strip()] += 1
                    else:
                        dict[songs[0].strip()] = 1
                picked_freq = max(dict.items(), key=lambda x: x[1]) # Finds the highest number in the dictionary of songs

                returnString += f"    This member is a Song Leader and below are the songs that {instring} has picked the most\n"
                for key, value in dict.items():
                    if value == picked_freq[1]:
                        returnString += f"• {key} : {picked_freq[1]}\n"  # returns the most picked song / songs that the song leader has chosen.
            return returnString

    except psycopg2.Error as err:
        returnString = ("DB error: ", err)
    finally:
        if db:
            db.close()

def artist_search(txt):
    ### Artist Search ###
    #   The program needs an argument for it to perform the artist search from the database
    #   If the artist exists in the database, the program returns the number of songs that the artist have completed
    #   Loops through the song title and returns to the user the name of the song.


    # define any local helper functions here

    # set up some globals

    # manipulate database

    usage = "Usage: song_search.py 'Artist_Search'"
    db = None

    try:
        db = psycopg2.connect("dbname=nlpt22")
        cur = db.cursor()
        if len(txt) == 1:
            returnString = "No Artist included" # if there is no argument, notify the user that there was no input to search for an artist from the database
            return returnString
        else:
            instring = txt
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
                returnString = f"\nNo songs from | {instring}|"
                return returnString

            else:   # Notifies the user the number of songs that the artist have done.
                returnString = f"\nArtist: {instring} | Number of Songs: {len(songInfo)}\n"
                returnString += "=======================================\n"
                for songs in songInfo:  # Loops throught the title of the song from the given artist and returnString = s all the songs.
                    returnString += f"    • {songs[0]}\n"

                return returnString
    except psycopg2.Error as err:
        print("DB error: ", err)
    finally:
        if db:
            db.close()

def roster_search(txt):
    usage = "Usage: Search_Roster.py 'search_roster'"
    db = None

    # Grab information related to the Month of the Roster
    Months = {1: "January",
            2: "Februrary",
            3: "March",   #Good Friday
            4: "April",   #Good Friday
            5: "May",
            6: "June",    #Wintercon
            7: "July",    #Wintercon
            8: "August",
            9: "September",
            10: "October",
            11: "November",
            12: "December"    #Christmas
            }
    Roles = ["Song Leader 1", "Song Leader 2", "Vocal", "Guitar 1", "Guitar 2", "Keys", "Drum", "Pads"]


    today = datetime.date.today()
    month = Months[today.month] #String format of the Month -> January, February, etc..

    try:
        db = psycopg2.connect("dbname=nlpt22")
        cur = db.cursor()
        if len(txt) == 0:   # if there was no name included as an argument
            returnString = "No name included"
            return returnString
        name = txt
        sList = sundays(today.month, today.year)

        d = sList[0]
        year = d[2:4]
        month = d[5:7]
        day = d[8:10]
        
        first_sun = day + "." + month + "." + year
        qry = f"SELECT id FROM Sundays WHERE date = '{first_sun}'"
        cur.execute(qry)
        fID = cur.fetchone()[0]
        
        cur.execute(f"SELECT MIN(id) FROM Roster WHERE month = '{month}' AND id >= {fID}")
        minID = int(cur.fetchone()[0])

        qry = f"""
        SELECT id, song_leader1, song_leader2, vocal, guitar_1, guitar_2, keys, drum, pads 
        FROM roster where '{name}' in (song_leader1, song_leader2, vocal, guitar_1, guitar_2, keys, drum, pads) 
        AND month = '{month}';
        """
        cur.execute(qry)
        info = cur.fetchall()
        if len(info) == 0:
            returnString = f"\n{name} is not rostered for {month}"
            return returnString
        rostered_date = []
        roster = []
        d_day = []

        for item in info:
            rosteredID = item[0]
            id = rosteredID - minID
            print(sList[id])
            rostered_date.append(sList[id])
            d_day.append((datetime.date.fromisoformat(sList[id]) - today).days)
            list = []
            for name in item[1:]:
                name = name.strip()
                list.append(name)
            roster.append(list)

        i = 0
        returnString = ""
        while i < len(rostered_date):
            returnString += 15*' ' + rostered_date[i] + 5*" "
            if d_day[i] < 0:
                d_day[i] = -1*d_day[i]
                returnString += f"{d_day[i]} days ago\n"
            else:
                returnString += f"in {d_day[i]} days\n"
            j = 0
            while j < len(Roles):
                if roster[i][j] == '':
                    j += 1
                else:
                    returnString += f"{Roles[j]} : {roster[i][j]}\n"
                    j += 1
            i += 1

        return returnString


    except psycopg2.Error as err:
        print("DB error: ", err)
    finally:
        if db:
            db.close()

def show_sunday():
    usage = "Usage: sunday_list.py 'sunday_list'"
    db = None
    returnString = "\n"

    try:
        db = psycopg2.connect("dbname=nlpt22")
        cur = db.cursor()
        cur.execute("SELECT date FROM Sundays GROUP BY date, sundays.id ORDER BY sundays.id")
        info = cur.fetchall()
        
        for item in info:
            returnString += sunday_search(item[0]) + '\n'
            
        returnString += f"There are {len(info)} Sundays in the database"
        
        return returnString
    except psycopg2.Error as err:
        print("DB error: ", err)
    finally:
        if db:
            db.close()

def show_members():
    usage = "Usage: pyFunc.py 'show_members'"
    db = None
    returnString = '\n'
    
    try:
        db = psycopg2.connect("dbname=nlpt22")
        cur = db.cursor()
        cur.execute("SELECT name FROM Members")
        info = cur.fetchall()
        
        for item in info:
            print(item[0].strip())
            if item[0].strip() == 'Annabel' or item[0].strip() == 'Annette':
                returnString += "\n" + f"Member Name: {item[0].strip()}\nRole: Sound" + "\n"
            else:
                returnString += member_search(item[0].strip()) + '\n'
        
        return returnString
    
    except psycopg2.Error as err:
        print("DB error: ", err)
    finally:
        if db:
            db.close()

def month_roster_search(txt):
    usage = "Usage: 'month_search'"
    db = None
    
    # Grab information related to the Month of the Roster
    Months = ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"]
    Roles = ["Song Leader 1", "Song Leader 2", "Vocal", "Guitar 1", "Guitar 2", "Keys", "Drum", "Pads"]


    try:
        db = psycopg2.connect("dbname=nlpt22")
        cur = db.cursor()
        today = datetime.date.today()
        if len(txt) == 0:   # if there was no month included as an argument
            returnString = "No month included"
            return returnString
        
        if txt.isdigit():
            txt = int(txt)
            sList = sundays(txt, today.year)
            txt = txt - 1
            mth = Months[txt]
        elif txt in Months:
            st = int(Months.index(txt)) + 1
            sList = sundays(st, today.year)
            mth = txt
        if txt == 'all' or txt == 'All':
            qry = f"""
            SELECT song_leader1, song_leader2, vocal, guitar_1, guitar_2, keys, drum, pads
            FROM Roster
            """
        else:    
            d = sList[0]
            year = d[2:4]
            month = d[5:7]
            day = d[8:10]
            
            first_sun = day + "." + month + "." + year
            qry = f"SELECT id FROM Sundays WHERE date = '{first_sun}'"
            cur.execute(qry)
            fID = cur.fetchone()[0]
            
            qry = f"""
                SELECT song_leader1, song_leader2, vocal, guitar_1, guitar_2, keys, drum, pads 
                FROM roster 
                WHERE month = '{mth}' AND id >= {fID}
                """
        cur.execute(qry)
        info = cur.fetchall()
        if len(info) == 0:
            returnString = f"\n{txt} is not in the roster\n"
            return returnString
        roster = []

        for item in info:
            list = []
            for name in item:
                if name == None:
                    list.append('')
                else:
                    name = name.strip()
                    list.append(name)
            roster.append(list)

        if txt == 'all' or txt == 'All':
            returnString = "\n"
            for m in range(1,12):
                sList = sundays(m, today.year)
                i = 0
                while i < len(sList):
                    returnString += sList[i] + '\n'
                    j = 0
                    while j < len(Roles):
                        print(j)
                        if roster[i][j] == '':
                            j += 1
                        else:
                            returnString += f"{Roles[j]} : {roster[i][j]}\n"
                            j += 1
                    i += 1
        else:
            i = 0
            returnString = "\n"
            while i < len(sList):
                returnString += sList[i] + '\n'
                j = 0
                while j < len(Roles):
                    if roster[i][j] == '':
                        j += 1
                    else:
                        returnString += f"{Roles[j]} : {roster[i][j]}\n"
                        j += 1
                i += 1
        
        return returnString
            
        
    except psycopg2.Error as err:
        print("DB error: ", err)
    finally:
        if db:
            db.close()

def add_member(name, role):
    db = None
    try:
        db = psycopg2.connect("dbname=nlpt22")
        cur = db.cursor()
        cur.execute("SELECT MAX(ID) FROM Members")
        id = int(cur.fetchone()[0]) + 1
        
        qry = f"""
        INSERT INTO Members(ID, Name, Role)
        VALUES({id}, '{name}', '{role}')
        """
        
        cur.execute(qry)
        db.commit()
        returnString = f"New member Added!\n{id} | {name} | {role}"
        return returnString
    except psycopg2.Error as err:
        print("DB error: ", err)
    finally:
        if db:
            db.close()
    
def add_sunday(date, sermon_title, passage, songs, artists):
    db = None
    day = int(date[0:2])
    month = int(date[3:5])
    year = int('20' + date[6:8])
    d = datetime.date(year, month, day) # change argument input into datetime format
    
    if d.isoweekday() != 7:
        returnString = f"{date} is not a Sunday\n"
        return returnString
    
    try:
        db = psycopg2.connect("dbname=nlpt22")
        cur = db.cursor()
        qry = f"SELECT * FROM Sundays WHERE date = '{date}'"
        cur.execute(qry)
        exists_info = cur.fetchall()
        if len(exists_info):    # Check if the data already exists
            returnString = f"Sunday data for the date {date} already exists\n"
            return returnString
        
        # Below checks if a Sunday has been skipped
        qry = "SELECT date FROM Sundays WHERE id = (SELECT max(id) FROM Sundays)"
        cur.execute(qry)
        last_sunday = cur.fetchone()
        last_day = calendar.monthrange(year, month)[1]
        d_compare = datetime.date(int('20'+last_sunday[0][6:8]), int(last_sunday[0][3:5]), int(last_sunday[0][0:2]))
        change_day = int(last_sunday[0][0:2]) + 7
        if change_day > last_day:
            change_day = change_day - calendar.monthrange(year, month-1)[1]
            if month != 12:
                change_month = month + 1
            else:
                change_month = 12
            d_compare = d_compare.replace(day = change_day, month = change_month)
        else:
            d_compare = d_compare.replace(day = change_day)
    
        # Exits the program if a Sunday has been skipped
        if d_compare < d:
            returnString = f"You have skipped a Sunday: {d_compare}\n"
            return returnString
            
    
        # Returns to the user the given date, sermon title and the sermon passage of the specific Sunday
        returnString = f"{date} | {sermon_title} | {passage}\n"
        i = 0
        while i < len(songs): # Prints all the song title and artist of the Sunday
            returnString += f"    {songs[i]} by {artists[i]}\n"
            i += 1
        
        qry = f"""
        SELECT max(id) from Sundays
        """
        cur.execute(qry)    # Fetches a new id for the Sunday
        sundayID = cur.fetchone()[0] + 1
        qry = f"""
        INSERT INTO Sundays (ID, Date, Title, Passage)
        VALUES ({sundayID}, '{date}', '{sermon_title}', '{passage}');
        """
        cur.execute(qry)
        db.commit() # insert new sunday information to the database
        
        i = 0
        while i < len(songs): #Loop through each song and artists
            if "'" in songs[i]:
                songs[i] = songs[i].replace("'", "''")	# if an apostrophe is used as part of the song, replace it as '' to be used for queries
            songs[i] = songs[i].strip()

            if "'" in artists[i]:
                artists[i] = artists[i].replace("'", "''")    # if an apostrophe is used as part of the artist name, replace it as '' to be used for queries
            artists[i] = artists[i].strip()

            qry = f"""
            SELECT Songs.id, Songs.title, Artists.name 
            FROM Songs, Artists 
            WHERE Songs.title = '{songs[i]}'
            AND Artists.name = '{artists[i]}' 
            AND Songs.artistid = Artists.id
            """
            cur.execute(qry)
            info = cur.fetchall()   # Fetch song information from the database

            if len(info) == 0:  # if the song information does not exist in the database, insert new song information with new id
                cur.execute("SELECT MAX(ID) FROM Songs")
                sID = cur.fetchone()[0] + 1
                artists[i] = artists[i].strip()
                qry = f"SELECT id FROM Artists WHERE name = '{artists[i]}'"  # Fetch Artist ID to insert the information for new song variable
                cur.execute(qry)
                aID = cur.fetchone()

                if aID == None: # if the artist is not part of the database, create new artist and add it to the database
                    aID = input(f"Enter new ID for new artist ({artists[i]}) in database:\n")    # Asks for input for an artist ID for the new artist

                    qry = f"""
                    INSERT INTO Artists (ID, Name)
                    VALUES ({aID}, {artists[i]})
                    """
                    cur.execute(qry)
                    db.commit()
                    returnString += f"{artists[i]} ({aID}) added as a new artist in the database\n"   # Notify the user that a new artist has been added to the database
                else:
                    aID = aID[0].strip()    # if the artist already exists, strip away whitespaces

                qry = f"""
                INSERT INTO Songs (ID, Title, ArtistID)
                VALUES ({sID}, '{songs[i].strip()}', '{aID}');
                """
                cur.execute(qry)
                db.commit() # commit new song information with the relevant information to the database

                returnString += "New Song added\n"   # Notifies the user that a new song has been added with the relevant information
                returnString += f"song_ID: {sID}  |  Song: {songs[i]}  |  Artist: {artists[i]}  |  artist_ID: {aID}\n"
                songID = sID
            else:   # if song exists in the database, add it to the relevant variables in order to update sunday_songs
                songID = info[0][0] 

            qry = f"""
            INSERT INTO Sunday_Songs (songID, SundayID)
            VALUES ({songID}, {sundayID})
            """
            cur.execute(qry)
            db.commit() # commit songID and sundayID into the table Sunday_Songs so that the user is able use Sunday_search.py to search what song we have done on a specific Sunday.
            i += 1
        
        returnString += f"{len(songs)} Songs added into the database for {date}\n"  # Notifies user that all the songs have been added successfully!
        return returnString

    except psycopg2.Error as err:
        print("DB error: ", err)
    finally:
        if db:
            db.close()

def easter(year):
    
    year = int(year)

    D = 225 - 11*(year % 19)

    if D > 50:
        while D >= 51:
            D -= 30
    if D > 48:
        D -= 1

    E = int((year + (year/4) + D + 1) % 7)
    Q = D + 7 - E

    output = []
    if Q < 32:
        month = '03'
        Eday = Q
        Gday = str(Q - 2)
        output.append(f"{Eday}.{month}")
        output.append(f"{Gday}.{month}")
    else:
        month = '04'
        day = Q - 31
        if day < 10 and day > 2:
            Eday = '0' + str(day) 
            Gday = '0' + str(day - 2)
            output.append(f"{Eday}.{month}")
            output.append(f"{Gday}.{month}")
        elif day <= 2:
            day = '0' + str(day)
            output.append(f"{day}.{month}")
            month = '03'
            day = str(31 - (2-int(day)))
            output.append(f"{day}.{month}")
        else:
            output.append(f"{day}.{month}")
            day = str(day - 2)
            output.append(f"{day}.{month}") 
    return output
   
def numWeeks(Month):
    if Month == 'Wintercon' or Month == 'wintercon':
        return 4
    else:
        # Grab information related to the Month of the Roster
        Months = {
                "January"   : 1,
                "Februrary" : 2,
                "March"     : 3,   #Good Friday
                "April"     : 4,   #Good Friday
                "May"       : 5,
                "June"      : 6,    #Wintercon
                "July"      : 7,    #Wintercon
                "August"    : 8,
                "September" : 9,
                "October"   : 10,
                "November"  : 11,
                "December"  : 12    #Christmas
        }
        Month = Months[Month]
        today = datetime.date.today()
        Easter = easter(today.isoformat()[0:4])
        
        start = today.replace(month=Month, day=1)       # Get the first date of the month
        last_day = calendar.monthrange(2022,Month)[1]   # Get the last day of the month
        end = start.replace(day=last_day)               # last date of the month
        numWeeks = 0
        
        for i in range(start.day, end.day): # Loop through start to end date of the month and find the number of Sundays for the month
            d = datetime.date(year=2022, month = Month, day = i)
            if d.isoweekday() == 7:
                numWeeks += 1
            i += 1
        if (Month == int(Easter[1][4])):   # add an extra day if Good Friday occurs on this month
            numWeeks += 1
        if (Month == 12 and (today.replace(month=12,day=25).isoweekday()) != 7):   # add an extra day if Christmas is included in the roster AND Christmas does not fall on a Sunday
            numWeeks += 1
        return numWeeks

def add_roster(month, song_leader1, song_leader2, vocal, guitar_1, guitar_2, keys, drum, pads):
    try:
        db = psycopg2.connect("dbname=nlpt22")
        cur = db.cursor()
        cur.execute("SELECT MAX(id) FROM Roster")
        id = cur.fetchone()[0]
        rid = id
        for i in range (0, len(song_leader1)):
            rid += 1
            qry = f"""
            INSERT INTO Roster(id, month, song_leader1, song_leader2, vocal, guitar_1, guitar_2, keys, drum, pads)
            VALUES ({rid}, '{month}', '{song_leader1[i]}', '{song_leader2[i]}', '{vocal[i]}', '{guitar_1[i]}', '{guitar_2[i]}', '{keys[i]}', '{drum[i]}', '{pads[i]}')
            """
            cur.execute(qry)
            db.commit()
        qry = f"SELECT song_leader1, song_leader2, vocal, guitar_1, guitar_2, keys, drum, pads FROM Roster WHERE id > {id}"
        cur.execute(qry)
        results = cur.fetchall()
        
        today = datetime.date.today()
        Months = {
                "January"   : 1,
                "Februrary" : 2,
                "March"     : 3,   #Good Friday
                "April"     : 4,   #Good Friday
                "May"       : 5,
                "June"      : 6,    #Wintercon
                "July"      : 7,    #Wintercon
                "August"    : 8,
                "September" : 9,
                "October"   : 10,
                "November"  : 11,
                "December"  : 12    #Christmas
               }
        
    
        sList = sundays(Months[month], today.year)
        returnString = "\n"
        RolesList = []
        NamesList = []
        for i in range(0, len(results)):
            Roles = []
            names = []
            roster = results[i]
            RoleStandard = ["Song Leader 1", "Song Leader 2", "Vocal", "Guitar 1", "Guitar 2", "Keys", "Drum", "Pads"]
            for j in range(0, len(RoleStandard)):
                if roster[j] != '               ':
                    names.append(roster[j])
                    Roles.append(RoleStandard[j])
                j += 1
            RolesList.append(Roles)
            NamesList.append(names)
            i += 1
        
        print(RolesList)
        print(NamesList)
        
        for k in range(0,len(results)):
            names = NamesList[k]
            returnString += f"{sList[k]}\n"
            r = RolesList[k]
            name = NamesList[k]
            for m in range(0, len(name)):
                returnString += f"  {r[m]} : {name[m].strip()}\n"         #   add Roles into a new list for each Sundays
                m += 1
            k += 1
                        
        return returnString
        
    except psycopg2.Error as err:
        print("DB Error: ", err)
    finally:
        if db:
            db.close()
    
        