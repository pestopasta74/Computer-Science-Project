import customtkinter as ctk
from tkinter import messagebox

def show_retry_messagebox():
    response = messagebox.askretrycancel("Try again", "Incorrect Email/Password")
    return "Retry" if response else "Cancel"


def validate():
    email = entry_email.get()
    password = entry_password.get()

    print(f"Validating: email={email}, password={password}")

    if email == "test123" and password == "testing guys":  # Simulating successful validation
        print("Validation successful")
    else:
        print("Validation failed")
        if show_retry_messagebox() == "Retry":
            print("Retrying... Clearing entries and setting focus.")
            reset_entries()

def reset_entries():
    # Ensure the entry fields are enabled and focus is set correctly
    entry_email.configure(state='normal')
    entry_password.configure(state='normal')
    entry_email.delete(0, 'end')
    entry_password.delete(0, 'end')
    entry_email.focus_set()  # Explicitly set the focus
    print("Entries cleared and focus set to email entry.")

# Set appearance mode and default color theme
ctk.set_appearance_mode("System")
ctk.set_default_color_theme("blue")

# Create the main application window
root = ctk.CTk()
root.resizable(False, False)
root.geometry('400x200')
root.title('Login')

# Create widgets
label_email = ctk.CTkLabel(root, text='Email')
entry_email = ctk.CTkEntry(root, corner_radius=10, border_width=2, border_color='black', width=250)
label_password = ctk.CTkLabel(root, text='Password')
entry_password = ctk.CTkEntry(root, show='*', corner_radius=10, border_width=2, border_color='black', width=250)
submit_button = ctk.CTkButton(root, text='Submit', command=validate, fg_color='green', hover_color='darkgreen')
forgot_password_button = ctk.CTkButton(root, text='Forgotten password?', text_color='black')

# Place widgets
label_email.place(x=25, y=25)
entry_email.place(x=100, y=25)
label_password.place(x=25, y=75)
entry_password.place(x=100, y=75)
submit_button.place(x=215, y=135)
forgot_password_button.place(x=60, y=135)

if __name__ == '__main__':
    root.mainloop()
