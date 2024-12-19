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


class PlanetMenu:
    def __init__(self, width, height):
        self.width = 300  # Fixed width for the menu
        self.height = height
        self.visible = False
        self.current_planet = None
        self.scroll_y = 0
        self.max_scroll = 0
        self.images = {}  # Cache for planet images

    def load_image(self, path):
        if path not in self.images:
            try:
                # Load and scale image to fit menu width
                image = pygame.image.load(path)
                aspect_ratio = image.get_width() / image.get_height()
                new_width = min(self.width - 40, 200)  # Leave some padding
                new_height = int(new_width / aspect_ratio)
                self.images[path] = pygame.transform.scale(image, (new_width, new_height))
            except:
                # Create placeholder if image loading fails
                placeholder = pygame.Surface((200, 200))
                placeholder.fill(Colours.dark_gray)
                self.images[path] = placeholder
        return self.images[path]

    def show(self, planet):
        self.current_planet = planet
        self.visible = True
        self.scroll_y = 0

    def hide(self):
        self.visible = False
        self.current_planet = None

    def handle_event(self, event):
        if not self.visible:
            return False

        if event.type == pygame.MOUSEBUTTONDOWN:
            # Check if click is outside menu
            menu_rect = pygame.Rect(width - self.width, 0, self.width, height)
            if not menu_rect.collidepoint(event.pos):
                self.hide()
                return True

            # Handle scrolling
            if event.button == 4:  # Mouse wheel up
                self.scroll_y = min(0, self.scroll_y + 20)
            elif event.button == 5:  # Mouse wheel down
                self.scroll_y = max(-self.max_scroll, self.scroll_y - 20)

        return True

    def draw(self, surface):
        if not self.visible or not self.current_planet:
            return

        # Create menu surface with transparency
        menu_surface = pygame.Surface((self.width, self.height), pygame.SRCALPHA)
        menu_surface.fill((30, 30, 30, 230))  # Semi-transparent background

        # Calculate content height and update max scroll
        content_height = 0
        y_offset = 20 + self.scroll_y

        # Title
        title_font = pygame.font.SysFont('Arial', 24, bold=True)
        title = title_font.render(self.current_planet.name, True, Colours.white)
        menu_surface.blit(title, (20, y_offset))
        y_offset += 40

        # Planet Image
        image = self.load_image(self.current_planet.image_path)
        menu_surface.blit(image, (20, y_offset))
        y_offset += image.get_height() + 20

        # Information sections
        sections = [
            ("Physical Characteristics", [
                f"Radius: {format(self.current_planet.radius, '.2e')} km",
                f"Mass: {format(self.current_planet.mass, '.2e')} kg"
            ]),
            ("Orbital Properties", [
                f"Distance from Sun: {format(((self.current_planet.start_x)**2 + (self.current_planet.start_y)**2)**0.5 / AU, '.2f')} AU",
                f"Orbital Speed: {format(((self.current_planet.start_vx)**2 + (self.current_planet.start_vy)**2)**0.5 / 1000, '.2f')} km/s"
            ]),
            ("Description", [
                self.current_planet.description
            ])
        ]

        info_font = pygame.font.SysFont('Arial', 16)
        section_font = pygame.font.SysFont('Arial', 18, bold=True)

        for section_title, items in sections:
            # Section title
            section_text = section_font.render(section_title, True, Colours.light_gray)
            menu_surface.blit(section_text, (20, y_offset))
            y_offset += 30

            # Section content
            for item in items:
                # Word wrap long text
                words = item.split()
                line = []
                for word in words:
                    line.append(word)
                    text = ' '.join(line)
                    if info_font.size(text)[0] > self.width - 40:
                        line.pop()
                        text = ' '.join(line)
                        text_surface = info_font.render(text, True, Colours.white)
                        menu_surface.blit(text_surface, (20, y_offset))
                        y_offset += 25
                        line = [word]

                if line:
                    text = ' '.join(line)
                    text_surface = info_font.render(text, True, Colours.white)
                    menu_surface.blit(text_surface, (20, y_offset))
                    y_offset += 25

            y_offset += 20

        # Update max scroll if content is taller than menu
        self.max_scroll = max(0, y_offset - self.height)

        # Draw close button
        close_font = pygame.font.SysFont('Arial', 20)
        close_text = close_font.render('×', True, Colours.white)
        menu_surface.blit(close_text, (self.width - 30, 10))

        # Draw scroll indicators if needed
        if self.max_scroll > 0:
            if self.scroll_y < 0:
                pygame.draw.polygon(menu_surface, Colours.white,
                    [(self.width - 20, 40), (self.width - 10, 40), (self.width - 15, 30)])
            if self.scroll_y > -self.max_scroll:
                pygame.draw.polygon(menu_surface, Colours.white,
                    [(self.width - 20, height - 40), (self.width - 10, height - 40), (self.width - 15, height - 30)])

        # Blit menu to main surface
        surface.blit(menu_surface, (width - self.width, 0))

