import pygame
import sqlite3

# Initialize Pygame
pygame.init()

# Set up display
width, height = 1200, 800
window = pygame.display.set_mode((width, height))
pygame.display.set_caption("Solar System Simulator")

# Connect to the database
conn = sqlite3.connect('database.db')
cursor = conn.cursor()

# Constants
G = 6.67430 * 10 ** -11  # Gravitational constant
AU = 1.496 * 10 ** 11  # Astronomical unit
scale_factor = 5 * 10 ** 9  # Scaling factor for the solar system to fit on screen
time_step = 60 * 60 * 24  # Time step in seconds (1 day per update)
font = pygame.font.SysFont('Arial', 12)  # Font for planet names

class Colours:
    red = (255, 0, 0)
    green = (0, 255, 0)
    blue = (0, 0, 255)
    yellow = (255, 255, 0)
    white = (255, 255, 255)
    black = (0, 0, 0)
    cyan = (0, 255, 255)
    magenta = (255, 0, 255)
    gray = (128, 128, 128)
    orange = (255, 165, 0)

class Body:
    def __init__(self, id, name, radius, mass, start_x, start_y, start_vx, start_vy, description, colour, image_path):
        self.name = name
        self.radius = radius
        self.mass = mass
        self.start_x = start_x
        self.start_y = start_y
        self.start_vx = start_vx
        self.start_vy = start_vy
        self.description = description
        self.colour = colour
        self.image_path = image_path
        self.frame_of_reference = False

    def draw(self, frame_of_reference):
        # Shrink planet sizes so they don’t overlap as much
        r = max(5, int(self.radius / (scale_factor * 5)))  # Adjusted to a smaller size for less overlap

        # Calculate the position based on the frame of reference
        x = int((self.start_x - frame_of_reference.start_x) / scale_factor) + width // 2
        y = int((self.start_y - frame_of_reference.start_y) / scale_factor) + height // 2

        # Draw planet
        pygame.draw.circle(window, self.colour, (x, y), r)

        # Draw planet name
        name_surface = font.render(self.name, True, Colours.white)
        window.blit(name_surface, (x + r + 2, y - r))  # Position the name next to the planet

    def update(self, all_bodies: list):
        # Reset forces to 0
        force_x = 0
        force_y = 0

        for body in all_bodies:
            if body.name != self.name:
                dx = body.start_x - self.start_x
                dy = body.start_y - self.start_y
                distance_squared = dx**2 + dy**2
                distance = distance_squared ** 0.5

                if distance == 0:
                    continue  # Avoid division by zero

                # Calculate the force due to gravity (F = GMm/r^2)
                force = G * self.mass * body.mass / distance_squared

                # Break down the force into components
                force_x += force * (dx / distance)
                force_y += force * (dy / distance)

        # Calculate acceleration (F = ma -> a = F/m)
        acceleration_x = force_x / self.mass
        acceleration_y = force_y / self.mass

        # Update velocity (v = u + at)
        self.start_vx += acceleration_x * time_step
        self.start_vy += acceleration_y * time_step

        # Update position (s = s + v * t)
        self.start_x += self.start_vx * time_step
        self.start_y += self.start_vy * time_step

class Simulator:
    def __init__(self, bodies=[]):
        self.running = True
        self.clock = pygame.time.Clock()
        self.time = 0
        self.bodies = bodies

    def run(self):
        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False

            window.fill(Colours.black)
            frame_of_reference = None
            for body in self.bodies:
                if body.frame_of_reference:
                    frame_of_reference = body
                    break

            bodies_copy = self.bodies.copy()  # Create a copy of the list to avoid modifying it while iterating
            for body in self.bodies:
                body.update(bodies_copy)
                body.draw(frame_of_reference)

            pygame.display.flip()  # Update the display
            self.clock.tick(60)  # Run at 60 FPS


# Assign planets to variables using databse
cursor.execute("SELECT * FROM Planets")
planets = cursor.fetchall()
sun, mercury, venus, earth, mars, jupiter, saturn, uranus, neptune = [Body(*planet) for planet in planets]


if __name__ == "__main__":
    sun.frame_of_reference = True
    sim = Simulator([sun, mercury, venus, earth, mars, jupiter, saturn, uranus, neptune])
    sim.run()
