from modules.data_validation import DataValidator
import customtkinter as ctk
from tkinter import messagebox
from modules.user_management import UserDatabase


# Set appearance mode and default color theme
ctk.set_appearance_mode("System")
ctk.set_default_color_theme("blue")


class MainUI(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.resizable(True, True)
        self.minsize(1000, 600)
        self.title('Home')
        self.geometry('1250x750')

        # Configure grid layout: 2 columns and 1 row
        self.grid_columnconfigure(0, weight=1)  # Sidebar column (1/4 of the width)
        self.grid_columnconfigure(1, weight=3)  # Main content column (3/4 of the width)
        self.grid_rowconfigure(0, weight=1)  # Single row for both sidebar and content

        # Sidebar Frame
        self.sidebar_frame = ctk.CTkFrame(self, corner_radius=10)
        self.sidebar_frame.grid(row=0, column=0, sticky="nsew", padx=10, pady=10)

        # Main Content Frame
        self.content_frame = ctk.CTkFrame(self, corner_radius=10)
        self.content_frame.grid(row=0, column=1, sticky="nsew", padx=10, pady=10)

        # Configure rows inside frames to allow content to stretch
        self.sidebar_frame.grid_rowconfigure(0, weight=0)  # Stop stretching for the search bar row
        self.sidebar_frame.grid_rowconfigure(1, weight=1)  # Allow stretching for other content rows
        self.content_frame.grid_rowconfigure(0, weight=1)  # Allow stretching in content frame

        # Call setup_sidebar within the constructor
        self.setup_sidebar()

    def setup_sidebar(self):
        # Search bar inside the sidebar frame
        self.search_bar = ctk.CTkEntry(self.sidebar_frame, placeholder_text="Search", corner_radius=10)
        self.search_bar.grid(row=0, column=0, sticky="ew", padx=10, pady=10)

        # Corrected the method binding
        self.search_bar.bind("<Return>", self.search)

        # Add a dummy widget to demonstrate full height in sidebar
        self.dummy_label = ctk.CTkLabel(self.sidebar_frame, text="Other Content")
        self.dummy_label.grid(row=1, column=0, sticky="nsew", padx=5, pady=10)

    # Accept event as a parameter
    def search(self, event=None):
        search_query = self.search_bar.get()
        if not search_query:
            messagebox.showwarning("Search", "Please enter a search query.")
            return

        # Perform search operation
        print(f"Searching for: {search_query}")


def main():
    app = MainUI()
    app.setup_sidebar()
    app.mainloop()


if __name__ == '__main__':
    main()
