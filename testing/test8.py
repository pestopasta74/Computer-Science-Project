import pygame
from pygame.locals import *
import sqlite3
import datetime
import math

# Initialize Pygame
pygame.init()

# Set up display
width, height = 1200, 800
window = pygame.display.set_mode((width, height))
pygame.display.set_caption("Solar System Simulator")

# Connect to the database
conn = sqlite3.connect('database.db')
cursor = conn.cursor()

# Physical constants
G = 6.67430 * 10 ** -11  # Universal gravitational constant (m³ kg⁻¹ s⁻²)
AU = 149597871000  # Astronomical unit in meters (1 AU = mean Earth-Sun distance)
scale_factor = 5 * 10 ** 9  # Visual scaling factor to fit planets on screen
time_step = 60 * 60 * 24  # Simulation time step in seconds (1 day per update)
font = pygame.font.SysFont('Arial', 12)

class Colours:
    """Define standard colors for the simulation"""
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
    """
    Represents a celestial body (planet or star) in the solar system.
    
    Attributes:
        name (str): Name of the celestial body
        radius (float): Physical radius of the body
        mass (float): Mass of the body
        a (float): Semi-major axis of orbit in AU
        ec (float): Orbital eccentricity
        description (str): Description of the body
        colour (tuple): RGB color for visualization
        image_path (str): Path to body's texture image
        Ma (float): Mean anomaly at epoch (degrees)
        Mb (float): Mean motion (degrees per day)
    """
    
    def __init__(self, id, name, radius, mass, a, ec, start_vx, start_vy, description, colour, image_path):
        """Initialize celestial body with its physical and orbital parameters"""
        self.name = name
        self.radius = radius
        self.mass = mass
        self.a = a  # Semi-major axis
        self.ec = ec  # Eccentricity
        self.description = description
        self.colour = colour
        self.image_path = image_path
        
        # Calculate semi-minor axis using the relationship b = a * sqrt(1-e²)
        self.b = self.calc_semi_minor_axis(self.a, self.ec)
        
        # Initialize position coordinates
        self.start_x = 0
        self.start_y = 0
        
        # Orbital parameters
        self.frame_of_reference = False
        self.Ma = 0  # Mean anomaly at epoch (will be set later)
        self.Mb = 0  # Mean motion (will be set later)
        
        # Calculate initial position
        self.update_position(0)
        
        # Store initial positions for reset functionality
        self.reset_x = self.start_x
        self.reset_y = self.start_y
    
    def calc_semi_minor_axis(self, a, ec):
        """
        Calculate the semi-minor axis of the orbital ellipse.
        
        Args:
            a (float): Semi-major axis
            ec (float): Eccentricity
            
        Returns:
            float: Semi-minor axis length
        """
        return a * math.sqrt(1 - ec**2)
    
    def calc_days_since_epoch(self, current_date):
        """
        Calculate days since January 1st, 2000 (J2000 epoch).
        Uses the formula from provided documentation.
        
        Args:
            current_date (datetime): Date to calculate days since epoch
            
        Returns:
            int: Number of days since J2000 epoch
        """
        y = current_date.year
        m = current_date.month
        D = current_date.day
        
        # Formula from documentation section 2.7.1.2
        d = (367 * y - 
             7 * (y + (m + 9) // 12) // 4 - 
             3 * ((y + (m - 9) // 7) // 100 + 1) // 4 + 
             275 * m // 9 + 
             D - 730515)
        return d
    
    def normalize_angle(self, angle):
        """
        Normalize an angle to be within 0-360 degrees.
        
        Args:
            angle (float): Angle in degrees
            
        Returns:
            float: Normalized angle between 0 and 360 degrees
        """
        return angle - (angle // 360) * 360
    
    def calc_mean_anomaly(self, days):
        """
        Calculate the mean anomaly for a given number of days since epoch.
        M = Ma + (Mb * d) where Ma is the mean anomaly at epoch and Mb is the mean motion.
        
        Args:
            days (float): Days since J2000 epoch
            
        Returns:
            float: Mean anomaly in degrees
        """
        M = self.Ma + (self.Mb * days)
        return self.normalize_angle(M)
    
    def update_position(self, days):
        """
        Update the body's position based on its orbital parameters.
        Uses the mean anomaly to calculate position on the elliptical orbit.
        
        Args:
            days (float): Days since J2000 epoch
        """
        if self.name == "Sun":
            self.start_x = 0
            self.start_y = 0
            return
            
        M = self.calc_mean_anomaly(days)
        M_rad = math.radians(M)
        
        # Calculate position using parametric form of ellipse
        self.start_x = self.a * math.cos(M_rad)
        self.start_y = self.b * math.sin(M_rad)
    
    def update(self, bodies, time_step=time_step):
        """
        Update body's position based on simulation time.
        
        Args:
            bodies (list): List of all bodies in simulation
            time_step (float): Time step in seconds
        """
        current_date = datetime.datetime(2000, 1, 1) + datetime.timedelta(seconds=time_step)
        days = self.calc_days_since_epoch(current_date)
        self.update_position(days)
    
    def draw(self, frame_of_reference):
        """
        Draw the body and its orbit on the display.
        
        Args:
            frame_of_reference (Body): Body to use as the center of the view
        """
        # Scale radius for display (minimum 5 pixels for visibility)
        r = max(5, int(self.radius / (scale_factor * 5)))
        
        # Calculate screen coordinates
        x = int((self.start_x - frame_of_reference.start_x) / scale_factor) + width // 2
        y = int((self.start_y - frame_of_reference.start_y) / scale_factor) + height // 2
        
        # Draw planet
        pygame.draw.circle(window, self.colour, (x, y), r)
        
        # Draw name label
        name_surface = font.render(self.name, True, Colours.white)
        window.blit(name_surface, (x + r + 2, y - r))
        
        # Draw orbital ellipse (except for the Sun)
        if self.name != "Sun":
            pygame.draw.ellipse(window, self.colour, 
                              (width//2 - int(self.a/scale_factor),
                               height//2 - int(self.b/scale_factor),
                               int(2*self.a/scale_factor),
                               int(2*self.b/scale_factor)), 
                              1)
    
    def reset(self):
        """Reset the body to its initial position"""
        self.start_x = self.reset_x
        self.start_y = self.reset_y

# Orbital parameters from documentation
# Ma: Mean anomaly at epoch (degrees)
# Mb: Mean motion (degrees per day)
# These values can be obtained from:
# 1. NASA JPL HORIZONS system (https://ssd.jpl.nasa.gov/horizons/app.html)
# 2. IAU Minor Planet Center (https://minorplanetcenter.net/data)
# 3. ESA Near-Earth Object Coordination Centre (https://neo.ssa.esa.int/)
ORBITAL_PARAMS = {
    "Mercury": {"Ma": 168.6562, "Mb": 4.0923344368},
    "Venus": {"Ma": 48.0052, "Mb": 1.6021302244},
    "Earth": {"Ma": 356.0470, "Mb": 0.9856002585},
    "Mars": {"Ma": 18.6021, "Mb": 0.5240207766},
    "Jupiter": {"Ma": 19.8950, "Mb": 0.0830853001},
    "Saturn": {"Ma": 316.9670, "Mb": 0.0334442282},
    "Uranus": {"Ma": 142.5905, "Mb": 0.011725806},
    "Neptune": {"Ma": 260.2471, "Mb": 0.005995147},
    "Sun": {"Ma": 0, "Mb": 0}
}

# [Previous code remains the same until the Simulator class]

class Button:
    """
    Represents a clickable button in the simulation interface.
    
    Attributes:
        text (str): Button label
        x (int): X-coordinate position
        y (int): Y-coordinate position
        icon_path (str): Path to button icon image
        action (function): Function to call when button is clicked
    """
    def __init__(self, text, x, y, icon_path, action=None):
        self.text = text
        self.x = x
        self.y = y
        self.icon_path = icon_path
        self.action = action
        self.icon = pygame.image.load(icon_path).convert_alpha()

    def draw(self, window):
        """Draw the button on the window"""
        window.blit(self.icon, (self.x, self.y))

    def is_clicked(self, pos):
        """Check if button was clicked"""
        button_rect = self.icon.get_rect(topleft=(self.x, self.y))
        return button_rect.collidepoint(pos)

class Simulator:
    """
    Main simulation controller class.
    
    Handles the simulation loop, user interface, and time controls.
    """
    def __init__(self, bodies=[]):
        self.running = True
        self.paused = False
        self.clock = pygame.time.Clock()
        self.time = 0  # Time elapsed in simulation (seconds since J2000)
        self.epoch = datetime.datetime(2000, 1, 1)  # J2000 epoch
        self.bodies = bodies
        
        # Load play button icon for later use
        pygame.image.load("icons/play.svg").convert_alpha()
        
        # Calculate middle of screen for button placement
        middle = width // 2
        
        # Initialize interface buttons
        self.buttons = [
            Button("Settings", 20, 20, "icons/settings.svg", self.open_settings),
            Button("Restart", 100, 20, "icons/restart.svg", self.restart),
            Button("Zoom out", 180, 20, "icons/zoom_out.svg", self.zoom_out),
            Button("Zoom in", 220, 20, "icons/zoom_in.svg", self.zoom_in),
            Button("Slow Down", middle - 80, 20, "icons/slow_down.svg", self.lower_speed),
            Button("Play", middle, 20, "icons/pause.svg", self.toggle_running),
            Button("Speed Up", middle + 80, 20, "icons/speed_up.svg", self.increase_speed),
            Button("Share", width - 320, 20, "icons/share.svg", self.share)
        ]
        
        # Initialize simulation speed settings
        self.speed = 3  # Default speed index
        self.speeds = {
            0: {"step": 1/60, "name": "1 frame = 1 second"},
            1: {"step": 1, "name": "1 frame = 1 minute"},
            2: {"step": 60 * 60, "name": "1 frame = 1 hour"},
            3: {"step": 60 * 60 * 24, "name": "1 frame = 1 day"},
            4: {"step": 60 * 60 * 24 * 7, "name": "1 frame = 1 week"}
        }

    def open_settings(self):
        """Open settings menu (placeholder)"""
        print("Open settings")

    def share(self):
        """Share simulation state (placeholder)"""
        print("Share simulation")

    def toggle_running(self):
        """Pause/unpause the simulation"""
        self.paused = not self.paused
        # Update button icon based on simulation state
        if self.paused:
            self.buttons[5].icon = pygame.image.load("icons/play.svg").convert_alpha()
        else:
            self.buttons[5].icon = pygame.image.load("icons/pause.svg").convert_alpha()

    def lower_speed(self):
        """Decrease simulation speed"""
        self.speed = max(0, self.speed - 1)

    def increase_speed(self):
        """Increase simulation speed"""
        self.speed = min(len(self.speeds) - 1, self.speed + 1)

    def restart(self):
        """Reset simulation to initial state"""
        for body in self.bodies:
            body.reset()
        self.time = 0

    def zoom_out(self):
        """Increase scale factor to zoom out"""
        global scale_factor
        scale_factor *= 1.1

    def zoom_in(self):
        """Decrease scale factor to zoom in"""
        global scale_factor
        scale_factor /= 1.1

    @property
    def date(self):
        """Current date in simulation"""
        return self.epoch + datetime.timedelta(seconds=self.time)

    def main(self):
        """Main simulation loop"""
        while self.running:
            # Handle events
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                if event.type == MOUSEBUTTONDOWN:
                    pos = pygame.mouse.get_pos()
                    for button in self.buttons:
                        if button.is_clicked(pos):
                            button.action()

            # Clear screen
            window.fill(Colours.black)
            
            # Find reference frame
            frame_of_reference = None
            for body in self.bodies:
                if body.frame_of_reference:
                    frame_of_reference = body
                    break

            # Draw date and speed information
            large_font = pygame.font.SysFont('Arial', 24)
            date_surface = large_font.render(
                f"{self.date.strftime('%d/%m/%Y at %H:%M:%S')}", 
                True, 
                Colours.white
            )
            window.blit(date_surface, (width - date_surface.get_width() - 20, 20))
            
            speed_surface = large_font.render(
                f"Speed: {self.speeds[self.speed]['name']}", 
                True, 
                Colours.white
            )
            window.blit(speed_surface, (width - speed_surface.get_width() - 20, 50))

            # Update and draw all bodies
            bodies_copy = self.bodies.copy()
            for body in self.bodies:
                if not self.paused:
                    body.update(bodies_copy, self.speeds[self.speed]["step"])
                body.draw(frame_of_reference)

            # Draw interface buttons
            for button in self.buttons:
                button.draw(window)

            # Update display
            pygame.display.flip()
            self.clock.tick(60)  # Maintain 60 FPS

            # Update simulation time
            if not self.paused:
                self.time += self.speeds[self.speed]["step"]

# Create bodies and run simulation
cursor.execute("SELECT * FROM Planets")
planets = cursor.fetchall()
bodies = []
for planet in planets:
    body = Body(*planet)
    if body.name in ORBITAL_PARAMS:
        body.Ma = ORBITAL_PARAMS[body.name]["Ma"]
        body.Mb = ORBITAL_PARAMS[body.name]["Mb"]
    bodies.append(body)

if __name__ == "__main__":
    bodies[0].frame_of_reference = True  # Set Sun as reference
    sim = Simulator(bodies)
    sim.main()