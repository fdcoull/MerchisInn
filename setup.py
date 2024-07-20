import sqlite3

DB = 'var/merchisinn.db'

conn = sqlite3.connect(DB)
cursor = conn.cursor()

cursor.execute(""" 
        CREATE TABLE customers 
        (id INTEGER PRIMARY KEY AUTOINCREMENT,
        email TEXT,
        password TEXT,
        first_name TEXT,
        last_name TEXT)""")

cursor.execute("""
        CREATE TABLE bookings 
        (id INTEGER PRIMARY KEY AUTOINCREMENT,
        customer_id INTEGER,
        check_in TEXT,
        check_out TEXT,
        no_guests INTEGER,
        no_beds INTEGER,
        no_accessible INTEGER)""")

cursor.execute(""" 
        CREATE TABLE rooms 
        (id INTEGER PRIMARY KEY AUTOINCREMENT,
        no_king INTEGER,
        no_single INTEGER,
        accessible INTEGER)""")

cursor.execute("""
        CREATE TABLE allocations 
        (id INTEGER PRIMARY KEY AUTOINCREMENT,
        booking_id INTEGER,
        room_id INTEGER)""")

cursor.execute("""
        CREATE TABLE admins 
        (id INTEGER PRIMARY KEY AUTOINCREMENT,
        email TEXT,
        password TEXT)""")

# King rooms
cursor.execute('INSERT INTO rooms (no_king, no_single, accessible) VALUES (1, 0, 0)')
cursor.execute('INSERT INTO rooms (no_king, no_single, accessible) VALUES (1, 0, 0)')
cursor.execute('INSERT INTO rooms (no_king, no_single, accessible) VALUES (1, 0, 0)')
cursor.execute('INSERT INTO rooms (no_king, no_single, accessible) VALUES (1, 0, 0)')
cursor.execute('INSERT INTO rooms (no_king, no_single, accessible) VALUES (1, 0, 0)')

# King and sinlge rooms
cursor.execute('INSERT INTO rooms (no_king, no_single, accessible) VALUES (1, 1, 0)')
cursor.execute('INSERT INTO rooms (no_king, no_single, accessible) VALUES (1, 1, 0)')

# Family rooms
cursor.execute('INSERT INTO rooms (no_king, no_single, accessible) VALUES (1, 2, 0)')
cursor.execute('INSERT INTO rooms (no_king, no_single, accessible) VALUES (1, 2, 0)')

# Accessible rooms
cursor.execute('INSERT INTO rooms (no_king, no_single, accessible) VALUES (1, 2,1)')

conn.commit()
