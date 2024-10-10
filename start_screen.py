import customtkinter as ctk
from tkinter import messagebox
from PIL import Image
import subprocess

# Set appearance mode and default color theme
ctk.set_appearance_mode("System")  # Can be 'Light', 'Dark', or 'System'
ctk.set_default_color_theme("blue")

class StartScreenUI(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.resizable(False, False)
        self.title('Login')
        self.geometry('400x200')

        # Call the method to set the initial icon based on the current appearance mode
        self.create_widgets()
        self.place_widgets()

    def create_widgets(self):
        # Create button with an initial image placeholder, we will update the image later
        settings_img = ctk.CTkImage(
            Image.open("icons/settings.png"), size=(30, 30)
        )
        self.settings_button = ctk.CTkButton(self, text='', command=self.open_settings, width=35, height=35, fg_color='white', image=settings_img)

        self.settings_button.image = settings_img


    def place_widgets(self):
        # Place the button in the top-left corner
        self.settings_button.place(x=10, y=10)



    def open_settings(self):
        # Placeholder for the settings function
        messagebox.showinfo("Settings", "Settings window would open here.")

def main():
    app = StartScreenUI()
    app.mainloop()

if __name__ == '__main__':
    main()
