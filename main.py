from modules.user_management import UserDatabase
import login_UI
import start_screen

# Trying to read the user login information from a file
try:
    with open("user_login_info.txt", "r") as file:
        email, password = file.read().splitlines()
except FileNotFoundError:
    email, password = '', ''

# Creating an instance of the UserDatabase class
db = UserDatabase()

# Checking if the user exists in the database
if not db.check_user(email, password):
    # If the user doesn't exist, display the login UI
    ui = login_UI
    ui.main()
    del ui

# Display the start screen (as we now have a valid user)
start_screen.main()
