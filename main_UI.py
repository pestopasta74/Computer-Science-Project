import customtkinter as ctk

class SolarSystemSimulator(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("Solar System Simulator")
        self.geometry("800x600")

        self.create_widgets()

    def create_widgets(self):
        self.label = ctk.CTkLabel(self, text="Solar System Simulator", font=("Arial", 24))
        self.label.pack(pady=20)

        self.start_button = ctk.CTkButton(self, text="Start Simulation", command=self.start_simulation)
        self.start_button.pack(pady=10)

        self.stop_button = ctk.CTkButton(self, text="Stop Simulation", command=self.stop_simulation)
        self.stop_button.pack(pady=10)

        self.quit_button = ctk.CTkButton(self, text="Quit", command=self.quit)
        self.quit_button.pack(pady=10)

    def start_simulation(self):
        print("Simulation started")

    def stop_simulation(self):
        print("Simulation stopped")

if __name__ == "__main__":
    app = SolarSystemSimulator()
    app.mainloop()