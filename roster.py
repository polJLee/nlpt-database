# This Python Function will add new Roster for the Month
# - Asks for Month
import calendar
import psycopg2
import datetime
import subprocess
import sys
# set up some globals

usage = "Usage: roster.py 'roster'"
db = None

# helper functions

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



Month = int(input("Which Month would you like to put into the database?\n"))

today = datetime.date.today()
addition = 0


Easter = easter(today.isoformat()[0:4])

start = today.replace(month=Month, day=1)
last_day = calendar.monthrange(2022,Month)[1]
end = start.replace(day=last_day)
numWeeks = 0

for i in range(start.day, end.day):
    d = datetime.date(year=2022, month = Month, day = i)
    if d.isoweekday() == 7:
        numWeeks += 1
    i += 1
if (Month == int(Easter[0][4]) or Month == int(Easter[1][4]) or Month == 12):
    numWeeks += 1
if (Month == 6 or Month == 7):
    confirmation = input("is Wintercon happening this month?\n(y/n)")
    if confirmation == 'y':
        numWeeks += 1

# manipulate database
try:
    
    db = psycopg2.connect("dbname = nlpt22")
    cur = db.cursor()
    cur.execute(f"SELECT month FROM Roster WHERE month = '{Months[Month]}'")
    exists = cur.fetchall()
    if exists != []:
        print(f"The Roster for the month of {Months[Month]} already exists")
        exit()
    cur.execute("SELECT count(*) FROM Roster")
    id = cur.fetchone()[0]

    song_leader1 = [None] * i
    song_leader2 = [None] * i
    vocal = [None] * i
    guitar_1 = [None] * i
    guitar_2 = [None] * i
    keys = [None] * i
    drum = [None] * i
    pads = [None] * i
    
    for i in range(0,numWeeks):
        print(f"Start entering the Roster for the month '{Months[Month]}'")
        print(f"Week {i+1}")
        song_leader1[i] = input("Song Leader 1: ")
        song_leader2[i] = input("Song Leader 2: ")
        vocal[i] = input("Vocal: ")
        guitar_1[i] = input("Guitar 1: ")
        guitar_2[i] = input("Guitar 2: ")
        keys[i] = input("Keys: ")
        drum[i] = input("Drum: ")
        pads[i] = input("Pads: ")
        i += 1

    confirmation = input("Are these values right? Y/N\n")
    
    if confirmation == 'Y':
        for i in range(0, numWeeks):
            id += 1
            qry = f"""
            INSERT INTO Roster(id, month, song_leader1, song_leader2, vocal, guitar_1, guitar_2, keys, drum, pads) 
            VALUES ({id}, '{Months[Month]}', '{song_leader1[i]}', '{song_leader2[i]}', '{vocal[i]}', '{guitar_1[i]}', '{guitar_2[i]}', '{keys[i]}', '{drum[i]}', '{pads[i]}')
            """
            cur.execute(qry)
            db.commit()
        print("Successfully Uploaded!")
    else:
        print("Restart Program")
        
    
except psycopg2.Error as err:
	print("DB error: ", err)
finally:
	if db:
		db.close()