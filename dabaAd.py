import sqlite3

conn = sqlite3.connect('GAME200.db')
print ("Opened database successfully")

conn.execute("INSERT INTO GAME (QU,AN) \
      VALUES ('Months', 'january:february:march:april:may:june:July:August:September:October:November:December')");

conn.execute("INSERT INTO GAME (QU,AN) \
      VALUES ('Days', 'sunday:monday:tuesday:wednesday:thursday:friday:may"
             "')");



conn.commit()
print ("Records created successfully")
conn.close()