import sqlite3

conn = sqlite3.connect('GAME200.db')
print ("Opened database successfully")

conn.execute("INSERT INTO GAME (QU,AN) \
      VALUES ('Months', 'january:february:march:april:may:june:july:august:september:october:november:december')");

conn.execute("INSERT INTO GAME (QU,AN) \
      VALUES ('Days', 'sunday:monday:tuesday:wednesday:thursday:friday:saturday"
             "')");



conn.commit()
print ("Records created successfully")
conn.close()
