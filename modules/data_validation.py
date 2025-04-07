import re  # Import the regular expressions module

# Class to validate different types of user input data
class DataValidator:
    def email(self, data):
        # Checks weather the email is valid
        # Must contain an '@' symbol, a domain name and a top-level domain
        pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+(?:\.[a-zA-Z]{2,}|(?:\d{1,3}\.){3}\d{1,3})$'
        return bool(re.fullmatch(pattern, data))


    def password(self, password):
        # Validates a password:
        # Must be at least 8 characters long, contain at least one letter and one digit
        if len(password) < 8:
            return False
        if not re.search(r'[A-Za-z]', password):  # Check for at least one letter
            return False
        if not re.search(r'\d', password):        # Check for at least one digit
            return False
        return True

    def phone(self, data):
        # Validates a UK phone number
        # Accepts various formats with optional country code (+44), spaces, and parentheses
        pattern = r'^(((\+44\s?\d{4}|\(?0\d{4}\)?)\s?\d{3}\s?\d{3})|' \
                  r'((\+44\s?\d{3}|\(?0\d{3}\)?)\s?\d{3}\s?\d{4})|' \
                  r'((\+44\s?\d{2}|\(?0\d{2}\)?)\s?\d{4}\s?\d{4}))' \
                  r'(\s?\#(\d{4}|\d{3}))?$'
        return bool(re.fullmatch(pattern, data))

    def name(self, data):
        # Validates a person's name:
        # Only allows alphabetic characters, spaces, and hyphens
        pattern = r'^[a-zA-Z]+(?:[ -][a-zA-Z]+)*$'
        return bool(re.fullmatch(pattern, data))

    def username(self, data):
        # Validates a username:
        # Must be alphanumeric only (letters and digits)
        pattern = r'^[a-zA-Z0-9]+$'
        return bool(re.fullmatch(pattern, data))

    def birthdate(self, data):
        # Validates a birthdate:
        # Format must be YYYY-MM-DD, year between 1901 and 2019, valid month/day values
        if re.match(r'^\d{4}-\d{2}-\d{2}$', data):
            year = int(data[:4])
            month = int(data[5:7])
            day = int(data[8:10])
            if 1900 < year < 2020 and 0 < month < 13 and 0 < day < 32:
                return True
        return False

    def age(self, data):
        # Validates age:
        # Must be a number between 1 and 149
        if re.match(r'^[0-9]+$', data) and 0 < int(data) < 150:
            return True
        return False

    def length_check(self, data, length, option):
        # Checks length of the input string based on a condition:
        # option = 'min' -> checks if data is at least 'length' characters long
        # option = 'max' -> checks if data is at most 'length' characters long
        # option = 'equal' -> checks if data is exactly 'length' characters long
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

    def astronomical_units(self, data):
        # Validates astronomical units:
        # Must be a positive number (integer or float)
        pattern=r'^(?!0+(\.0+)?$)\d+(\.\d+)?$'
        return bool(re.fullmatch(pattern, data))

    def standard_form(self, data):
        # Validates numbers in standard form:
        # Pattern 1: Scientific notation using 'e' or 'E' (e.g., 2.5e3, -1.2E-4)
        pattern_scientific = r'^[+-]?\d+(\.\d+)?[eE][+-]?\d+$'
        if re.fullmatch(pattern_scientific, data):
            return True

        # Pattern 2: Standard form using 'x10^' (e.g., 2.5x10^3, -1.2x10^-4)
        pattern_x10 = r'^[+-]?\d+(\.\d+)?x10\^[+-]?\d+$'
        return bool(re.fullmatch(pattern_x10, data))
