import sys
import psycopg2
import os


usage = "Usage: sunday_list.py 'rewind'"
db = None


try:
    db = psycopg2.connect("dbname=nlpt22")
    cur = db.cursor()
    cur.execute("SELECT date FROM Sundays GROUP BY date, sundays.id ORDER BY sundays.id")
    info = cur.fetchall()
    
    for item in info:
        os.system(f"python3 sunday_search.py {item[0]}")
        
    print(f"There are {len(info)} Sundays in the database")
except psycopg2.Error as err:
	print("DB error: ", err)
finally:
	if db:
		db.close()