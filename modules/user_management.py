import sqlite3
import bcrypt

class UserDatabase:
    def __init__(self):
        self.conn = sqlite3.connect('database.db')
        self.cursor = self.conn.cursor()
        self.create_table()

    def create_table(self):
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS users
                            (id INTEGER PRIMARY KEY AUTOINCREMENT,
                            email TEXT NOT NULL UNIQUE,
                            password TEXT NOT NULL)''')
        self.conn.commit()

    def add_user(self, email, password):
        hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
        print(hashed_password)
        self.cursor.execute("INSERT INTO users (email, password) VALUES (?, ?)",  (email, hashed_password))
        self.conn.commit()

    def check_user(self, email, password):
        self.cursor.execute("SELECT password FROM users WHERE email=?", (email,))
        user_password = self.cursor.fetchone()[0]
        if user_password:
            if password == user_password or bcrypt.checkpw(password.encode("utf-8"), user_password.encode("utf-8")):
                return user_password
        return False

    def close_connection(self):
        self.cursor.close()
        self.conn.close()

# Example usage
if __name__ == '__main__':
    db = UserDatabase()
    db.add_user('john@hotmail.com', 'password123')
    print(db.check_user('john@hotmail.com', 'password123'))  # True