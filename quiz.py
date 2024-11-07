from modules.quiz_simulator import QuizSimulator
import customtkinter as ctk

class QuizScreen(QuizSimulator, ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("Solar System Quiz")
        self.geometry("350x300")

        self.create_widgets()

    def create_widgets(self):
        self.label = ctk.CTkLabel(self, text="Solar System Quiz", font=("Arial", 24))
        self.label.pack(pady=20)

        self.start_button = ctk.CTkButton(self, text="Start Quiz")
        self.start_button.pack(pady=10)

        self.quit_button = ctk.CTkButton(self, text="Quit", command=self.quit)
        self.quit_button.pack(pady=10)

if __name__ == "__main__":
    app = QuizScreen()
    app.mainloop()