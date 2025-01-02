import customtkinter as ctk
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

    def load_settings(self) -> Dict[str, Any]:
        if not os.path.exists(self.SETTINGS_FILE):
            return self.default_settings.copy()

        try:
            with open(self.SETTINGS_FILE, "r") as file:
                settings = json.load(file)
                merged = self.default_settings.copy()
                merged.update(settings)
                return merged
        except (FileNotFoundError, json.JSONDecodeError) as e:
            logging.warning(f"Could not load settings: {e}")
            return self.default_settings.copy()

    def save_settings(self, settings: Dict[str, Any]) -> Dict[str, Any]:
        try:
            with open(self.SETTINGS_FILE, "w") as file:
                json.dump(settings, file, indent=4)
            self.settings = settings
            return settings
        except IOError as e:
            logging.error(f"Failed to save settings: {e}")
            return None


class SettingsUI(ctk.CTk):
    def __init__(self, came_from=None, settings_manager=None):
        super().__init__()

        self.came_from = came_from
        self.settings_manager = settings_manager or SettingsManager()

        self.title("Settings")
        self.geometry("500x600")
        self.resizable(False, False)

        # Define color themes
        self.colour_palettes = {
            "Blue": "blue",
            "Green": "green",
            "Orange": "custom-tkinter-themes/orange.json",
            "Pink": "custom-tkinter-themes/pink.json",
            "Purple": "custom-tkinter-themes/purple.json",
            "Red": "custom-tkinter-themes/red.json",
            "Yellow": "custom-tkinter-themes/yellow.json",
            "High Contrast": "custom-tkinter-themes/high_contrast.json"
        }

        self.create_application()

    def create_application(self):
        """Create or refresh the application UI."""
        # Clear existing widgets
        for widget in self.winfo_children():
            widget.destroy()

        # Load settings
        settings = self.settings_manager.load_settings()

        # Apply current settings
        ctk.set_appearance_mode(settings["Color mode"].lower())
        ctk.set_default_color_theme(settings["Colour palette"]["path"])

        # Header section
        header_frame = ctk.CTkFrame(self, fg_color="transparent")
        header_frame.pack(fill="x", padx=20, pady=(20, 0))

        # Back Button
        ctk.CTkButton(
            header_frame,
            text="🔙 Back",
            command=self.go_back,
            width=100,
            font=(settings["Font"], settings["Font size"], "bold" if settings["Font bold"] else "normal")
        ).pack(side="left")

        # Title
        ctk.CTkLabel(
            header_frame,
            text="⚙️ Settings",
            font=(settings["Font"], 26, "bold" if settings["Font bold"] else "normal"),
            anchor="center"
        ).pack(side="top", pady=(0, 10))

        # TabView section
        tabview = ctk.CTkTabview(self)
        tabview.pack(fill="both", expand=True, padx=20, pady=20)

        # Create tabs
        self.create_font_tab(tabview, settings)
        self.create_appearance_tab(tabview, settings)
        self.create_sound_tab(tabview, settings)

        # Save Button
        ctk.CTkButton(
            self,
            text="💾 Save Settings",
            command=self.save_settings,
            width=300,
            font=(settings["Font"], settings["Font size"], "bold" if settings["Font bold"] else "normal")
        ).pack(pady=20)

    def create_font_tab(self, tabview, settings):
        """Create Font Settings tab."""
        font_tab = tabview.add("🔤 Font")
        font_options = ["Arial", "Times New Roman", "Comic Sans MS", "Courier New", "Impact", "Georgia"]

        # Font settings
        self.font_var = ctk.StringVar(value=settings["Font"])
        ctk.CTkLabel(
            font_tab,
            text="Font Family",
            font=(settings["Font"], settings["Font size"], "bold" if settings["Font bold"] else "normal")
        ).pack(anchor="w", pady=(20, 5))

        ctk.CTkOptionMenu(
            font_tab,
            values=font_options,
            variable=self.font_var,
            width=300,
            font=(settings["Font"], settings["Font size"])
        ).pack(pady=10)

        self.bold_var = ctk.BooleanVar(value=settings["Font bold"])
        ctk.CTkCheckBox(
            font_tab,
            text="Bold Font",
            variable=self.bold_var,
            width=300,
            font=(settings["Font"], settings["Font size"])
        ).pack(pady=10)

    def create_appearance_tab(self, tabview, settings):
        """Create Appearance Settings tab."""
        appearance_tab = tabview.add("🎨 Appearance")
        color_modes = ["Light", "Dark", "System"]

        # Color mode settings
        self.color_mode_var = ctk.StringVar(value=settings["Color mode"])
        ctk.CTkLabel(
            appearance_tab,
            text="Color Mode",
            font=(settings["Font"], settings["Font size"], "bold" if settings["Font bold"] else "normal")
        ).pack(anchor="w", pady=(20, 5))

        ctk.CTkOptionMenu(
            appearance_tab,
            values=color_modes,
            variable=self.color_mode_var,
            width=300,
            font=(settings["Font"], settings["Font size"])
        ).pack(pady=10)

        # Color theme settings
        self.color_theme_var = ctk.StringVar(value=settings["Colour palette"]["name"])
        ctk.CTkLabel(
            appearance_tab,
            text="Color Theme",
            font=(settings["Font"], settings["Font size"], "bold" if settings["Font bold"] else "normal")
        ).pack(anchor="w", pady=(10, 5))

        ctk.CTkOptionMenu(
            appearance_tab,
            values=list(self.colour_palettes.keys()),
            variable=self.color_theme_var,
            width=300,
            font=(settings["Font"], settings["Font size"])
        ).pack(pady=10)

    def create_sound_tab(self, tabview, settings):
        """Create Sound Settings tab."""
        sound_tab = tabview.add("🔊 Sound")

        # Volume settings
        self.volume_var = ctk.DoubleVar(value=settings["Volume"])
        self.volume_label = ctk.CTkLabel(
            sound_tab,
            text=f"Volume: {int(settings['Volume'])}%",
            font=(settings["Font"], settings["Font size"], "bold" if settings["Font bold"] else "normal")
        )
        self.volume_label.pack(anchor="w", pady=(20, 5))

        volume_slider = ctk.CTkSlider(
            sound_tab,
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

    def go_back(self):
        """Return to the previous window."""
        if self.came_from:
            self.came_from.deiconify()
        self.destroy()

    def save_settings(self):
        """Save current settings."""
        updated_settings = {
            "Font": self.font_var.get(),
            "Font size": 12,
            "Font bold": self.bold_var.get(),
            "Color mode": self.color_mode_var.get(),
            "Colour palette": {
                "name": self.color_theme_var.get(),
                "path": self.colour_palettes[self.color_theme_var.get()]
            },
            "Volume": int(self.volume_var.get()),
            "Icon size": 24
        }

        try:
            self.settings_manager.save_settings(updated_settings)
            if self.came_from and hasattr(self.came_from, 'refresh_settings'):
                self.came_from.refresh_settings()
            self.refresh_ui()
        except Exception as e:
            logging.error(f"Error saving settings: {e}")

    def refresh_ui(self):
        """Refresh UI with updated settings."""
        current_geometry = self.geometry()
        self.create_application()
        self.geometry(current_geometry)


def main():
    """Application entry point."""
    app = SettingsUI()
    app.mainloop()


if __name__ == "__main__":
    main()
