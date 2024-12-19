import customtkinter as ctk
import json
import os
from typing import Callable
from tkinter import messagebox

class Settings:
    SETTINGS_FILE = "settings.json"

    def __init__(self):
        # Default settings
        self.font = "Arial"
        self.font_size = 12
        self.font_bold = False
        self.color_mode = "Light"
        self.colour_palette = {"name": "Blue", "path": "blue"}
        self.volume = 50
        self.icon_size = 24
        self.original_settings = {}  # Store original settings for comparison

        self.colour_palletes = {
            "Blue": "blue",
            "Green": "custom-tkinter-themes/green.json",
            "Orange": "custom-tkinter-themes/orange.json",
            "Pink": "custom-tkinter-themes/pink.json",
            "Purple": "custom-tkinter-themes/purple.json",
            "Red": "custom-tkinter-themes/red.json",
            "Yellow": "custom-tkinter-themes/yellow.json",
            "High Contrast": "custom-tkinter-themes/high_contrast.json",
        }
        self.load_settings()
        self.store_original_settings()

    def store_original_settings(self):
        """Store the original settings for comparison"""
        self.original_settings = {
            "Font": self.font,
            "Font size": self.font_size,
            "Font bold": self.font_bold,
            "Color mode": self.color_mode,
            "Colour palette": self.colour_palette,
            "Volume": self.volume,
            "Icon size": self.icon_size
        }

    def load_settings(self):
        if os.path.exists(self.SETTINGS_FILE):
            try:
                with open(self.SETTINGS_FILE, "r") as file:
                    settings = json.load(file)
                    self.font = settings.get("Font", self.font)
                    self.font_size = settings.get("Font size", self.font_size)
                    self.font_bold = settings.get("Font bold", self.font_bold)
                    self.color_mode = settings.get("Color mode", self.color_mode)
                    colour_palette = settings.get("Colour palette", self.colour_palette)
                    if isinstance(colour_palette, str):
                        colour_palette = {"name": colour_palette, "path": self.colour_palletes.get(colour_palette, "blue")}
                    self.colour_palette = colour_palette
                    self.volume = settings.get("Volume", self.volume)
                    self.icon_size = settings.get("Icon size", self.icon_size)
            except (json.JSONDecodeError, IOError):
                print("Error loading settings. Using defaults.")

    def save_settings(self):
        settings = {
            "Font": self.font,
            "Font size": self.font_size,
            "Font bold": self.font_bold,
            "Color mode": self.color_mode,
            "Colour palette": self.colour_palette,
            "Volume": self.volume,
            "Icon size": self.icon_size
        }
        with open(self.SETTINGS_FILE, "w") as file:
            json.dump(settings, file, indent=4)
        self.store_original_settings()  # Update original settings after saving

