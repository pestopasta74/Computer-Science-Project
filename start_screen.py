import customtkinter as ctk
from settings import SettingsManager, SettingsUI
from PIL import Image
from modules.window_centre import center_window
import os

settings = SettingsManager()
settings.load_settings()

class StartScreen(ctk.CTk):
    def __init__(self):
        super().__init__()

        # Configure window
        self.size = "500x500"
        self.title("Main Menu")
        self.resizable(False, False)
        center_window(self, self.size)

        # Set appearance and theme
        ctk.set_appearance_mode(settings.settings["Color mode"])
        ctk.set_default_color_theme(settings.settings["Colour palette"]["path"])

        # Load settings icon
        self.settings_image = ctk.CTkImage(
            light_image=Image.open("icons/settings_light.png"),
            dark_image=Image.open("icons/settings_dark.png"),
            size=(48, 48)
        )

        # Load quit icon
        self.quit_image = ctk.CTkImage(
            light_image=Image.open("icons/Circle_x_Light.png"),
            dark_image=Image.open("icons/Circle_x_Dark.png"),
            size=(48, 48)
        )

        # Create widgets
        self.create_widgets()

    def create_widgets(self):
        # Title label
        self.label = ctk.CTkLabel(
            self,
            text="Solar System Simulator",
            font=(settings.settings["Font"], 24, "bold")
        )
        self.label.pack(pady=(30, 20))

        # Settings button
        self.settings_button = ctk.CTkButton(
            self,
            text="",
            image=self.settings_image,
            command=self.open_settings,
            fg_color="transparent",  # Keep transparent background if desired
            hover_color="#b0bec5",  # Hover color for feedback
            width=48,  # Set width to match the image size
            height=48  # Set height to match the image size
        )
        self.settings_button.place(x=10, y=10)

        # Quit button
        self.quit_button = ctk.CTkButton(
            self,
            text="",
            image=self.quit_image,
            command=self.quit,
            fg_color="transparent",
            hover_color="#b0bec5",
            width=48,
            height=48
        )
        self.quit_button.place(x=430, y=10)

        # Control buttons with unified styling
        button_config = {"width": 200, "height": 40, "corner_radius": 20, "font": (settings.settings["Font"], 14)}
        self.start_button = ctk.CTkButton(self, text="Start Simulator", **button_config)
        self.start_button.pack(pady=(10, 10))

        self.quiz_button = ctk.CTkButton(self, text="Take Quiz", **button_config)
        self.quiz_button.pack(pady=10)

        self.sandbox_button = ctk.CTkButton(self, text="See Results", **button_config)
        self.sandbox_button.pack(pady=10)

        self.quit_button = ctk.CTkButton(self, text="Logout", command=self.logout, **button_config)
        self.quit_button.pack(pady=(10, 30))

    def logout(self):
        # Delete the user_login_info.txt file if it exists
        file_path = "user_login_info.txt"
        if os.path.exists(file_path):
            os.remove(file_path)
        self.quit()


    def open_settings(self):
        # Placeholder function for settings action
        pass

if __name__ == "__main__":
    app = StartScreen()
    app.mainloop()
