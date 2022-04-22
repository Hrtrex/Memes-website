import sqlite3 as sql

def get_db_connection():
    conn = sql.connect('sqlite/baza.db')
    conn.row_factory = sql.Row
    return conn