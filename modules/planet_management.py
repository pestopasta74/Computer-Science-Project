# Assuming that the simulation starts on 1st January 2000, 00:00:00 UTC
# The database will store the planets' name, radius, mass, starting x and y coordinates, description, colour, and image path

import sqlite3

class SimulationDatabase:
    def __init__(self):
        self.conn = sqlite3.connect('database.db')
        self.cursor = self.conn.cursor()

    def create_planets_table(self):
        # Create a Planets table with the specified columns
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS Planets (
                            id INTEGER PRIMARY KEY AUTOINCREMENT,
                            name TEXT NOT NULL,
                            radius REAL NOT NULL,
                            mass REAL NOT NULL,
                            start_x REAL NOT NULL,
                            start_y REAL NOT NULL,
                            description TEXT,
                            colour TEXT NOT NULL,
                            image_path TEXT NOT NULL);''')
        self.conn.commit()

    def add_planet(self, name, radius, mass, start_x, start_y, description, colour, image_path):
        # Add a planet to the Planets table
        self.cursor.execute('''INSERT INTO Planets (name, radius, mass, start_x, start_y, description, colour, image_path)
                            VALUES (?, ?, ?, ?, ?, ?, ?, ?)''',
                            (name, radius, mass, start_x, start_y, description, colour, image_path))
        self.conn.commit()

    def get_planets(self):
        # Get all planets from the Planets table
        self.cursor.execute("SELECT * FROM Planets")
        return self.cursor.fetchall()

    def search_planets(self, search_query):
        # Search for planets based on name
        self.cursor.execute("SELECT * FROM Planets WHERE name LIKE ?", (f"%{search_query}%",))
        return self.cursor.fetchall()

    def close_connection(self):
        # Close the database connection
        self.cursor.close()
        self.conn.close()

def main():
    # Initialize and create the planets table
    db = SimulationDatabase()
    db.create_planets_table()

    # Example usage: Adding a planet
    db.add_planet('Sun', 696340, 1.989 * 10**30, 0, 0, 'The Sun is the star at the center of the Solar System.', 'yellow', 'planet_images/sun.png')

    # Print all planets
    print(db.get_planets())

    # Search for planets
    print(db.search_planets('Earth'))

    # Close the database connection
    db.close_connection()

if __name__ == '__main__':
    main()
