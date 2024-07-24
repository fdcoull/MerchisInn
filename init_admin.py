import bcrypt
import sqlite3

conn = sqlite3.connect('var/merchisinn.db')
cursor = conn.cursor()

email = input("Input admin email: ")
password = input("Input admin password: ")

passwordHashed = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())

cursor.execute('INSERT INTO admins (email, password) VALUES ("'+ email +'", "'+ passwordHashed.decode('utf-8') +'")')

conn.commit()
conn.close()

print("Admin added")
