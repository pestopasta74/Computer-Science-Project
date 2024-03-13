import tkinter as tk
import tkinter.ttk as ttk
import tkinter.messagebox as tkmessagebox

root = tk.Tk()

def login():
    print("Logging in")
    root.destroy()
    tk.messagebox.showinfo("Login", "You have logged in successfully")

def register():
    register_window = tk.Toplevel()
    register_window.title("Register")
    register_window.resizable(False, False)

def create_ui():
    root.title("Login")
    root.resizable(False, False)

    # Create a frame for the login section
    login_frame = tk.Frame(root)
    login_frame.pack(pady=10)

    tk.Label(login_frame, text="Username:").grid(row=0, column=0, padx=5, pady=5)
    username_entry = tk.Entry(login_frame)
    username_entry.grid(row=0, column=1, padx=5, pady=5)

    tk.Label(login_frame, text="Password:").grid(row=1, column=0, padx=5, pady=5)
    password_entry = tk.Entry(login_frame, show="*")
    password_entry.grid(row=1, column=1, padx=5, pady=5)

    login_button = tk.Button(login_frame, text="Login", command=login)
    login_button.grid(row=2, columnspan=2, padx=5, pady=5)

    # Create a separator between the login and registration sections
    separator = ttk.Separator(root, orient='horizontal')
    separator.pack(fill='x')

    # Create a frame for the registration section
    register_frame = tk.Frame(root)
    register_frame.pack(pady=10)

    tk.Label(register_frame, text="Don't have a login?").grid(row=0, column=0, padx=5, pady=5)

    register_button = tk.Button(register_frame, text="Register", command=register)
    register_button.grid(row=0, column=1, padx=5, pady=5)

    root.mainloop()
