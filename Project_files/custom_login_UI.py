from data_validation import DataValidator
import customtkinter as ctk
import CTkMessagebox as ctkmsg

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
        self.master.geometry('400x250')
        self.validator = DataValidator()

        self.create_widgets()
        self.place_widgets()

    def create_widgets(self):
        self.label_email = ctk.CTkLabel(self.master, text='Email')
        self.entry_email = ctk.CTkEntry(self.master, corner_radius=10, border_width=2, border_color='black')

        self.label_password = ctk.CTkLabel(self.master, text='Password')
        self.entry_password = ctk.CTkEntry(self.master, show='*', corner_radius=10, border_width=2, border_color='black')

        self.submit_button = ctk.CTkButton(self.master, text='Submit', command=self.validate, fg_color='green')
        self.forgot_password_button = ctk.CTkButton(self.master, text='Forgotten password?', text_color='black')

    def place_widgets(self):
        self.label_email.place(x=50, y=50)
        self.entry_email.place(x=150, y=50)

        self.label_password.place(x=50, y=100)
        self.entry_password.place(x=150, y=100)

        self.submit_button.place(x=250, y=210)
        self.forgot_password_button.place(x=150, y=150)

    def validate(self):
        email = self.entry_email.get()
        password = self.entry_password.get()

        if self.validator.email(email) and self.validator.password(password):
            pass
        else:
            ctkmsg.CTkMessagebox(title="Try again", message="Incorrect Email/Password", icon="cancel", option_1="Retry")

if __name__ == '__main__':
    app = LoginUI(root)
    app.master.mainloop()
