import customtkinter as ctk

class StartScreen(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("Solar System Simulator")
        self.geometry("350x300")

        self.create_widgets()

    def create_widgets(self):
        self.label = ctk.CTkLabel(self, text="Solar System Simulator", font=("Arial", 24))
        self.label.pack(pady=20)

        self.start_button = ctk.CTkButton(self, text="Start Simulator")
        self.start_button.pack(pady=10)

        self.quiz_button = ctk.CTkButton(self, text="Take Quiz")
        self.quiz_button.pack(pady=10)

        self.sandbox_button = ctk.CTkButton(self, text="Sandbox Mode")
        self.sandbox_button.pack(pady=10)

        self.quit_button = ctk.CTkButton(self, text="Quit", command=self.quit)
        self.quit_button.pack(pady=10)


if __name__ == "__main__":
    app = StartScreen()
    app.mainloop()