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
                            start_vx REAL NOT NULL,
                            start_vy REAL NOT NULL,
                            description TEXT,
                            colour TEXT NOT NULL,
                            image_path TEXT NOT NULL);''')
        self.conn.commit()

    def add_planet(self, name, radius, mass, start_x, start_y, start_vx, start_vy, description, colour, image_path):
        # Add a planet to the Planets table
        self.cursor.execute('''INSERT INTO Planets (name, radius, mass, start_x, start_y, start_vx, start_vy, description, colour, image_path)
                            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)''',
                            (name, radius, mass, start_x, start_y, start_vx, start_vy, description, colour, image_path))
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
    # db.add_planet('Sun', 696340, 1.989 * 10**30, 0, 0, 0, 0, 'The Sun is the star at the center of the Solar System.', 'yellow', 'planet_images/sun.png')
    AU = 1.496 * 10 ** 11  # Astronomical unit
    # Add planets to the database
    db.add_planet('Sun', 696340, 1.989 * 10**30, 0, 0, 0, 0, 'The Sun is the star at the center of the Solar System.', 'yellow', 'planet_images/sun.png')
    db.add_planet('Mercury', 2439.7, 3.285 * 10**23, 0.39 * AU, 0, 0, 47400, 'Mercury is the smallest and innermost planet in the Solar System.', 'gray', 'planet_images/mercury.png')
    db.add_planet('Venus', 6051.8, 4.867 * 10**24, 0.72 * AU, 0, 0, 35020, 'Venus is the second planet from the Sun and has a thick, toxic atmosphere.', 'orange', 'planet_images/venus.png')
    db.add_planet('Earth', 6371, 5.972 * 10**24, 1 * AU, 0, 0, 30000, 'The Earth is the third planet from the Sun.', 'blue', 'planet_images/earth.png')
    db.add_planet('Mars', 3389.5, 6.39 * 10**23, 1.52 * AU, 0, 0, 24077, 'Mars is the fourth planet from the Sun and is known as the Red Planet.', 'red', 'planet_images/mars.png')
    db.add_planet('Jupiter', 69911, 1.898 * 10**27, 5.2 * AU, 0, 0, 13070, 'Jupiter is the largest planet in the Solar System and has a strong magnetic field.', 'orange', 'planet_images/jupiter.png')
    db.add_planet('Saturn', 58232, 5.683 * 10**26, 9.58 * AU, 0, 0, 9680, 'Saturn is famous for its prominent ring system.', 'yellow', 'planet_images/saturn.png')
    db.add_planet('Uranus', 25362, 8.681 * 10**25, 19.2 * AU, 0, 0, 6800, 'Uranus is the seventh planet and has a unique sideways rotation.', 'cyan', 'planet_images/uranus.png')
    db.add_planet('Neptune', 24622, 1.024 * 10**26, 30.05 * AU, 0, 0, 5430, 'Neptune is the farthest planet from the Sun and has strong winds.', 'blue', 'planet_images/neptune.png')

    # Print all planets
    print(db.get_planets())

    # Search for planets
    print(db.search_planets('Earth'))

    # Close the database connection
    db.close_connection()

if __name__ == '__main__':
    main()
