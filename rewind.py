import operator
import sys
import psycopg2
import os

## NewLife Praise Team Rewind 2022 ##
#  • Number of Songs we have done this year to this date (Show last commit) √
#  • List of Artists and how many of their songs we have done this year √
#  • Song title | Song Artist | Number of times we have done them √

#  • Member Name | Role | Number of times they stood this year √
#  • Song Leaders -> Most repeated songs and most repeated Artists

usage = "Usage: rewind.py 'rewind'"
db = None

print("This is a summary for our New Life Praise Team 2022")
print("---------------------------------------------------\n\n")


try:
    db = psycopg2.connect("dbname=nlpt22")
    cur = db.cursor()
    cur.execute("SELECT COUNT(songs), Sundays.date FROM Songs, Sundays WHERE Sundays.id = (SELECT max(id) FROM Sundays) GROUP BY Sundays.date")
    numSongs, last_commit = cur.fetchone()
    
    print(f"Up until {last_commit}, we have done {numSongs} songs\n")
    print(f"Out of {numSongs} songs, we have done:")
    qry = "SELECT Artists.name, count(Songs.artistid) FROM Artists, Songs WHERE Artists.id = Songs.artistid GROUP BY Artists.name ORDER BY COUNT DESC"
    cur.execute(qry)
    info = cur.fetchall()
    for item in info:
        if int(item[1]) == 1:
            print(f"• {item[1]} song is from {item[0].strip()}")
        else:
            print(f"• {item[1]} songs are from {item[0].strip()}")
    qry = """SELECT Songs.title as songs, Artists.name as artists, count(sunday_songs.sundayid) as count
    FROM Songs, Artists, Sundays, Sunday_songs 
    WHERE Songs.artistid = Artists.id 
    AND Sunday_songs.songid = Songs.id 
    AND Sunday_songs.sundayid = Sundays.id 
    GROUP BY Songs.title, Artists.name 
    ORDER BY count DESC, songs ASC"""
    
    cur.execute(qry)
    info = cur.fetchall()
    print("\nBelow are the songs, artists and the number of times the song was done throughout this year\n\n")
    for item in info:
        print(f"{item[0]} | {item[1]} | {item[2]}")
    
    print("\n\n--MEMBERS--")
    cur.execute("SELECT name, role from Members")
    memberInfo = cur.fetchall()
    
    for item in memberInfo:
        os.system(f"python3 member_search.py {item[0].strip()}")
        
    
    
    
except psycopg2.Error as err:
	print("DB error: ", err)
finally:
	if db:
		db.close()