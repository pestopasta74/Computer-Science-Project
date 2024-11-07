import customtkinter as ctk
import json
import os

class Settings(ctk.CTk):
    SETTINGS_FILE = "settings.json"

    def __init__(self):
        super().__init__()
        self.title("Settings")
        self.geometry("800x600")

        # Load settings
        settings = self.load_settings()
        self.font = settings.get("Font", "Arial")
        self.font_size = settings.get("Font size", 12)
        self.color_mode = settings.get("Color mode", "Light")
        self.colour_palette = settings.get("Colour palette", "Default")
        self.volume = settings.get("Volume", 50)
        self.icon_size = settings.get("Icon size", 24)

        # Apply color mode
        ctk.set_appearance_mode(self.color_mode)
        self.create_widgets()

    def load_settings(self):
        # Load settings from JSON file, return defaults if file is missing or invalid
        if os.path.exists(self.SETTINGS_FILE):
            try:
                with open(self.SETTINGS_FILE, "r") as file:
                    return json.load(file)
            except (json.JSONDecodeError, IOError):
                print("Error loading settings. Using defaults.")
        return {}

    def save_settings(self):
        # Save settings to JSON file
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

    def create_widgets(self):
        # Title Label
        ctk.CTkLabel(self, text="Settings", font=(self.font, int(2 * self.font_size))).pack(pady=20)

        # Font Selection Dropdown
        optionmenu_var = ctk.StringVar(value=self.font)
        font_menu = ctk.CTkOptionMenu(
            self, values=["Arial", "Times New Roman", "Comic Sans MS", "Courier New", "Impact", "Georgia"],
            command=self.change_font, variable=optionmenu_var
        )
        font_menu.pack(pady=20)

        # Color Mode Selection Dropdown
        color_var = ctk.StringVar(value=self.color_mode)
        color_menu = ctk.CTkOptionMenu(
            self, values=["Light", "Dark", "System"],
            command=self.change_color_mode, variable=color_var
        )
        color_menu.pack(pady=20)

        # Save Button
        save_button = ctk.CTkButton(self, text="Save", command=self.save)
        save_button.pack(pady=20)

    def change_font(self, choice):
        print("Font changed to:", choice)
        self.font = choice

    def change_color_mode(self, choice):
        print("Color mode changed to:", choice)
        self.color_mode = choice
        ctk.set_appearance_mode(choice)  # Apply color mode

    def refresh(self):
        # Reinitialize widgets without fully reinitializing the window
        for widget in self.winfo_children():
            widget.destroy()
        self.create_widgets()

    def save(self):
        # Save settings and refresh interface
        self.save_settings()
        self.refresh()

if __name__ == "__main__":
    settings_app = Settings()
    settings_app.mainloop()
