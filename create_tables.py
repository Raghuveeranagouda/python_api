import sqlite3

connection = sqlite3.connect('data.db')
cursor = connection.cursor()

create_query = "CREATE TABLE IF NOT EXISTS users(id INTEGER PRIMARY KEY, username text, password text)"
cursor.execute(create_query)

create_query = "CREATE TABLE IF NOT EXISTS items(name text, price real)"
cursor.execute(create_query)

connection.commit()
connection.close()
