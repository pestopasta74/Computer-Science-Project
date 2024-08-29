import re

# Class to validate data
class DataValidator:
    def email(self, data):
        # Checks weather the email is valid
        pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+(?:\.[a-zA-Z]{2,}|(?:\d{1,3}\.){3}\d{1,3})$'
        return bool(re.fullmatch(pattern, data))

    def password(self, password):
        # password validation (at least 8 characters, one letter, one number)
        if len(password) < 8:
            return False
        if not re.search(r'[A-Za-z]', password):
            return False
        if not re.search(r'\d', password):
            return False
        return True

    def phone(self, data):
        # Checks weather the number is a valid UK phone number
        pattern = r'^(((\+44\s?\d{4}|\(?0\d{4}\)?)\s?\d{3}\s?\d{3})|((\+44\s?\d{3}|\(?0\d{3}\)?)\s?\d{3}\s?\d{4})|((\+44\s?\d{2}|\(?0\d{2}\)?)\s?\d{4}\s?\d{4}))(\s?\#(\d{4}|\d{3}))?$'
        return bool(re.fullmatch(pattern, data))


    def name(self, data):
        pattern = r'^[a-zA-Z]+(?:[ -][a-zA-Z]+)*$'
        return bool(re.fullmatch(pattern, data))


    def username(self, data):
        pattern = r'^[a-zA-Z0-9]+$'
        return bool(re.fullmatch(pattern, data))


    def birthdate(self, data):
        if re.match(r'^\d{4}-\d{2}-\d{2}$', data) and 1900 < int(data[:4]) < 2020 and 0 < int(data[5:7]) < 13 and 0 < int(data[8:10]) < 32:
            return True
        return False


    def age(self, data):
        if re.match(r'^[0-9]+$', data) and 0 < int(data) < 150:
            return True
        return False

    def length_check(self, data, length, option):
        if option == 'min':
            if len(data) >= length:
                return True
        elif option == 'max':
            if len(data) <= length:
                return True
        elif option == 'equal':
            if len(data) == length:
                return True
        return False
