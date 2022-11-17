import sys
import psycopg2
import datetime
from sundays import sundays


usage = "Usage: Search_Roster.py 'search_roster'"
db = None

# process command-line args

argc = len(sys.argv)


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
    if argc == 1:   # if there was no name included as an argument
        print("No name included")
        exit()
    insert = sys.argv[1:]
    name = ''
    for item in insert:
        name += item + ' '
    name = name.strip()
    sList = sundays(today.month)
    
    cur.execute(f"SELECT MIN(id) FROM Roster WHERE month = '{month}'")
    minID = int(cur.fetchone()[0])
    
    qry = f"""
    SELECT id, song_leader1, song_leader2, vocal, guitar_1, guitar_2, keys, drum, pads 
    FROM roster where '{name}' in (song_leader1, song_leader2, vocal, guitar_1, guitar_2, keys, drum, pads) 
    AND month = '{month}';
    """
    cur.execute(qry)
    info = cur.fetchall()
    if len(info) == 0:
        print(f"{name} is not rostered for {month}")
        exit()
    rostered_date = []
    roster = []
    d_day = []
    
    for item in info:
        rosteredID = item[0]
        id = rosteredID - minID
        rostered_date.append(sList[id])
        d_day.append((datetime.date.fromisoformat(sList[id]) - today).days)
        list = []
        for name in item[1:]:
            name = name.strip()
            list.append(name)
        roster.append(list)

    i = 0
    while i < len(rostered_date):
        print(15*' ', end='')
        print(rostered_date[i], end='')
        print(5*' ', end='')
        if d_day[i] < 0:
            d_day[i] = -1*d_day[i]
            print(f"{d_day[i]} days ago", end='')
        else:
            print(f"in {d_day[i]} days", end='')
        print('')
        j = 0
        while j < len(Roles):
            if roster[i][j] == '':
                j += 1
            else:
                print(f"{Roles[j]} : {roster[i][j]}")
                j += 1
        i += 1
    
    
except psycopg2.Error as err:
	print("DB error: ", err)
finally:
	if db:
		db.close()