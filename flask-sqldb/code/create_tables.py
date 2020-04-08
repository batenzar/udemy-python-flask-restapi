import sqlite3

connection = sqlite3.connect('data.db')
cursor = connection.cursor()

# create auto incrementing id primary key as int
# Note: you can't use 'id int' here. It must use full name so we use 'id INTERGER'
create_table = "CREATE TABLE IF NOT EXISTS users (id INTEGER PRIMARY KEY, username text, password text)"
cursor.execute(create_table)

create_table = "CREATE TABLE IF NOT EXISTS items (name text, price real)"
cursor.execute(create_table)

connection.commit()
connection.close()