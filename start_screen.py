import customtkinter as ctk
from settings import Settings
from PIL import Image
from modules.window_centre import center_window

settings = Settings()
settings.load_settings()

class StartScreen(ctk.CTk):
    def __init__(self):
        super().__init__()

        # Configure window
        self.size = "500x500"
        self.title("Solar System Simulator")
        self.resizable(False, False)
        center_window(self, self.size)

        # Set appearance and theme
        ctk.set_appearance_mode(settings.color_mode)
        ctk.set_default_color_theme(settings.colour_palette["path"])

        # Load settings icon
        self.settings_image = ctk.CTkImage(
            light_image=Image.open("icons/settings_light.png"),
            dark_image=Image.open("icons/settings_dark.png"),
            size=(48, 48)
        )

        # Create widgets
        self.create_widgets()

    def create_widgets(self):
        # Title label
        self.label = ctk.CTkLabel(
            self,
            text="Solar System Simulator",
            font=(settings.font, 24, "bold")
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

        # Control buttons with unified styling
        button_config = {"width": 200, "height": 40, "corner_radius": 20, "font": (settings.font, 14)}
        self.start_button = ctk.CTkButton(self, text="Start Simulator", **button_config)
        self.start_button.pack(pady=(10, 10))

        self.quiz_button = ctk.CTkButton(self, text="Take Quiz", **button_config)
        self.quiz_button.pack(pady=10)

        self.sandbox_button = ctk.CTkButton(self, text="Sandbox Mode", **button_config)
        self.sandbox_button.pack(pady=10)

        self.quit_button = ctk.CTkButton(self, text="Quit", command=self.quit, **button_config)
        self.quit_button.pack(pady=(10, 30))

    def open_settings(self):
        # Placeholder function for settings action
        pass

if __name__ == "__main__":
    app = StartScreen()
    app.mainloop()
