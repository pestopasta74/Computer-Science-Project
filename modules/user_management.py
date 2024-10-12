import sqlite3
import bcrypt
from unittest import TestCase

class UserDatabase:
    def __init__(self):
        self.conn = sqlite3.connect('database.db')
        self.cursor = self.conn.cursor()
        self.create_table()

    def create_table(self):
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS users
                            (id INTEGER PRIMARY KEY AUTOINCREMENT,
                            email TEXT NOT NULL UNIQUE,
                            password TEXT NOT NULL,
                            is_admin BOOL NOR NULL);''')
        self.conn.commit()

    def add_user(self, email, password, is_admin=False):
        hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
        print(hashed_password)
        self.cursor.execute("INSERT INTO users (email, password, is_admin) VALUES (?, ?, ?)",  (email, hashed_password, is_admin))
        self.conn.commit()

    def check_user(self, email, password):
        self.cursor.execute("SELECT password FROM users WHERE email=?", (email,))
        user_password = self.cursor.fetchone()
        if not user_password:
            return False
        user_password = user_password[0]
        if user_password:
            if password == user_password or bcrypt.checkpw(password.encode("utf-8"), user_password.encode("utf-8")):
                return user_password
        return False

    def close_connection(self):
        self.cursor.close()
        self.conn.close()

def main():
    db = UserDatabase()
    db.add_user('john@hotmail.com', 'password123', is_admin=True)

if __name__ == '__main__':
    main()
