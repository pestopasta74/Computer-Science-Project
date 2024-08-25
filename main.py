from modules.user_management import UserDatabase
import login_UI
import main_UI


try:
    with open("user_login_info.txt", "r") as file:
        email, password = file.read().splitlines()
except FileNotFoundError:
    email, password = '', ''

db = UserDatabase()
if not db.check_user(email, password):
    login_UI.main()

main_UI.main()