class SettingsUI(ctk.CTk):
    def __init__(self, on_back_callback=None):
        super().__init__()
        self.settings = Settings()
        self.on_back_callback = on_back_callback

        # Configure window
        self.title("Settings")
        self.geometry("600x900")
        self.resizable(False, False)

        # Apply initial settings
        ctk.set_appearance_mode(self.color_mode)
        ctk.set_default_color_theme(self.colour_palette["path"])
        self.font_weight = "bold" if self.font_bold else "normal"

        # Status message
        self.status_var = ctk.StringVar()

        # Create UI elements
        self.create_widgets()

        # Center window
        self.center_window()

        # Bind closing event
        self.protocol("WM_DELETE_WINDOW", self.on_closing)

    def center_window(self):
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()
        window_width = 600
        window_height = 800
        x = (screen_width - window_width) // 2
        y = (screen_height - window_height) // 2
        self.geometry(f"{window_width}x{window_height}+{x}+{y}")

    def create_widgets(self):
        # Header frame with back and close buttons
        header_frame = ctk.CTkFrame(self, fg_color="transparent")
        header_frame.pack(fill="x", padx=20, pady=10)

        # Back button
        back_button = ctk.CTkButton(
            header_frame,
            text="← Back",
            command=self.handle_back,
            width=80,
            height=32,
            corner_radius=8
        )
        back_button.pack(side="left")

        # Close button
        close_button = ctk.CTkButton(
            header_frame,
            text="✕ Close",
            command=self.on_closing,
            width=80,
            height=32,
            corner_radius=8,
            fg_color="red",
            hover_color="dark red"
        )
        close_button.pack(side="right")

        # Main container with padding
        self.main_frame = ctk.CTkScrollableFrame(
            self,
            fg_color=("gray95", "gray10"),
            corner_radius=15
        )
        self.main_frame.pack(padx=40, pady=(0, 40), fill="both", expand=True)

        # Title
        title_frame = ctk.CTkFrame(self.main_frame, fg_color="transparent")
        title_frame.pack(fill="x", padx=20, pady=(20, 40))

        ctk.CTkLabel(
            title_frame,
            text="⚙️ Settings",
            font=(self.font, 32, "bold")
        ).pack()

        # Settings sections container
        settings_frame = ctk.CTkFrame(self.main_frame, fg_color="transparent")
        settings_frame.pack(fill="both", expand=True, padx=20)

        # Create settings sections
        self.create_font_section(settings_frame)
        self.create_appearance_section(settings_frame)
        self.create_sound_section(settings_frame)

        # Status message
        self.status_label = ctk.CTkLabel(
            settings_frame,
            textvariable=self.status_var,
            font=(self.font, 16),
            text_color="green"
        )
        self.status_label.pack(pady=(20, 0))

        # Bottom buttons frame
        button_frame = ctk.CTkFrame(self, fg_color="transparent")
        button_frame.pack(fill="x", padx=40, pady=(0, 20), side="bottom")

        # Save button
        ctk.CTkButton(
            button_frame,
            text="💾 Save Changes",
            command=self.save_and_show_confirmation,
            height=45,
            corner_radius=8,
            font=(self.font, 14, "bold")
        ).pack(side="left", padx=(0, 10), expand=True, fill="x")

        # Logout button
        ctk.CTkButton(
            button_frame,
            text="🚪 Log Out",
            command=self.confirm_logout,
            height=45,
            corner_radius=8,
            font=(self.font, 14, "bold"),
            fg_color="red",
            hover_color="dark red"
        ).pack(side="right", expand=True, fill="x")

    def create_font_section(self, parent):
        self.create_section_label("🔤 Font Settings", parent)

        font_frame = ctk.CTkFrame(parent, fg_color="transparent")
        font_frame.pack(fill="x", pady=(0, 20))

        # Font family selection
        ctk.CTkLabel(font_frame, text="Font Family", font=(self.settings.font, 14)).pack(anchor="w")
        font_var = ctk.StringVar(value=self.settings.font)
        font_menu = ctk.CTkOptionMenu(
            font_frame,
            values=["Arial", "Times New Roman", "Comic Sans MS", "Courier New", "Impact", "Georgia"],
            variable=font_var,
            width=200,
            height=35,
            corner_radius=8
        )
        font_menu.pack(pady=(5, 0))
        font_menu.configure(command=lambda choice: self.preview_setting(self.change_font, choice))

        # Bold font checkbox
        bold_var = ctk.BooleanVar(value=self.settings.font_bold)
        ctk.CTkCheckBox(
            font_frame,
            text="Bold Font",
            variable=bold_var,
            command=lambda: self.preview_setting(self.change_font_weight),
            width=200,
            height=35,
            corner_radius=8
        ).pack(pady=(10, 0))

    def create_appearance_section(self, parent):
        self.create_section_label("🎨 Appearance", parent)

        appearance_frame = ctk.CTkFrame(parent, fg_color="transparent")
        appearance_frame.pack(fill="x", pady=(0, 20))

        # Color mode selection
        ctk.CTkLabel(appearance_frame, text="Color Mode", font=(self.settings.font, 14)).pack(anchor="w")
        view_mode_var = ctk.StringVar(value=self.settings.color_mode)
        view_mode_menu = ctk.CTkOptionMenu(
            appearance_frame,
            values=["Light", "Dark", "System"],
            variable=view_mode_var,
            width=200,
            height=35,
            corner_radius=8
        )
        view_mode_menu.pack(pady=(5, 10))
        view_mode_menu.configure(command=lambda choice: self.preview_setting(self.change_color_mode, choice))

        # Color theme selection
        ctk.CTkLabel(appearance_frame, text="Color Theme", font=(self.settings.font, 14)).pack(anchor="w")
        colour_var = ctk.StringVar(value=self.settings.colour_palette["name"])
        colour_menu = ctk.CTkOptionMenu(
            appearance_frame,
            values=list(self.settings.colour_palletes.keys()),
            variable=colour_var,
            width=200,
            height=35,
            corner_radius=8
        )
        colour_menu.pack(pady=(5, 0))
        colour_menu.configure(command=lambda choice: self.preview_setting(self.change_colour_palette, choice))

    def create_sound_section(self, parent):
        self.create_section_label("🔊 Sound", parent)

        volume_frame = ctk.CTkFrame(parent, fg_color="transparent")
        volume_frame.pack(fill="x", pady=(0, 20))

        self.volume_label = ctk.CTkLabel(volume_frame, text=f"Volume: {self.settings.volume}%", font=(self.settings.font, 14))
        self.volume_label.pack(anchor="w")

        volume_slider = ctk.CTkSlider(
            volume_frame,
            from_=0,
            to=100,
            number_of_steps=100,
            variable=ctk.DoubleVar(value=self.settings.volume),
            width=200,
            height=20,
            corner_radius=8
        )
        volume_slider.pack(pady=(5, 0))
        volume_slider.configure(command=lambda value: self.preview_setting(self.change_volume, value))

    def create_section_label(self, text, parent):
        section_frame = ctk.CTkFrame(parent, fg_color="transparent")
        section_frame.pack(fill="x", pady=(20, 10))

        ctk.CTkLabel(
            section_frame,
            text=text,
            font=(self.settings.font, 18, "bold"),
            text_color=("gray40", "gray60")
        ).pack(anchor="w")

    def preview_setting(self, setting_func: Callable, *args):
        """Preview a setting without saving it"""
        setting_func(*args)
        self.show_status("Changes will be saved when you click 'Save Changes'")

    def show_status(self, message: str, duration: int = 2000):
        self.status_var.set(message)
        self.after(duration, lambda: self.status_var.set(""))

    def change_volume(self, value):
        self.settings.volume = int(float(value))
        self.volume_label.configure(text=f"Volume: {self.settings.volume}%")

    def change_font(self, choice):
        self.settings.font = choice
        self.update_font_settings()

    def change_color_mode(self, choice):
        self.settings.color_mode = choice
        ctk.set_appearance_mode(choice)

    def change_colour_palette(self, choice):
        self.settings.colour_palette = {"name": choice, "path": self.settings.colour_palletes[choice]}
        ctk.set_default_color_theme(self.settings.colour_palette["path"])

    def change_font_weight(self):
        self.settings.font_bold = not self.settings.font_bold
        self.settings.font_weight = "bold" if self.settings.font_bold else "normal"
        self.update_font_settings()

    def update_font_settings(self):
        for widget in self.winfo_children():
            if isinstance(widget, (ctk.CTkLabel, ctk.CTkButton)):
                current_font = widget.cget("font")
                if isinstance(current_font, tuple):
                    widget.configure(font=(self.settings.font, current_font[1], self.settings.font_weight))

    def save_and_show_confirmation(self):
        self.save_settings()
        self.apply_settings()  # Apply settings immediately to the window
        self.show_status("✅ Settings saved and applied successfully!")

    def apply_settings(self):
        """Apply the current settings to the UI immediately."""
        ctk.set_appearance_mode(self.settings.color_mode)
        ctk.set_default_color_theme(self.settings.colour_palette["path"])
        self.settings.font_weight = "bold" if self.settings.font_bold else "normal"
        self.update_font_settings()

    def save_and_show_confirmation(self):
        if self.settings.save_settings():
            self.show_status("✅ Settings saved successfully!")
        else:
            self.show_status("❌ Error saving settings")

    def handle_back(self):
        if self.has_unsaved_changes():
            if messagebox.askyesno("Unsaved Changes", "You have unsaved changes. Do you want to save before going back?"):
                self.settings.save_settings()
        if self.on_back_callback:
            self.on_back_callback()
        self.destroy()

    def has_unsaved_changes(self):
        current_settings = {
            "Font": self.settings.font,
            "Font size": self.settings.font_size,
            "Font bold": self.settings.font_bold,
            "Color mode": self.settings.color_mode,
            "Colour palette": self.settings.colour_palette,
            "Volume": self.settings.volume,
            "Icon size": self.settings.icon_size
        }
        return current_settings != self.settings.original_settings

    def confirm_logout(self):
        if messagebox.askyesno("Confirm Logout", "Are you sure you want to log out?"):
            self.logout()

    def logout(self):
        try:
            os.remove("user_login_info.txt")
        except FileNotFoundError:
            pass
        self.quit()

    def on_closing(self):
        if self.has_unsaved_changes():
            if messagebox.askyesno("Unsaved Changes", "You have unsaved changes. Do you want to save before closing?"):
                self.save_settings()
        self.destroy()

if __name__ == "__main__":
    app = SettingsUI()
    app.mainloop()
