import customtkinter as ctk
import json
import os

class Settings:
    SETTINGS_FILE = "settings.json"

    def __init__(self):
        # Default settings
        self.font = "Arial"
        self.font_size = 12
        self.color_mode = "Light"
        self.colour_palette = "Blue" # Default colour palette that comes with custom tkinter
        self.volume = 50
        self.icon_size = 24

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
                    self.color_mode = settings.get("Color mode", self.color_mode)
                    self.colour_palette = settings.get("Colour palette", self.colour_palette)
                    self.volume = settings.get("Volume", self.volume)
                    self.icon_size = settings.get("Icon size", self.icon_size)
            except (json.JSONDecodeError, IOError):
                print("Error loading settings. Using defaults.")

    def save_settings(self):
        """Save current settings to JSON file."""
        settings = {
            "Font": self.font,
            "Font size": self.font_size,
            "Color mode": self.color_mode,
            "Colour palette": self.colour_palette,
            "Volume": self.volume,
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

        # Create UI elements
        self.create_widgets()

    def create_widgets(self):
        # Title label
        ctk.CTkLabel(self, text="Settings", font=(self.font, int(2 * self.font_size))).pack(pady=20)

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
        colour_var = ctk.StringVar(value=self.colour_palette)
        colour_menu = ctk.CTkOptionMenu(
            self, values=["Blue", "Green", "Red", "Purple", "Orange", "Yellow"],
            variable=colour_var
        )

        # Save button
        save_button = ctk.CTkButton(self, text="Save", command=self.save_and_refresh)
        save_button.pack(pady=20)

    def change_font(self, choice):
        print("Font changed to:", choice)
        self.font = choice

    def change_color_mode(self, choice):
        print("Color mode changed to:", choice)
        self.color_mode = choice
        ctk.set_appearance_mode(choice)

    def save_and_refresh(self):
        """Save settings and refresh the UI to reflect changes."""
        self.save_settings()
        self.refresh()

    def refresh(self):
        """Refresh the UI elements without reinitializing the entire window."""
        for widget in self.winfo_children():
            widget.destroy()
        self.create_widgets()

if __name__ == "__main__":
    settings_app = SettingsUI()
    settings_app.mainloop()
