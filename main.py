from modules.user_management import UserDatabase
import subprocess

try:
    with open("user_login_info.txt", "r") as file:
        email, password = file.read().splitlines()
        db = UserDatabase()
        if db.check_user(email, password):
            subprocess.run(['python3', 'main_UI.py'])
        else:
            print('it does not work')
            subprocess.run(['python3', 'login_UI.py'])

except FileNotFoundError:
    subprocess.run(['python3', 'login_UI.py'])