import tkinter as tk

class GUI(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Login Form")
        self.geometry("400x400")
        self.create_widgets()


    def create_widgets(self):
        self.label = tk.Label(self, text="Login Form")
        self.label.pack()

        self.username_label = tk.Label(self, text="Username")
        self.username_label.pack()

        self.username_entry = tk.Entry(self)
        self.username_entry.pack()

        self.password_label = tk.Label(self, text="Password")
        self.password_label.pack()

        self.password_entry = tk.Entry(self, show="*")
        self.password_entry.pack()

        self.login_button = tk.Button(self, text="Login", command=self.login)
        self.login_button.pack()


    def login(self):
        username = self.username_entry.get()
        password = self.password_entry.get()

        if username == "admin" and password == "admin":
            print("Login successful")
        else:
            print("Login failed")


if __name__ == "__main__":
    app = GUI()
    app.mainloop()