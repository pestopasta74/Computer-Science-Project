import customtkinter as ctk
from tkinter import messagebox
from modules.simulation_management import SimulationDatabase


# Set appearance mode and default color theme
ctk.set_appearance_mode("System")
ctk.set_default_color_theme("blue")

# Create a class for each result (simulation) in the database
class SimulationResult(ctk.CTkFrame):
    def __init__(self, master, title, image, description, **kwargs):
        super().__init__(master, corner_radius=10, **kwargs)
        self.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)

        # Add some example content to the result frame
        title_label = ctk.CTkLabel(self, text=title, font=("", 16, "bold"))
        title_label.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")

        description_label = ctk.CTkLabel(self, text=description)
        description_label.grid(row=1, column=0, padx=10, pady=10, sticky="nsew")


# Create a scrollable frame for the results
class ScrollableResultsFrame(ctk.CTkScrollableFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)
        self.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)

        # Add some example content to the results_frame
        db = SimulationDatabase()
        simulations = db.get_simulations(1)  # Get simulations for category 1 (kinematics)
        for i, (id, title, description, image_path, file_path, category_id) in enumerate(simulations):
            result = SimulationResult(self, title, image_path, description)
            result.grid(row=i, column=0, padx=10, pady=10, sticky="nsew")


class MainUI(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.resizable(True, True)
        self.minsize(1000, 600)
        self.title('Home')
        self.geometry('1250x750')

        # Configure grid layout: 2 columns and 3 rows
        self.grid_columnconfigure(0, weight=1)  # Sidebar column (1/4 of the width)
        self.grid_columnconfigure(1, weight=4)  # Main content column (3/4 of the width)
        self.grid_rowconfigure(0, weight=0)  # Header row for search and filters
        self.grid_rowconfigure(1, weight=1)  # Content row for tags and results
        self.grid_rowconfigure(2, weight=0)  # Bottom padding or footer (optional)

        # Search Frame (row 0, column 0 and column 1)
        self.search_frame = ctk.CTkFrame(self, corner_radius=10)
        self.search_frame.grid(row=0, column=0, columnspan=1, padx=10, pady=10, sticky="ew")
        self.search_frame.grid_columnconfigure(0, weight=1)
        self.search_bar = ctk.CTkEntry(self.search_frame, placeholder_text="Search")
        self.search_bar.grid(row=0, column=0, padx=10, pady=10, sticky="ew")
        self.search_bar.bind("<Return>", self.search)

       # Sidebar Frame (Tags and Filters)
        self.sidebar_frame = ctk.CTkFrame(self, corner_radius=10)
        self.sidebar_frame.grid(row=1, column=0, padx=10, pady=10, sticky="nsew")
        self.sidebar_frame.grid_rowconfigure(list(range(40)), weight=1)  # Configure rows for equal spacing
        self.sidebar_frame.grid_columnconfigure(0, weight=1)  # Allow the tag list to stretch horizontally

        # Add a tags title label
        tags_label = ctk.CTkLabel(
            self.sidebar_frame,
            text="Categories:",
            font=("", 20, "bold"),
            wraplength=200  # Adjust this value if necessary
        )
        tags_label.grid(row=0, column=0, padx=5, pady=5, sticky="nws")


        # Adding some example tags as buttons inside the sidebar_frame
        tags = SimulationDatabase().get_categories()
        for i, tag in enumerate(tags):
            tag_button = ctk.CTkButton(self.sidebar_frame, text=tag)
            tag_button.grid(row=i + 1, column=0, padx=5, pady=5, sticky="new")

        # add a filter title label
        filter_label = ctk.CTkLabel(
            self.sidebar_frame,
            text="Filters:",
            font=("", 20, "bold"),
            wraplength=200  # Adjust this value if necessary
        )
        filter_label.grid(row=4, column=0, padx=5, pady=5, sticky="nws")

        # Main Content Frame
        self.content_frame = ctk.CTkFrame(self, corner_radius=10)
        self.content_frame.grid(row=0, column=1, rowspan=2, padx=10, pady=10, sticky="nsew")
        self.content_frame.grid_rowconfigure(0, weight=1)  # Allow stretching in content frame
        self.content_frame.grid_columnconfigure(0, weight=1)

        # Example of Results Frame inside Main Content Frame
        self.results_frame = ScrollableResultsFrame(self.content_frame)
        self.results_frame.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")
        self.results_frame.grid_rowconfigure(0, weight=1)
        self.results_frame.grid_columnconfigure(0, weight=1)

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
