import pygame
from pygame.locals import *
import sqlite3
import datetime

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


class Button:
    def __init__(self, text, x, y, icon_path, action=None):
        self.text = text
        self.x = x
        self.y = y
        self.icon_path = icon_path
        self.action = action
        self.icon = pygame.image.load(icon_path).convert_alpha()

    def draw(self, window):
        window.blit(self.icon, (self.x, self.y))

    def is_clicked(self, pos):
        button_rect = self.icon.get_rect(topleft=(self.x, self.y))
        return button_rect.collidepoint(pos)

# Define functions for each button action
def play():
    print("Play simulation")

def pause():
    print("Pause simulation")

def restart():
    print("Restart simulation")

def slow_down():
    print("Slow down simulation")

def speed_up():
    print("Speed up simulation")

def open_settings():
    print("Open settings")

def share():
    print("Share simulation")

# Create buttons with icons


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
        self.reset_x = start_x
        self.reset_y = start_y
        self.reset_vx = start_vx
        self.reset_vy = start_vy

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

    def update(self, all_bodies: list, time_step=time_step):
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

    def reset(self):
        self.start_x = self.reset_x
        self.start_y = self.reset_y
        self.start_vx = self.reset_vx
        self.start_vy = self.reset_vy

class Simulator:
    def __init__(self, bodies=[]):
        self.running = True
        self.paused = False
        self.clock = pygame.time.Clock()
        self.time = 0
        self.epoch = datetime.datetime(2000, 1, 1)
        self.bodies = bodies
        # Preload the play button icon
        pygame.image.load(f"icons/play.svg").convert_alpha()
        middle = width // 2
        self.buttons = [
            Button("Settings", 20, 20, "icons/settings.svg", open_settings),
            Button("Restart", 100, 20, "icons/restart.svg", self.restart),
            Button("Slow Down", middle - 80, 20, "icons/slow_down.svg", self.lower_speed),
            Button("Play", middle, 20, f"icons/pause.svg", self.toggle_running),
            Button("Speed Up", middle + 80, 20, "icons/speed_up.svg", self.increase_speed),
            Button("Share", width - 320, 20, "icons/share.svg", share)
        ]
        self.speed = 3
        self.speeds = {
            0: { "step": 1/60, "name": "1 frame = 1 second" },
            1: { "step": 1, "name": "1 frame = 1 minute" },
            2: { "step": 60 * 60, "name": "1 frame = 1 hour" },
            3: { "step": 60 * 60 * 24, "name": "1 frame = 1 day" },
            4: { "step": 60 * 60 * 24 * 7, "name": "1 frame = 1 week" },
        }

    def toggle_running(self):
        self.paused = not self.paused
        # Update the play/pause button icon
        if self.paused:
            self.buttons[3].icon = pygame.image.load(f"icons/play.svg").convert_alpha()
        else:
            self.buttons[3].icon = pygame.image.load(f"icons/pause.svg").convert_alpha()

    def lower_speed(self):
        self.speed = max(0, self.speed - 1)

    def increase_speed(self):
        self.speed = min(4, self.speed + 1)

    def restart(self):
        for body in self.bodies:
            body.reset()
        self.time = 0

    @property
    def date(self):
        return self.epoch + datetime.timedelta(seconds=self.time)

    def run(self):
        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                if event.type == MOUSEBUTTONDOWN:
                    pos = pygame.mouse.get_pos()
                    for button in self.buttons:
                        if button.is_clicked(pos):
                            button.action()

            window.fill(Colours.black)
            frame_of_reference = None
            for body in self.bodies:
                if body.frame_of_reference:
                    frame_of_reference = body
                    break

            # Draw buttons
            for button in self.buttons:
                button.draw(window)

            # Add a text display for the current date
            large_font = pygame.font.SysFont('Arial', 24)  # Larger font for the date
            date_surface = large_font.render(f"{self.date.strftime('%d/%m/%Y at %H:%M:%S')}", True, Colours.white)
            window.blit(date_surface, (width - date_surface.get_width() - 20, 20))
            # On the next line, add a text display for the current speed
            speed_surface = large_font.render(f"Speed: {self.speeds[self.speed]['name']}", True, Colours.white)
            window.blit(speed_surface, (width - speed_surface.get_width() - 20, 50))

            bodies_copy = self.bodies.copy()  # Create a copy of the list to avoid modifying it while iterating
            for body in self.bodies:
                if not self.paused:
                    body.update(bodies_copy, self.speeds[self.speed]["step"])
                body.draw(frame_of_reference)

            pygame.display.flip()  # Update the display
            self.clock.tick(60)  # Run at 60 FPS

            if not self.paused:
                self.time += self.speeds[self.speed]["step"]

# Assign planets to variables using databse
cursor.execute("SELECT * FROM Planets")
planets = cursor.fetchall()
sun, mercury, venus, earth, mars, jupiter, saturn, uranus, neptune = [Body(*planet) for planet in planets]


if __name__ == "__main__":
    sun.frame_of_reference = True
    sim = Simulator([sun, mercury, venus, earth, mars, jupiter, saturn, uranus, neptune])
    sim.run()
