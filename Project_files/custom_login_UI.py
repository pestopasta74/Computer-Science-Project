from data_validation import DataValidator
import customtkinter as ctk

# Set appearance mode and default color theme
ctk.set_appearance_mode("System")
ctk.set_default_color_theme("blue")

# Create the main application window
root = ctk.CTk()

class LoginUI:
    def __init__(self, master):
        self.master = master
        self.master.title('Login')
        self.master.geometry('600x400')
        self.validator = DataValidator()

        self.create_widgets()
        self.setup_layout()

    def create_widgets(self):
        self.label_email = ctk.CTkLabel(self.master, text='Email')
        self.entry_email = ctk.CTkEntry(self.master, corner_radius=10, border_width=2, border_color='black')

        self.label_password = ctk.CTkLabel(self.master, text='Password')
        self.entry_password = ctk.CTkEntry(self.master, show='*', corner_radius=10, border_width=2, border_color='black')

        self.submit_button = ctk.CTkButton(self.master, text='Submit', command=self.validate)
        self.forgot_password_button = ctk.CTkButton(self.master, text='Forgotten password?')

    def setup_layout(self):
        self.label_email.grid(row=0, column=0)
        self.entry_email.grid(row=0, column=1)

        self.label_password.grid(row=1, column=0)
        self.entry_password.grid(row=1, column=1)

        self.submit_button.grid(row=2, column=0)
        self.forgot_password_button.grid(row=2, column=1)

    def validate(self):
        email = self.entry_email.get()
        password = self.entry_password.get()

        if self.validator.email(email) and self.validator.password(password):
            ctk.CTkMessageBox.showinfo('Success', 'Valid email and password')
        else:
            ctk.CTkMessageBox.showerror('Error', 'Invalid email or password')

if __name__ == '__main__':
    app = LoginUI(root)
    app.master.mainloop()
