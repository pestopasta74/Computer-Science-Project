import customtkinter as ctk
from tkinter import messagebox
from modules.data_validation import DataValidator
from modules.user_management import UserDatabase
from settings import SettingsManager, SettingsUI
from PIL import Image

# Initialize settings
settings_manager = SettingsManager()
settings = settings_manager.settings

class LoginUI(ctk.CTk):
    def __init__(self):
        super().__init__()

        # Configure window
        self.title("Login")
        self.geometry("500x600")
        self.resizable(False, False)

        # Set appearance and theme
        ctk.set_appearance_mode(settings["Color mode"])
        ctk.set_default_color_theme(settings["Colour palette"]["path"])
        self.coloured_hearts_dict = {
            "Blue": "💙",
            "High Contrast": "🤍",
            "Green": "💚",
            "Yellow": "💛",
            "Purple": "💜",
            "Orange": "🧡",
            "Black": "🖤",
            "Pink": "🩷",
            "Red": "❤️"
        }

        # Initialize components
        self.validator = DataValidator()
        self.verify_user = UserDatabase()

        # Load icons with light and dark mode
        self.settings_image = ctk.CTkImage(
            light_image=Image.open("icons/settings_light.png"),
            dark_image=Image.open("icons/settings_dark.png"),
            size=(24, 24)
        )

        self.close_image = ctk.CTkImage(
            light_image=Image.open("icons/Circle_x_Light.png"),
            dark_image=Image.open("icons/Circle_x_Dark.png"),
            size=(24, 24)
        )

        # Create widgets
        self.create_widgets()

        # Center window on screen
        self.center_window()

    def center_window(self):
        """Center the window on the screen."""
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()
        window_width = 500
        window_height = 600
        x = (screen_width - window_width) // 2
        y = (screen_height - window_height) // 2
        self.geometry(f"{window_width}x{window_height}+{x}+{y}")

    def create_widgets(self):
        # Create a main frame with gradient effect
        self.main_frame = ctk.CTkFrame(
            self,
            fg_color=("gray95", "gray10"),
            corner_radius=15
        )
        self.main_frame.pack(padx=40, pady=40, fill="both", expand=True)

        # Header frame for close and settings buttons
        self.header_frame = ctk.CTkFrame(
            self.main_frame,
            fg_color="transparent"
        )
        self.header_frame.pack(fill="x", padx=20, pady=(20, 0))

        # Close and settings buttons
        self.close_button = ctk.CTkButton(
            self.header_frame,
            text="",
            image=self.close_image,
            command=self.quit_application,
            width=32,
            height=32,
            fg_color="transparent",
            hover_color=("gray85", "gray15"),
            corner_radius=8
        )
        self.close_button.pack(side="left")

        self.settings_button = ctk.CTkButton(
            self.header_frame,
            text="",
            image=self.settings_image,
            command=self.open_settings,
            width=32,
            height=32,
            fg_color="transparent",
            hover_color=("gray85", "gray15"),
            corner_radius=8
        )
        self.settings_button.pack(side="right")

        # Logo/Brand space (placeholder)
        for key, value in self.coloured_hearts_dict.items():
            if settings["Colour palette"]["name"] == key:
                logo_text = value
                break
            else:
                logo_text = "👤" # Should never occur

        self.logo_label = ctk.CTkLabel(
            self.main_frame,
            text=logo_text,
            font=("Arial", 64),
            text_color=("gray60", "gray40")
        )
        self.logo_label.pack(pady=(20, 0))

        # Title with enhanced styling
        self.title_label = ctk.CTkLabel(
            self.main_frame,
            text="Welcome Back",
            font=(settings["Font"], 32, "bold")
        )
        self.title_label.pack(pady=(20, 40))

        # Login form frame
        self.form_frame = ctk.CTkFrame(
            self.main_frame,
            fg_color="transparent"
        )
        self.form_frame.pack(fill="x", padx=40)

        # Email entry with icon
        self.entry_email = ctk.CTkEntry(
            self.form_frame,
            placeholder_text="Enter your email",
            height=45,
            corner_radius=8,
            border_width=2,
            font=(settings["Font"], 14),
            width=300
        )
        self.entry_email.pack(fill="x", pady=(0, 20))

        # Password entry with icon
        self.entry_password = ctk.CTkEntry(
            self.form_frame,
            placeholder_text="Enter your password",
            height=45,
            corner_radius=8,
            border_width=2,
            font=(settings["Font"], 14),
            width=300,
            show="•"
        )
        self.entry_password.pack(fill="x")

        # Remember me and forgot password row
        self.options_frame = ctk.CTkFrame(
            self.form_frame,
            fg_color="transparent"
        )
        self.options_frame.pack(fill="x", pady=(20, 30))

        self.remember_me = ctk.CTkCheckBox(
            self.options_frame,
            text="Remember me",
            font=(settings["Font"], 12),
            corner_radius=6,
            border_width=2,
            checkbox_height=20,
            checkbox_width=20
        )
        self.remember_me.pack(side="left")

        # Submit button with enhanced styling
        self.submit_button = ctk.CTkButton(
            self.form_frame,
            text="Sign In",
            command=self.validate_credentials,
            height=45,
            corner_radius=8,
            font=(settings["Font"], 14, "bold")
        )
        self.submit_button.pack(fill="x", pady=(0, 20))

    def validate_credentials(self):
        """Validate user credentials and handle login."""
        email = self.entry_email.get()
        password = self.entry_password.get()

        if not email or not password:
            messagebox.showerror("Error", "Please fill in all fields")
            return

        # Check email validity
        if not self.validator.email(email):
            messagebox.showerror("Error", "Invalid email format")
            self.entry_email.configure(border_color="red")
            return

        # Verify user credentials
        hashed_password = self.verify_user.check_user(email, password)
        if not hashed_password:
            messagebox.showerror("Error", "Invalid email or password")
            self.reset_entries()
            return

        # Save credentials if 'Remember me' is checked
        if self.remember_me.get():
            with open("user_login_info.txt", "w") as file:
                file.write(f"{email}\n{hashed_password}")

        messagebox.showinfo("Success", "Login successful!")
        self.quit_application()

    def reset_entries(self):
        """Clear and reset entry fields."""
        self.entry_email.delete(0, 'end')
        self.entry_password.delete(0, 'end')
        self.entry_email.configure(border_color=self.entry_email.cget("fg_color"))
        self.entry_password.configure(border_color=self.entry_password.cget("fg_color"))

    def refresh_settings(self):
        """Reload settings and apply to the Login UI."""
        settings = settings_manager.load_settings()

        # Update appearance and theme
        ctk.set_appearance_mode(settings["Color mode"])
        ctk.set_default_color_theme(settings["Colour palette"]["path"])

        # Update widgets based on settings (example: font)
        self.title_label.configure(
            font=(settings["Font"], 32, "bold" if settings["Font bold"] else "normal")
        )
        self.submit_button.configure(
            font=(settings["Font"], 14, "bold" if settings["Font bold"] else "normal")
        )


    def quit_application(self):
        """Close application and release resources."""
        self.verify_user.close_connection()
        self.destroy()

    def open_settings(self):
        """Open the settings window."""
        self.withdraw()  # Hide the login window
        settings_ui = SettingsUI(came_from=self, settings_manager=settings_manager)
        settings_ui.mainloop()

        # Refresh settings after closing settings UI
        self.refresh_settings()


if __name__ == "__main__":
    app = LoginUI()
    app.mainloop()
