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

dance_classes_to_insert = [
    ('Hip Hop', 'Learn energetic and dynamic hip hop dance moves. Suitable for all skill levels.'),
    ('Ballet',
     'Experience the grace and discipline of classical ballet. Perfect for beginners and experienced dancers alike.'),
    ('Contemporary',
     'Explore fluid movements and self-expression in contemporary dance. Open to dancers of all backgrounds.'),
    ('Heels', 'Master the art of dancing in heels. A fun and empowering class for all genders and dance levels.'),
]

cur.executemany("INSERT INTO dance_classes (dance_class_name, dance_class_about) VALUES (?, ?)", dance_classes_to_insert)


connection.commit()
connection.close()
