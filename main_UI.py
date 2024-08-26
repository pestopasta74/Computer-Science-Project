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

        # Configure grid layout: 2 columns and 2 rows
        self.grid_columnconfigure(0, weight=1)  # Sidebar column (1/4 of the width)
        self.grid_columnconfigure(1, weight=4)  # Main content column (3/4 of the width)
        self.grid_rowconfigure(0, weight=0)  # "Header row" for the search bar
        self.grid_rowconfigure(1, weight=1)  # Allow content to stretch vertically

        # Search frame
        self.search_frame = ctk.CTkFrame(self, corner_radius=10)
        self.search_frame.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")
        self.search_frame.grid_columnconfigure(0, weight=1)  # Allow search bar to stretch horizontally
        self.search_frame.grid_rowconfigure(0, weight=0)  # Allow search bar to stretch vertically
        self.search_bar = ctk.CTkEntry(self.search_frame, placeholder_text="Search")
        self.search_bar.grid(row=0, column=0, padx=10, pady=10)
        self.search_bar.pack(fill="x", expand=True, padx=10, pady=10)
        self.search_bar.bind("<Return>", self.search)

        # Sidebar Frame
        self.sidebar_frame = ctk.CTkFrame(self, corner_radius=10)
        self.sidebar_frame.grid(row=1, column=0, padx=10, pady=10, sticky="nsew")
        self.sidebar_frame.grid_rowconfigure(0, weight=0)  # Stop stretching for the search bar row
        self.sidebar_frame.grid_rowconfigure(1, weight=1)  # Allow stretching for other content rows

        # Main Content Frame
        self.content_frame = ctk.CTkFrame(self, corner_radius=10)
        self.content_frame.grid(row=0, column=1, padx=10, pady=10, rowspan=2, sticky="nsew")

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
    app.mainloop()


if __name__ == '__main__':
    main()
