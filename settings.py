import customtkinter as ctk
import json
import os

class Settings:
    SETTINGS_FILE = "settings.json"

    def __init__(self):
        # Default settings
        self.font = "Arial"
        self.font_size = 12
        self.font_bold = False  # New attribute for bold font
        self.color_mode = "Light"
        self.colour_palette = {"name": "Blue", "path": "blue"}  # Default palette with name and path
        self.volume = 50  # Volume default value
        self.icon_size = 24

        self.colour_palletes = {
            "Blue": "blue",  # Default palette
            "Green": "custom-tkinter-themes/green.json",
            "Orange": "custom-tkinter-themes/orange.json",
            "Pink": "custom-tkinter-themes/pink.json",
            "Purple": "custom-tkinter-themes/purple.json",
            "Red": "custom-tkinter-themes/red.json",
            "Yellow": "custom-tkinter-themes/yellow.json",
            "High Contrast": "custom-tkinter-themes/high_contrast.json",
        }
        # Load settings from file
        self.load_settings()

    def load_settings(self):
        """Load settings from JSON file, with fallback to defaults if file is missing or invalid."""
        if os.path.exists(self.SETTINGS_FILE):
            try:
                with open(self.SETTINGS_FILE, "r") as file:
                    settings = json.load(file)
                    self.font = settings.get("Font", self.font)
                    self.font_size = settings.get("Font size", self.font_size)
                    self.font_bold = settings.get("Font bold", self.font_bold)  # Load bold setting
                    self.color_mode = settings.get("Color mode", self.color_mode)
                    colour_palette = settings.get("Colour palette", self.colour_palette)
                    if isinstance(colour_palette, str):
                        colour_palette = {"name": colour_palette, "path": self.colour_palletes.get(colour_palette, "Blue")}
                    self.colour_palette = colour_palette
                    self.volume = settings.get("Volume", self.volume)  # Load volume setting
                    self.icon_size = settings.get("Icon size", self.icon_size)
            except (json.JSONDecodeError, IOError):
                print("Error loading settings. Using defaults.")

    def save_settings(self):
        """Save current settings to JSON file."""
        settings = {
            "Font": self.font,
            "Font size": self.font_size,
            "Font bold": self.font_bold,  # Save bold setting
            "Color mode": self.color_mode,
            "Colour palette": self.colour_palette,
            "Volume": self.volume,  # Save volume setting
            "Icon size": self.icon_size
        }
        with open(self.SETTINGS_FILE, "w") as file:
            json.dump(settings, file)

class SettingsUI(ctk.CTk, Settings):
    def __init__(self):
        ctk.CTk.__init__(self)  # Initialize CTk window
        Settings.__init__(self)  # Initialize settings management

        self.title("Settings")
        self.geometry("800x600")

        # Apply initial color mode
        ctk.set_appearance_mode(self.color_mode)

        # Apply initial colour palette
        ctk.set_default_color_theme(self.colour_palette["path"])

        # Set font weight based on bold setting
        self.font_weight = "bold" if self.font_bold else "normal"

        # Create UI elements
        self.create_widgets()

    def create_widgets(self):
        ctk.set_default_color_theme(self.colour_palette["path"])  # Apply colour palette for when refreshing

        # Title label with bold handling
        ctk.CTkLabel(self, text="Settings", font=(self.font, int(2 * self.font_size), self.font_weight)).pack(pady=20)

        # Font selection dropdown
        font_var = ctk.StringVar(value=self.font)
        font_menu = ctk.CTkOptionMenu(
            self, values=["Arial", "Times New Roman", "Comic Sans MS", "Courier New", "Impact", "Georgia"],
            command=self.change_font, variable=font_var
        )
        font_menu.pack(pady=20)

        # View mode selection dropdown
        view_mode_var = ctk.StringVar(value=self.color_mode)
        view_mode_menu = ctk.CTkOptionMenu(
            self, values=["Light", "Dark", "System"],
            command=self.change_color_mode, variable=view_mode_var
        )
        view_mode_menu.pack(pady=20)

        # Colour palette selection dropdown
        colour_var = ctk.StringVar(value=self.colour_palette["name"])
        colour_menu = ctk.CTkOptionMenu(
            self, values=list(self.colour_palletes.keys()),
            command=self.change_colour_palette, variable=colour_var
        )
        colour_menu.pack(pady=20)

        # Bold font checkbox
        bold_var = ctk.BooleanVar(value=self.font_bold)
        bold_check = ctk.CTkCheckBox(self, text="Bold", variable=bold_var, command=self.change_font_weight)
        bold_check.pack(pady=20)

        # Volume slider
        volume_slider = ctk.CTkSlider(
            self, from_=0, to=100, number_of_steps=100,
            command=self.change_volume, variable=ctk.DoubleVar(value=self.volume)
        )
        volume_slider_label = ctk.CTkLabel(self, text="Volume")
        volume_slider_label.pack(pady=10)
        volume_slider.pack(pady=10)

        # Save button
        save_button = ctk.CTkButton(self, text="Save", command=self.save_and_refresh)
        save_button.pack(pady=20)

        # Log out Button (also quits app)
        log_out_button = ctk.CTkButton(self, text="Log Out", command=self.logoout)
        log_out_button.pack(pady=20)

    def change_font(self, choice):
        print("Font changed to:", choice)
        self.font = choice

    def change_color_mode(self, choice):
        print("Color mode changed to:", choice)
        self.color_mode = choice

    def change_colour_palette(self, choice):
        print("Colour palette changed to:", choice)
        self.colour_palette = {"name": choice, "path": self.colour_palletes[choice]}

    def change_font_weight(self):
        bold = not self.font_bold
        print("Font weight changed to:", bold)
        self.font_bold = bold
        self.font_weight = "bold" if bold else "normal"

    def change_volume(self, volume):
        print("Volume set to:", int(volume))
        self.volume = int(volume)

    def save_and_refresh(self):
        """Save settings and refresh the UI to reflect changes."""
        self.save_settings()
        self.refresh()

    def refresh(self):
        """Refresh the UI elements without reinitializing the entire window."""
        for widget in self.winfo_children():
            widget.destroy()
        ctk.set_appearance_mode(self.color_mode)
        self.create_widgets()

    def logoout(self):
        """Log out the user and quit the application."""
        try:
            os.remove("user_login_info.txt")
        except FileNotFoundError:
            pass
        self.quit()

if __name__ == "__main__":
    settings_app = SettingsUI()
    settings_app.mainloop()
