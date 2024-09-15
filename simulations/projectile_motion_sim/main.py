import customtkinter as ctk
import matplotlib as plt
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import (
    FigureCanvasTkAgg, NavigationToolbar2Tk)
import modules.physics as physics

# Set appearance mode and default color theme
ctk.set_appearance_mode("System")
ctk.set_default_color_theme("blue")


class MainUI(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.resizable(True, True)
        self.minsize(1000, 600)
        self.title('Projectile Motion Simulation')
        self.geometry('1250x750')

        # Configure grid layout: 2 columns and 3 rows
        self.grid_columnconfigure(0, weight=4)  # Main content column (3/4 of the width)
        self.grid_columnconfigure(1, weight=1)  # Sidebar column (1/4 of the width)
        self.grid_rowconfigure(0, weight=1)  # Header row for search and filters

       # Sidebar Frame (Tags and Filters)
        self.sidebar_frame = ctk.CTkFrame(self, corner_radius=10)
        self.sidebar_frame.grid(row=0, column=1, padx=10, pady=10, sticky="nsew")
        self.sidebar_frame.grid_rowconfigure(list(range(40)), weight=1)  # Configure rows for equal spacing
        self.sidebar_frame.grid_columnconfigure(0, weight=1)  # Allow the tag list to stretch horizontally

        # Main Content Frame
        self.simulation_display_frame = ctk.CTkFrame(self, corner_radius=10)
        self.simulation_display_frame.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")
        self.simulation_display_frame.grid_rowconfigure(0, weight=1)  # Allow stretching in content frame
        self.simulation_display_frame.grid_columnconfigure(0, weight=1)

        self.physics = physics.Physics(0, 0, 45, gravity=-9.81)
        self.time = 0

        # Set up sidebar sliders and dropdowns
        self.gravity_slider_label = ctk.CTkLabel(self.sidebar_frame, text="Gravity (m/s²)")
        self.gravity_slider = ctk.CTkSlider(self.sidebar_frame, from_=0, to=20, number_of_steps=20, command=self.set_gravity)
        self.gravity_slider.set(-self.physics.acceleration)
        self.gravity_slider_label.grid(row=1, column=0, padx=10, pady=10, sticky="ew")
        self.gravity_slider.grid(row=0, column=0, padx=10, pady=10, sticky="ew")
        self.gravity_dropdown = ctk.CTkOptionMenu(self.sidebar_frame, values=["-9.81", "-10", "-20", "-30", "-40", "-50"])
        self.gravity_dropdown.grid(row=2, column=0, padx=10, pady=10, sticky="ew")

        # Create a canvas for the simulation display
        self.canvas = ctk.CTkCanvas(self.simulation_display_frame)
        self.canvas.grid(row=0, column=0, sticky="nsew")
        # Add a matplotlib plot to the canvas
        self.plot = Figure(figsize=(5, 5))
        self.plot_canvas = plt.backends.backend_tkagg.FigureCanvasTkAgg(self.plot, master=self.canvas)
        self.plot_canvas.get_tk_widget().pack(fill=ctk.BOTH, expand=True)
        self.subplot = self.plot.add_subplot(111)

        self.update_graph()

    def update_graph(self):
        # Graph y=gravityx
        x = range(0, 10)
        y = [self.physics.acceleration * i for i in x]
        self.subplot.clear()
        self.subplot.plot(x, y)
        self.plot_canvas.draw()

    def set_gravity(self, event):
        new_gravity = int(self.gravity_slider.get())
        self.physics.acceleration = -new_gravity
        print(self.physics.acceleration)
        self.update_graph()




def main():
    app = MainUI()
    app.mainloop()


if __name__ == '__main__':
    main()
