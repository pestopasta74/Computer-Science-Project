from data_validation import DataValidator
import customtkinter as ctk
from tkinter import messagebox

# Set appearance mode and default color theme
ctk.set_appearance_mode("System")
ctk.set_default_color_theme("blue")

# Create the main application window
root = ctk.CTk()
root.resizable(False, False)

class LoginUI:
    def __init__(self, master):
        self.master = master
        self.master.title('Login')
        self.master.geometry('400x200')
        self.validator = DataValidator()

        self.create_widgets()
        self.place_widgets()

    def create_widgets(self):
        self.entry_email = ctk.CTkEntry(self.master, corner_radius=7, border_width=1, border_color="gray50", width=300, placeholder_text='Email')
        self.entry_password = ctk.CTkEntry(self.master, show='*', corner_radius=7,  border_width=1, border_color="gray50", width=300, placeholder_text='Password')

        self.submit_button = ctk.CTkButton(self.master, text='Submit', command=self.validate, fg_color='green', hover_color='darkgreen', text_color='black')
        self.forgot_password_button = ctk.CTkButton(self.master, text='Forgotten password?', text_color='black')

    def place_widgets(self):
        # Place the widgets on the window

        self.entry_email.place(x=60, y=25)
        self.entry_password.place(x=60, y=75)

        self.submit_button.place(x=215, y=135)
        self.forgot_password_button.place(x=60, y=135)

    def show_retry_messagebox(self):
        response = messagebox.askretrycancel("Try again", "Incorrect Email/Password")
        return "Retry" if response else "Cancel"

    def reset_entries(self):
        # Ensure the entry fields are enabled and focus is set correctly
        self.entry_email.delete(0, 'end')
        self.entry_password.delete(0, 'end')
        self.entry_email.configure(placeholder_text = 'Email')
        self.entry_password.configure(placeholder_text = 'Password')

    def validate(self):
        email = self.entry_email.get()
        password = self.entry_password.get()

        if self.validator.email(email) and self.validator.password(password):
            pass
        else:
            if self.show_retry_messagebox() == "Retry":
                self.reset_entries()


if __name__ == '__main__':
    app = LoginUI(root)
    app.master.mainloop()
