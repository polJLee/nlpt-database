import psycopg2



name = input("What's the name of the new member?\n")
role = input("What's the role of this member?\n")


usage = "Usage: add_member.py 'add_member'"
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
    print("New member added!")
    print(f"{id} | {name} | {role}")
    

except psycopg2.Error as err:
	print("DB error: ", err)
finally:
	if db:
		db.close()