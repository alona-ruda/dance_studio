import sqlite3

connection = sqlite3.connect('database.db')

with open('schema.sql') as f:
    connection.executescript(f.read())

cur = connection.cursor()

cur.execute("INSERT INTO teachers (name, surname) VALUES (?, ?)",
            ('Alice', 'Miller')
            )

cur.execute("INSERT INTO teachers (name, surname) VALUES (?, ?)",
            ('Ethan', 'Johnson')
            )

cur.execute("INSERT INTO teachers (name, surname) VALUES (?, ?)",
            ('Olivia', 'White')
            )

cur.execute("INSERT INTO teachers (name, surname) VALUES (?, ?)",
            ('Liam', 'Brown')
            )

cur.execute("INSERT INTO teachers (name, surname) VALUES (?, ?)",
            ('Ava', 'Davis')
            )

days_for_insert = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']

for day in days_for_insert:
    cur.execute("INSERT INTO days (day_name) VALUES (?)", (day,))

classes_to_insert = [
    ('Choreography',),
    ('Ballet',),
    ('Hip Hop',),
    ('Contemporary',),
]

cur.executemany("INSERT INTO classes (class_name) VALUES (?)", classes_to_insert)

connection.commit()
connection.close()
