import sqlite3

class SimulationDatabase:
    def __init__(self):
        self.conn = sqlite3.connect('database.db')
        self.cursor = self.conn.cursor()

    def create_categories_table(self):
        # Create Categories table first
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS Categories (
                            id INTEGER PRIMARY KEY AUTOINCREMENT,
                            name TEXT NOT NULL);''')
        self.conn.commit()

    def create_simulations_table(self):
        # Create Simulations table, referencing the Categories table
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS Simulations (
                            id INTEGER PRIMARY KEY AUTOINCREMENT,
                            title TEXT NOT NULL,
                            description TEXT NOT NULL,
                            file_path TEXT NOT NULL,
                            category_id INTEGER,
                            FOREIGN KEY (category_id) REFERENCES Categories(id));''')
        self.conn.commit()

    def add_simulation(self, title, description, file_path, category_id):
        # Fixed method to add a simulation to the Simulations table
        self.cursor.execute("INSERT INTO Simulations (title, description, file_path, category_id) VALUES (?, ?, ?, ?)",
                            (title, description, file_path, category_id))
        self.conn.commit()

    def get_simulations(self, category_id):
        # Get simulations based on category
        self.cursor.execute("SELECT * FROM Simulations WHERE category_id=?", (category_id,))
        return self.cursor.fetchall()

    def get_categories(self):
        # Get all categories from the Categories table
        self.cursor.execute("SELECT name FROM Categories")
        return [category[0] for category in self.cursor.fetchall()]

    def add_category(self, name):
        # Add a new category to the Categories table
        self.cursor.execute("INSERT INTO Categories (name) VALUES (?)", (name,))
        self.conn.commit()

    def search_simulations(self, search_query):
        # Search for simulations based on title
        self.cursor.execute("SELECT * FROM Simulations WHERE title LIKE ?", (f"%{search_query}%",))
        return self.cursor.fetchall()

    def close_connection(self):
        # Close the database connection
        self.cursor.close()
        self.conn.close()

def main():
    # Initialize and create tables
    db = SimulationDatabase()
    db.create_categories_table()
    db.create_simulations_table()

    # Example usage
    db.add_category('Kinematics')
    db.add_simulation('Projectile Motion Sim', 'Simulates the motion of a projectile under gravity.', '/path/to/projectile_sim', 1)
    print(db.get_simulations(1))
    print(db.search_simulations('Projectile'))

    # Close the database connection
    db.close_connection()

if __name__ == '__main__':
    main()