class DatePicker:
    def __init__(self, callback):
        self.callback = callback
        self.root = None

    def show(self):
        # Run Tkinter window in a separate thread
        thread = threading.Thread(target=self._show_window)
        thread.daemon = True
        thread.start()

    def _show_window(self):
        self.root = Tk()
        self.root.title("Select Date")

        # Center the window
        window_width = 300
        window_height = 250
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        x = (screen_width - window_width) // 2
        y = (screen_height - window_height) // 2
        self.root.geometry(f"{window_width}x{window_height}+{x}+{y}")

        # Style
        style = ttk.Style()
        style.configure('TButton', padding=5)
        style.configure('TLabel', padding=5)

        # Date selection widgets
        frame = ttk.Frame(self.root, padding="10")
        frame.grid(row=0, column=0, sticky=(N, W, E, S))

        # Year
        ttk.Label(frame, text="Year:").grid(row=0, column=0, sticky=W)
        year_var = StringVar(value="2000")
        year_entry = ttk.Entry(frame, textvariable=year_var, width=10)
        year_entry.grid(row=0, column=1, padx=5, pady=5)

        # Month
        ttk.Label(frame, text="Month:").grid(row=1, column=0, sticky=W)
        month_var = StringVar()
        months = list(calendar.month_name)[1:]
        month_combo = ttk.Combobox(frame, textvariable=month_var, values=months, width=10)
        month_combo.set(months[0])
        month_combo.grid(row=1, column=1, padx=5, pady=5)

        # Day
        ttk.Label(frame, text="Day:").grid(row=2, column=0, sticky=W)
        day_var = StringVar(value="1")
        day_entry = ttk.Spinbox(frame, from_=1, to=31, textvariable=day_var, width=5)
        day_entry.grid(row=2, column=1, padx=5, pady=5)

        def submit():
            try:
                year = int(year_var.get())
                month = months.index(month_var.get()) + 1
                day = int(day_var.get())
                date = datetime(year, month, day)
                self.callback(date)
                self.root.destroy()
            except ValueError:
                ttk.Label(frame, text="Invalid date!", foreground="red").grid(row=4, column=0, columnspan=2)

        ttk.Button(frame, text="Set Date", command=submit).grid(row=3, column=0, columnspan=2, pady=20)

        self.root.mainloop()

class Button:
    def __init__(self, text, x, y, icon_path, action=None, tooltip=""):
        self.text = text
        self.x = x
        self.y = y
        self.icon_path = icon_path
        self.action = action
        self.tooltip = tooltip
        self.icon = pygame.image.load(icon_path).convert_alpha()
        self.hovered = False

    def draw(self, window):
        # Draw button background when hovered
        button_rect = self.icon.get_rect(topleft=(self.x, self.y))
        if self.hovered:
            pygame.draw.rect(window, Colours.dark_gray, button_rect)

        window.blit(self.icon, (self.x, self.y))

        # Draw tooltip if hovered
        if self.hovered:
            tooltip_font = pygame.font.SysFont('Arial', 14)
            tooltip_surface = tooltip_font.render(self.tooltip, True, Colours.white)
            tooltip_x = self.x
            tooltip_y = self.y + self.icon.get_height() + 5
            pygame.draw.rect(window, Colours.dark_gray,
                           (tooltip_x, tooltip_y, tooltip_surface.get_width() + 10, tooltip_surface.get_height() + 5))
            window.blit(tooltip_surface, (tooltip_x + 5, tooltip_y + 2))

    def is_clicked(self, pos):
        button_rect = self.icon.get_rect(topleft=(self.x, self.y))
        return button_rect.collidepoint(pos)

    def update_hover(self, pos):
        button_rect = self.icon.get_rect(topleft=(self.x, self.y))
        self.hovered = button_rect.collidepoint(pos)

