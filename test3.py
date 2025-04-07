import pygame
from pygame.locals import *
import sqlite3
import datetime
import math
from datetime import datetime, timedelta
import json
import os
from tkinter import *
from tkinter import ttk
import calendar
import threading
from settings import SettingsManager

# Initialize Pygame
pygame.init()

# Set up display
width, height = 1200, 800
window = pygame.display.set_mode((width, height))
pygame.display.set_caption("Solar System Simulator")

# Constants
G = 6.67430 * 10 ** -11  # Gravitational constant
AU = 1.496 * 10 ** 11  # Astronomical unit
scale_factor = 5 * 10 ** 9  # Scaling factor for the solar system
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
    dark_gray = (50, 50, 50)
    light_gray = (192, 192, 192)  # Added missing light_gray color

class Body:
    def __init__(self, id, name, radius, mass, start_x, start_y, start_vx, start_vy, description, colour, image_path):
        self.id = id
        self.name = name
        self.radius = float(radius)
        self.mass = float(mass)
        self.start_x = float(start_x)
        self.start_y = float(start_y)
        self.description = description
        self.colour = getattr(Colours, colour.lower())
        self.image_path = image_path
        self.orbital_radius = math.sqrt(start_x**2 + start_y**2)  # Fixed orbital radius calculation

        # Initialize velocities correctly
        self.start_vx = float(start_vx)  # Use provided start_vx
        self.start_vy = float(start_vy)  # Use provided start_vy

        self.frame_of_reference = False
        self.reset_x = float(start_x)
        self.reset_y = float(start_y)
        self.reset_vx = self.start_vx
        self.reset_vy = self.start_vy
        self.selected = False

    def update(self, bodies, time_step=time_step):
        if self.name == "Sun":  # Skip update for Sun
            return

        total_fx = 0
        total_fy = 0

        # Calculate gravitational forces from all other bodies
        for other in bodies:
            if other != self:
                dx = other.start_x - self.start_x
                dy = other.start_y - self.start_y
                distance = math.sqrt(dx**2 + dy**2)

                if distance < 1e-10:  # Prevent division by zero
                    continue

                force = G * self.mass * other.mass / (distance**2)
                theta = math.atan2(dy, dx)
                total_fx += math.cos(theta) * force
                total_fy += math.sin(theta) * force

        # Update velocities
        self.start_vx += (total_fx / self.mass) * time_step
        self.start_vy += (total_fy / self.mass) * time_step

        # Update positions
        self.start_x += self.start_vx * time_step
        self.start_y += self.start_vy * time_step

    def draw(self, frame_of_reference):
        # Calculate relative position
        rel_x = self.start_x - frame_of_reference.start_x
        rel_y = self.start_y - frame_of_reference.start_y

        # Scale positions to screen coordinates
        screen_x = int(rel_x / scale_factor) + width // 2
        screen_y = int(rel_y / scale_factor) + height // 2

        # Calculate scaled radius (minimum 5 pixels)
        radius = max(5, int(self.radius / (scale_factor * 5)))

        # Draw orbit circle (only for non-Sun bodies)
        if self.name != "Sun":
            orbit_radius = int(self.orbital_radius / scale_factor)
            pygame.draw.circle(window, self.colour, (width // 2, height // 2), orbit_radius, 1)

        # Draw selection highlight
        if self.selected:
            pygame.draw.circle(window, Colours.white, (screen_x, screen_y), radius + 2)

        # Draw planet
        pygame.draw.circle(window, self.colour, (screen_x, screen_y), radius)

        # Draw labels
        if self.selected:
            name_font = pygame.font.SysFont('Arial', 16)
            name_surface = name_font.render(self.name, True, Colours.white)
            window.blit(name_surface, (screen_x + radius + 5, screen_y - radius - 20))

            desc_font = pygame.font.SysFont('Arial', 12)
            desc_text = self.description[:50] + "..." if len(self.description) > 50 else self.description
            desc_surface = desc_font.render(desc_text, True, Colours.gray)
            window.blit(desc_surface, (screen_x + radius + 5, screen_y - radius))
        else:
            name_surface = font.render(self.name, True, Colours.white)
            window.blit(name_surface, (screen_x + radius + 2, screen_y - radius))

    def reset(self):
        self.start_x = self.reset_x
        self.start_y = self.reset_y
        self.start_vx = self.reset_vx
        self.start_vy = self.reset_vy

class Button:
    def __init__(self, text, x, y, icon_path, action=None, tooltip=""):
        self.text = text
        self.x = x
        self.y = y
        self.action = action
        self.tooltip = tooltip
        try:
            self.icon = pygame.image.load(icon_path).convert_alpha()
        except pygame.error:
            # Create fallback surface if icon loading fails
            self.icon = pygame.Surface((32, 32))
            self.icon.fill(Colours.gray)
        self.hovered = False

    def draw(self, window):
        button_rect = self.icon.get_rect(topleft=(self.x, self.y))
        if self.hovered:
            pygame.draw.rect(window, Colours.dark_gray, button_rect)

        window.blit(self.icon, (self.x, self.y))

        if self.hovered and self.tooltip:
            self.draw_tooltip(window)

    def draw_tooltip(self, window):
        tooltip_font = pygame.font.SysFont('Arial', 14)
        tooltip_surface = tooltip_font.render(self.tooltip, True, Colours.white)
        tooltip_x = self.x
        tooltip_y = self.y + self.icon.get_height() + 5

        # Draw tooltip background
        padding = 5
        tooltip_rect = pygame.Rect(
            tooltip_x,
            tooltip_y,
            tooltip_surface.get_width() + padding * 2,
            tooltip_surface.get_height() + padding * 2
        )
        pygame.draw.rect(window, Colours.dark_gray, tooltip_rect)

        # Draw tooltip text
        window.blit(tooltip_surface, (tooltip_x + padding, tooltip_y + padding))

    def is_clicked(self, pos):
        return self.icon.get_rect(topleft=(self.x, self.y)).collidepoint(pos)

    def update_hover(self, pos):
        self.hovered = self.icon.get_rect(topleft=(self.x, self.y)).collidepoint(pos)

class Simulator:
    def __init__(self, bodies=[]):
        self.running = True
        self.paused = False
        self.clock = pygame.time.Clock()
        self.time = 0
        self.settings = SettingsManager()
        self.epoch = datetime(2000, 1, 1)
        self.bodies = bodies
        self.initialize_buttons()
        self.initialize_speeds()

    def initialize_buttons(self):
        middle = width // 2
        self.buttons = [
            Button("Settings", 20, 20, "icons/settings.svg", self.open_settings, "Open Settings"),
            Button("Restart", 70, 20, "icons/restart.svg", self.restart, "Restart Simulation"),
            Button("Zoom out", 120, 20, "icons/zoom_out.svg", self.zoom_out, "Zoom Out"),
            Button("Zoom in", 170, 20, "icons/zoom_in.svg", self.zoom_in, "Zoom In"),
            Button("Date", 220, 20, "icons/calendar.svg", self.open_date_picker, "Set Simulation Date"),
            Button("Slow Down", middle - 80, 20, "icons/slow_down.svg", self.lower_speed, "Decrease Speed"),
            Button("Play", middle, 20, "icons/pause.svg", self.toggle_running, "Play/Pause"),
            Button("Speed Up", middle + 80, 20, "icons/speed_up.svg", self.increase_speed, "Increase Speed"),
            Button("Share", width - 70, 20, "icons/share.svg", self.take_screenshot, "Take Screenshot")
        ]

    def open_settings(self):
        self.settings.show()

    def initialize_speeds(self):
        self.speed = 3
        self.speeds = {
            0: {"step": 1/60, "name": "1 frame = 1 second"},
            1: {"step": 1, "name": "1 frame = 1 minute"},
            2: {"step": 60 * 60, "name": "1 frame = 1 hour"},
            3: {"step": 60 * 60 * 24, "name": "1 frame = 1 day"},
            4: {"step": 60 * 60 * 24 * 7, "name": "1 frame = 1 week"}
        }

    def handle_events(self):
        mouse_pos = pygame.mouse.get_pos()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == MOUSEBUTTONDOWN:
                self.handle_mouse_click(event.pos)
            elif event.type == KEYDOWN:
                self.handle_keyboard_input(event.key)

        # Update button hover states
        for button in self.buttons:
            button.update_hover(mouse_pos)

    def handle_mouse_click(self, pos):
        # Handle button clicks
        for button in self.buttons:
            if button.is_clicked(pos):
                button.action()
                return

        # Handle planet selection
        frame_of_reference = self.get_frame_of_reference()
        for body in self.bodies:
            screen_pos = self.get_screen_position(body, frame_of_reference)
            radius = max(5, int(body.radius / (scale_factor * 5)))

            # Check if click is within planet's circle
            dx = pos[0] - screen_pos[0]
            dy = pos[1] - screen_pos[1]
            if dx*dx + dy*dy <= radius*radius:
                body.selected = not body.selected
            else:
                body.selected = False

    def handle_keyboard_input(self, key):
        if key == K_SPACE:
            self.toggle_running()
        elif key == K_r:
            self.restart()

    def get_screen_position(self, body, frame_of_reference):
        rel_x = body.start_x - frame_of_reference.start_x
        rel_y = body.start_y - frame_of_reference.start_y
        screen_x = int(rel_x / scale_factor) + width // 2
        screen_y = int(rel_y / scale_factor) + height // 2
        return (screen_x, screen_y)

    def get_frame_of_reference(self):
        return next((body for body in self.bodies if body.frame_of_reference), self.bodies[0])

    def main(self):
        while self.running:
            self.handle_events()
            self.update()
            self.draw()
            self.clock.tick(60)

    def update(self):
        if not self.paused:
            bodies_copy = self.bodies.copy()
            for body in self.bodies:
                body.update(bodies_copy, self.speeds[self.speed]["step"])
            self.time += self.speeds[self.speed]["step"]

    def draw(self):
        # Clear screen
        window.fill(Colours.black)

        # Draw UI header
        pygame.draw.rect(window, Colours.dark_gray, (0, 0, width, 60))

        # Draw bodies
        frame_of_reference = self.get_frame_of_reference()
        for body in self.bodies:
            body.draw(frame_of_reference)

        # Draw UI elements
        self.draw_info_panel()
        for button in self.buttons:
            button.draw(window)
        self.draw_help_text()

        pygame.display.flip()

    # ... [rest of the Simulator class methods remain the same]

def load_planets_from_csv(filename):
    """Load planet data from CSV file"""
    import csv
    planets = []

    try:
        with open(filename, 'r') as file:
            reader = csv.DictReader(file)
            for row in reader:
                planets.append(Body(
                    id=int(row['id']),
                    name=row['name'],
                    radius=float(row['radius']),
                    mass=float(row['mass']),
                    start_x=float(row['start_x']),
                    start_y=float(row['start_y']),
                    start_vx=float(row['start_vx']),
                    start_vy=float(row['start_vy']),
                    description=row['description'],
                    colour=row['colour'],
                    image_path=row['image_path']
                ))
    except FileNotFoundError:
        print(f"Error: Could not find {filename}")
        return []
    except (ValueError, KeyError) as e:
        print(f"Error reading planet data: {e}")
        return []

    return planets

if __name__ == "__main__":
    # Load planets from CSV
    planets = load_planets_from_csv('Planets Data.csv')

    if not planets:
        print("Failed to load planets. Exiting...")
        pygame.quit()
        exit()

    # Set Sun as the frame of reference
    for planet in planets:
        if planet.name == "Sun":
            planet.frame_of_reference = True
            break

    # Initialize and run simulator
    sim = Simulator(planets)
    try:
        sim.main()
    finally:
        pygame.quit()