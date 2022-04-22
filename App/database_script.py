import sqlite3

connection = sqlite3.connect('sqlite/baza.db')

cur = connection.cursor()

cur.execute("INSERT INTO blokady VALUES ('01-01-2021', '22-04-2021', 'jebac disa2', 124)")
cur.execute("INSERT INTO blokady VALUES ('01-01-2020', '22-04-2020', 'jebac disa3', 125)")
cur.execute("INSERT INTO blokady VALUES ('01-01-2019', '22-04-2019', 'jebac disa4', 126)")
connection.commit()
connection.close()