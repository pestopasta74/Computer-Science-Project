import customtkinter as ctk
import tkinter as tk
import json
import os
import logging
from typing import Dict, Any

class SettingsManager:
    SETTINGS_FILE = "settings.json"

    def __init__(self):
        self.default_settings = {
            "Font": "Arial",
            "Font size": 12,
            "Font bold": False,
            "Color mode": "System",
            "Colour palette": {
                "name": "Blue",
                "path": "blue"
            },
            "Volume": 50,
            "Icon size": 24
        }
        self.settings = self.load_settings()

    def load_settings(self):
        """Load settings from file or use defaults."""
        try:
            with open(self.SETTINGS_FILE, "r") as file:
                settings = json.load(file)
                # Merge with defaults to handle potential missing keys
                return {**self.default_settings, **settings}
        except (FileNotFoundError, json.JSONDecodeError):
            logging.warning("Could not load settings. Using defaults.")
            return self.default_settings

    def save_settings(self, updated_settings):
        """Save settings to file."""
        try:
            with open(self.SETTINGS_FILE, "w") as file:
                json.dump(updated_settings, file, indent=4)
            return updated_settings
        except IOError:
            logging.error("Failed to save settings")
            return None

class SettingsUI(ctk.CTk):
    def __init__(self, came_from):
        super().__init__()

        # Window configuration
        self.title("Application Settings")
        self.geometry("500x700")
        self.resizable(False, False)
        self.came_from = came_from # Store the previous window

        # Initialize settings manager
        self.settings_manager = SettingsManager()

        # Prepare color palettes
        self.colour_palettes = {
            "Blue": "blue",
            "Green": "custom-tkinter-themes/green.json",
            "Orange": "custom-tkinter-themes/orange.json",
            "Pink": "custom-tkinter-themes/pink.json",
            "Purple": "custom-tkinter-themes/purple.json",
            "Red": "custom-tkinter-themes/red.json",
            "Yellow": "custom-tkinter-themes/yellow.json",
            "High Contrast": "custom-tkinter-themes/high_contrast.json",
        }

        # Initial setup
        self.create_application()

    def create_application(self):
        """Create or refresh the entire application window."""
        # Destroy existing widgets if any
        for widget in self.winfo_children():
            widget.destroy()

        # Reload current settings
        settings = self.settings_manager.load_settings()

        # Set appearance based on current settings
        ctk.set_appearance_mode(settings["Color mode"].lower())
        palette = settings["Colour palette"]
        ctk.set_default_color_theme(palette["path"])

        # Main scrollable frame
        main_frame = ctk.CTkScrollableFrame(self, width=460, height=600)
        main_frame.pack(padx=20, pady=20)

        # Title
        ctk.CTkLabel(
            main_frame,
            text="⚙️ Application Settings",
            font=(settings["Font"], 24, "bold" if settings["Font bold"] else "normal")
        ).pack(pady=(0, 20))

        # Font Settings
        font_frame = self._create_section(main_frame, "🔤 Font Settings")

        # Font Family Dropdown
        font_options = ["Arial", "Times New Roman", "Comic Sans MS", "Courier New", "Impact", "Georgia"]
        self.font_var = ctk.StringVar(value=settings["Font"])
        ctk.CTkLabel(font_frame, text="Font Family").pack(anchor="w")
        font_menu = ctk.CTkOptionMenu(
            font_frame,
            values=font_options,
            variable=self.font_var,
            width=300
        )
        font_menu.pack(pady=10)

        # Bold Font Checkbox
        self.bold_var = ctk.BooleanVar(value=settings["Font bold"])
        bold_check = ctk.CTkCheckBox(
            font_frame,
            text="Bold Font",
            variable=self.bold_var,
            width=300
        )
        bold_check.pack(pady=10)

        # Appearance Settings
        appearance_frame = self._create_section(main_frame, "🎨 Appearance")

        # Color Mode Dropdown
        color_modes = ["Light", "Dark", "System"]
        self.color_mode_var = ctk.StringVar(value=settings["Color mode"])
        ctk.CTkLabel(appearance_frame, text="Color Mode").pack(anchor="w")
        color_mode_menu = ctk.CTkOptionMenu(
            appearance_frame,
            values=color_modes,
            variable=self.color_mode_var,
            width=300
        )
        color_mode_menu.pack(pady=10)

        # Color Theme Dropdown
        self.color_theme_var = ctk.StringVar(value=settings["Colour palette"]["name"])
        ctk.CTkLabel(appearance_frame, text="Color Theme").pack(anchor="w")
        color_theme_menu = ctk.CTkOptionMenu(
            appearance_frame,
            values=list(self.colour_palettes.keys()),
            variable=self.color_theme_var,
            width=300
        )
        color_theme_menu.pack(pady=10)

        # Sound Settings
        sound_frame = self._create_section(main_frame, "🔊 Sound")

        # Volume Slider
        self.volume_var = ctk.DoubleVar(value=settings["Volume"])
        self.volume_label = ctk.CTkLabel(
            sound_frame,
            text=f"Volume: {int(settings['Volume'])}%"
        )
        self.volume_label.pack(anchor="w")

        volume_slider = ctk.CTkSlider(
            sound_frame,
            from_=0,
            to=100,
            number_of_steps=100,
            variable=self.volume_var,
            width=300
        )
        volume_slider.pack(pady=10)
        volume_slider.configure(
            command=lambda value: self.volume_label.configure(
                text=f"Volume: {int(value)}%"
            )
        )

        # Save Button
        save_button = ctk.CTkButton(
            main_frame,
            text="💾 Save Settings",
            command=self.save_settings,
            width=300
        )
        save_button.pack(pady=20)

        # Status Label
        self.status_var = ctk.StringVar()
        self.status_label = ctk.CTkLabel(
            main_frame,
            textvariable=self.status_var,
            text_color="green"
        )
        self.status_label.pack(pady=10)

    def _create_section(self, parent, title):
        """Create a styled section header and frame."""
        ctk.CTkLabel(
            parent,
            text=title,
            font=("Arial", 16, "bold")
        ).pack(anchor="w", pady=(10, 5))

        frame = ctk.CTkFrame(parent, fg_color="transparent")
        frame.pack(fill="x", pady=(0, 15))

        return frame

    def save_settings(self):
        """Compile and save current settings."""
        updated_settings = {
            "Font": self.font_var.get(),
            "Font size": 12,  # Keeping original value
            "Font bold": self.bold_var.get(),
            "Color mode": self.color_mode_var.get(),
            "Colour palette": {
                "name": self.color_theme_var.get(),
                "path": self.colour_palettes[self.color_theme_var.get()]
            },
            "Volume": int(self.volume_var.get()),
            "Icon size": 24  # Keeping original value
        }

        # Attempt to save settings
        saved_settings = self.settings_manager.save_settings(updated_settings)

        if saved_settings:
            # Refresh the entire application window
            self.create_application()

            # Show success message
            self.status_var.set("✅ Settings saved and applied successfully!")
            self.after(2000, lambda: self.status_var.set(""))
        else:
            # Show error message
            self.status_var.set("❌ Failed to save settings")
            self.after(2000, lambda: self.status_var.set(""))

    def quit_application(self):
        """Close the application and re-open previous window"""
        self.came_from.deiconify()
        self.destroy()



def main():
    """Application entry point."""
    app = SettingsUI()
    app.mainloop()

if __name__ == "__main__":
    main()