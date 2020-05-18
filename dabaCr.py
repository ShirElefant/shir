import sqlite3

conn = sqlite3.connect('GAME200.db')
print ("Opened database successfully")

conn.execute('''CREATE TABLE GAME
         (QU TEXT PRIMARY KEY     NOT NULL,
         AN            TEXT     NOT NULL);''')
print ("Table created successfully")

conn.close()