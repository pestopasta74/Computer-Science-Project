from modules.data_validation import DataValidator
import customtkinter as ctk
from tkinter import messagebox
from modules.user_management import UserDatabase

# Set appearance mode and default color theme
ctk.set_appearance_mode("System")
ctk.set_default_color_theme("blue")

# Create the main application window

class LoginUI:
    def __init__(self):
        self.root = ctk.CTk()
        self.root.resizable(False, False)

        self.root.title('Login')
        self.root.geometry('400x200')
        self.validator = DataValidator()
        self.verify_user = UserDatabase()

        self.create_widgets()
        self.place_widgets()

    def create_widgets(self):
        self.entry_email = ctk.CTkEntry(self.root, corner_radius=7, border_width=1, border_color="gray50", width=300, placeholder_text='Email')
        self.entry_password = ctk.CTkEntry(self.root, show='•', corner_radius=7,  border_width=1, border_color="gray50", width=300, placeholder_text='Password')

        self.remember_me = ctk.CTkCheckBox(self.root, text='Remember me', text_color=('black', 'white'), border_width=1, border_color='gray50')
        self.submit_button = ctk.CTkButton(self.root, text='Submit', command=self.validate, fg_color='green', hover_color='darkgreen', text_color='black')

    def place_widgets(self):
        # Place the widgets on the window

        self.entry_email.place(x=50, y=29)
        self.entry_password.place(x=50, y=86)

        self.remember_me.place(x=50, y=143)
        self.submit_button.place(x=210, y=143)

    def show_retry_messagebox(self):
        response = messagebox.askretrycancel("Try again", "Incorrect Email/Password")
        return "Retry" if response else "Cancel"

    def reset_entries(self):
        # Ensure the entry fields are enabled and focus is set correctly
        self.entry_email.delete(0, 'end')
        self.entry_password.delete(0, 'end')
        self.entry_email.configure(placeholder_text = 'Email')
        self.entry_password.configure(placeholder_text = 'Password')

    def validate(self) -> bool:
        email = self.entry_email.get()
        password = self.entry_password.get()

        is_email_valid = self.validator.email(email)
        if not is_email_valid and self.show_retry_messagebox() == "Retry":
            self.reset_entries()
            return
        if not is_email_valid:
            return

        hashed_password = self.verify_user.check_user(email, password)
        if not hashed_password and self.show_retry_messagebox() == "Retry":
            return self.reset_entries()
        if not hashed_password:
            return

        if self.remember_me.get() == 1:
            # Save the email and password to a file
            with open("user_login_info.txt", "x") as f:
                # Save the hashed password
                f.write(email + '\n' + hashed_password)

        return True


def main():
    app = LoginUI()
    app.root.mainloop()


if __name__ == '__main__':
    main()