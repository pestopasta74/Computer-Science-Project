from modules.data_validation import DataValidator
import customtkinter as ctk
from tkinter import messagebox
from modules.user_management import UserDatabase


# Set appearance mode and default color theme
ctk.set_appearance_mode("System")
ctk.set_default_color_theme("blue")

# Create the main application window
root = ctk.CTk()
root.resizable(True, True)

class MainUI:
    def __init__(self, master):
        self.master = master
        self.master.title('Home')
        self.master.geometry('1250x750')

        self.create_widgets()
        self.place_widgets()

    def create_widgets(self):
        ...

    def place_widgets(self):
        ...


def main():
    app = MainUI(root)
    app.master.mainloop()


if __name__ == '__main__':
    main()