class Body:
    def __init__(self, id, name, radius, mass, start_x, start_y, start_vx, start_vy, description, colour, image_path):
        self.name = name
        self.radius = float(radius)
        self.mass = float(mass)
        self.start_x = float(start_x)
        self.start_y = float(start_y)
        self.description = description
        self.colour = getattr(Colours, colour.lower())
        self.image_path = image_path
        self.orbital_radius = self.start_x
        self.start_vx = 0
        self.start_vy = (G * 1.989 * 10 ** 30 / (self.start_x)) ** 0.5 if self.start_x else 0

        self.frame_of_reference = False
        self.reset_x = float(start_x)
        self.reset_y = float(start_y)
        self.reset_vx = self.start_vx
        self.reset_vy = self.start_vy
        self.selected = False

    def update(self, bodies, time_step=time_step):
        sun = next(body for body in bodies if body.name == "Sun")

        dx = sun.start_x - self.start_x
        dy = sun.start_y - self.start_y
        distance = (dx**2 + dy**2)**0.5
        if distance == 0:
            return

        force = G * self.mass * sun.mass / distance**2
        theta = math.atan2(dy, dx)
        fx = math.cos(theta) * force
        fy = math.sin(theta) * force

        self.start_vx += fx / self.mass * time_step
        self.start_vy += fy / self.mass * time_step

        self.start_x += self.start_vx * time_step
        self.start_y += self.start_vy * time_step

    def draw(self, frame_of_reference):
        r = max(5, int(self.radius / (scale_factor * 5)))

        x = int((self.start_x - frame_of_reference.start_x) / scale_factor) + width // 2
        y = int((self.start_y - frame_of_reference.start_y) / scale_factor) + height // 2

        # Draw orbit
        pygame.draw.circle(window, self.colour, (width // 2, height // 2),
                         int(self.orbital_radius / scale_factor), 1)

        # Draw selection highlight if selected
        if self.selected:
            pygame.draw.circle(window, Colours.white, (x, y), r + 2)

        # Draw planet
        pygame.draw.circle(window, self.colour, (x, y), r)

        # Draw name and info if selected
        if self.selected:
            # Draw name with larger font
            name_font = pygame.font.SysFont('Arial', 16)
            name_surface = name_font.render(self.name, True, Colours.white)
            window.blit(name_surface, (x + r + 5, y - r - 20))

            # Draw description with smaller font
            desc_font = pygame.font.SysFont('Arial', 12)
            desc_surface = desc_font.render(self.description[:50] + "...", True, Colours.gray)
            window.blit(desc_surface, (x + r + 5, y - r))
        else:
            # Just draw the name with regular font
            name_surface = font.render(self.name, True, Colours.white)
            window.blit(name_surface, (x + r + 2, y - r))

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
        self.epoch = datetime(2000, 1, 1)
        self.bodies = bodies

        # Initialize UI elements
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

        self.speed = 3
        self.speeds = {
            0: {"step": 1/60, "name": "1 frame = 1 second"},
            1: {"step": 1, "name": "1 frame = 1 minute"},
            2: {"step": 60 * 60, "name": "1 frame = 1 hour"},
            3: {"step": 60 * 60 * 24, "name": "1 frame = 1 day"},
            4: {"step": 60 * 60 * 24 * 7, "name": "1 frame = 1 week"}
        }

    def open_settings(self):
        print("Settings opened")

    def open_date_picker(self):
        date_picker = DatePicker(self.set_date)
        date_picker.show()

    def set_date(self, new_date):
        time_diff = new_date - self.epoch
        self.time = time_diff.total_seconds()

    def take_screenshot(self):
        # Create screenshots directory if it doesn't exist
        if not os.path.exists('screenshots'):
            os.makedirs('screenshots')

        # Generate filename with current date and time
        filename = f"screenshots/solar_system_{datetime.now().strftime('%Y%m%d_%H%M%S')}.png"
        pygame.image.save(window, filename)
        print(f"Screenshot saved as {filename}")

    def toggle_running(self):
        self.paused = not self.paused
        if self.paused:
            self.buttons[6].icon = pygame.image.load("icons/play.svg").convert_alpha()
        else:
            self.buttons[6].icon = pygame.image.load("icons/pause.svg").convert_alpha()

    def lower_speed(self):
        self.speed = max(0, self.speed - 1)

    def increase_speed(self):
        self.speed = min(len(self.speeds) - 1, self.speed + 1)

    def restart(self):
        for body in self.bodies:
            body.reset()
        self.time = 0

    def zoom_out(self):
        global scale_factor
        scale_factor *= 1.1

    def zoom_in(self):
        global scale_factor
        scale_factor /= 1.1

    @property
    def date(self):
        return self.epoch + timedelta(seconds=self.time)

    def main(self):
        while self.running:
            mouse_pos = pygame.mouse.get_pos()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                if event.type == MOUSEBUTTONDOWN:
                    # Handle button clicks
                    for button in self.buttons:
                        if button.is_clicked(mouse_pos):
                            button.action()

                    # Handle planet selection
                    frame_of_reference = next((body for body in self.bodies if body.frame_of_reference), None)
                    for body in self.bodies:
                        x = int((body.start_x - frame_of_reference.start_x) / scale_factor) + width // 2
                        y = int((body.start_y - frame_of_reference.start_y) / scale_factor) + height // 2
                        r = max(5, int(body.radius / (scale_factor * 5)))

                        # Check if click is within planet's circle
                        dx = mouse_pos[0] - x
                        dy = mouse_pos[1] - y
                        if dx*dx + dy*dy <= r*r:
                            body.selected = not body.selected
                        else:
                            body.selected = False

            # Update button hover states
            for button in self.buttons:
                button.update_hover(mouse_pos)

            # Clear the screen
            window.fill(Colours.black)

            # Draw UI header background
            pygame.draw.rect(window, Colours.dark_gray, (0, 0, width, 60))

            # Get frame of reference
            frame_of_reference = next((body for body in self.bodies if body.frame_of_reference), None)

            # Draw information panel
            self.draw_info_panel()

            # Update and draw bodies
            bodies_copy = self.bodies.copy()
            for body in self.bodies:
                if not self.paused:
                    body.update(bodies_copy, self.speeds[self.speed]["step"])
                body.draw(frame_of_reference)

            # Draw buttons
            for button in self.buttons:
                button.draw(window)

            # Draw help text
            self.draw_help_text()

            pygame.display.flip()
            self.clock.tick(60)

            if not self.paused:
                self.time += self.speeds[self.speed]["step"]

    def draw_info_panel(self):
        # Draw date and speed info
        large_font = pygame.font.SysFont('Arial', 24)

        # Date display
        date_surface = large_font.render(
            f"Date: {self.date.strftime('%d %b %Y %H:%M:%S')}",
            True,
            Colours.white
        )
        window.blit(date_surface, (width - date_surface.get_width() - 20, 20))

        # Speed display
        speed_surface = large_font.render(
            f"Speed: {self.speeds[self.speed]['name']}",
            True,
            Colours.white
        )
        window.blit(speed_surface, (width - speed_surface.get_width() - 20, 50))

        # Draw selected planet info
        selected_planet = next((body for body in self.bodies if body.selected), None)
        if selected_planet:
            self.draw_selected_planet_info(selected_planet)

    def draw_selected_planet_info(self, planet):
        info_font = pygame.font.SysFont('Arial', 16)
        y_offset = 100
        line_height = 20

        info_items = [
            f"Name: {planet.name}",
            f"Radius: {format(planet.radius, '.2e')} km",
            f"Mass: {format(planet.mass, '.2e')} kg",
            f"Distance from Sun: {format(((planet.start_x)**2 + (planet.start_y)**2)**0.5 / AU, '.2f')} AU",
            f"Orbital Speed: {format(((planet.start_vx)**2 + (planet.start_vy)**2)**0.5 / 1000, '.2f')} km/s"
        ]

        # Draw semi-transparent background
        info_width = 300
        info_height = len(info_items) * line_height + 20
        info_surface = pygame.Surface((info_width, info_height))
        info_surface.set_alpha(128)
        info_surface.fill(Colours.dark_gray)
        window.blit(info_surface, (10, y_offset - 10))

        # Draw text
        for i, text in enumerate(info_items):
            text_surface = info_font.render(text, True, Colours.white)
            window.blit(text_surface, (20, y_offset + i * line_height))

    def draw_help_text(self):
        help_font = pygame.font.SysFont('Arial', 14)
        help_text = [
            "Controls:",
            "Click on planets to select them",
            "Use mouse wheel to zoom",
            "Space to pause/play",
            "Press R to reset"
        ]

        y_offset = height - len(help_text) * 20 - 10
        for i, text in enumerate(help_text):
            text_surface = help_font.render(text, True, Colours.gray)
            window.blit(text_surface, (10, y_offset + i * 20))


def load_planets_from_csv(filename):
    """Load planet data from CSV file"""
    import csv
    planets = []

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
    return planets


if __name__ == "__main__":
    # Load planets from CSV
    planets = load_planets_from_csv('Planets Data.csv')

    # Set Sun as the frame of reference
    for planet in planets:
        if planet.name == "Sun":
            planet.frame_of_reference = True
            break

    # Initialize and run simulator
    sim = Simulator(planets)
    sim.main()