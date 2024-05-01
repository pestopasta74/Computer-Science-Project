import re

def validate_phone_number(phone):
    pattern = r'^(((\+44\s?\d{4}|\(?0\d{4}\)?)\s?\d{3}\s?\d{3})|((\+44\s?\d{3}|\(?0\d{3}\)?)\s?\d{3}\s?\d{4})|((\+44\s?\d{2}|\(?0\d{2}\)?)\s?\d{4}\s?\d{4}))(\s?\#(\d{4}|\d{3}))?$'
    return bool(re.fullmatch(pattern, phone))

# Test the function
print(validate_phone_number('01234567890'))       # True
print(validate_phone_number('+441234567890'))     # True
print(validate_phone_number('+44 1234567890'))    # True
print(validate_phone_number('1234567890'))        # False (too short)
print(validate_phone_number('+1234567890'))       # False (invalid country code)
print(validate_phone_number('012345678901'))      # False (too many digits)
print(validate_phone_number('012345678'))         # False (too few digits)
