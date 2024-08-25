from modules.data_validation import DataValidator
import customtkinter as ctk
from tkinter import messagebox
from modules.user_management import UserDatabase


# Set appearance mode and default color theme
ctk.set_appearance_mode("System")
ctk.set_default_color_theme("blue")

# Create the main application window


class Sidebar(ctk.CTkFrame):
    def __init__(self, root, *args, **kwargs):
        super().__init__(root, *args, **kwargs)


class MainUI:
    def __init__(self):
        self.root = ctk.CTk()
        self.root.resizable(True, True)
        self.root.title('Home')
        self.root.geometry('1250x750')

        self.sidebar = Sidebar(self.root, width=200, height=750)

        self.create_widgets()
        self.place_widgets()

    def create_widgets(self):
        ...

    def place_widgets(self):
        ...


def main():
    app = MainUI()
    app.root.mainloop()


if __name__ == '__main__':
    main()