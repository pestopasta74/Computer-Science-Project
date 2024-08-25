from modules.user_management import UserDatabase
import subprocess

try:
    open("user_login_info.txt", "r")
    print("File exists")
except FileNotFoundError:
    subprocess.run(['python3', 'login_UI.py'])