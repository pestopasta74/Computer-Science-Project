import unittest
import modules.data_validation as dv
import modules.user_management as um

class TestValidator(unittest.TestCase):
    def setUp(self):
        # Create an instance of the DataValidator class to test data validation
        self.validator = dv.DataValidator()

    def test_valid_email(self):
        # Valid emails
        valid_emails = [
        'user@example.com',
        'email@example.co.jp',
        'firstname-lastname@example.com',
        'email@example.museum',
        'email@example.name',
        '_______@example.com',
        '1234567890@example.com',
        'email@123.123.123.123'
        ]

        for email in valid_emails:
            # Tests valid emails
            self.assertTrue(self.validator.email(email))


    def test_invalid_email(self):
        # Invalid emails
        invalid_emails = [
        'plainaddress',
        '@example.com',
        'email@',
        'email@.com',
        'email@'
        ]

        for email in invalid_emails:
            # Tests invalid emails
            self.assertFalse(self.validator.email(email))


    def test_valid_phone(self):
        # Valid phone numbers
        valid_phones = [
        '+44 7975 556677',
        '07947674716',
        '020 7946 0716',
        '02079460716',
        '07975 556677'
]

        for phone in valid_phones:
            # Tests valid phone numbers
            self.assertTrue(self.validator.phone(phone))


    def test_invalid_phone(self):
        # Invalid phone numbers
        invalid_phones = [
        '1234567890',
        '1234',
        '12345678901234567890',
        '1234567890',
        '+1234567890',
        '+44 1234 56789'
]

        for phone in invalid_phones:
            # Tests invalid phone numbers
            self.assertFalse(self.validator.phone(phone))


    def test_valid_names(self):
        # Valid names
        valid_names = [
        'Preston',
        'Tyler',
        'Spencer',
        'Millie Hardy',
        'Ebony-Jane Smith',
        'Preston Leighton Tony Shaun Whiteman',
        'CJ',
        'J'
        ]

        for name in valid_names:
            self.assertTrue(self.validator.name(name))


    def test_invalid_names(self):
        # Invalid names
        invalid_names = [
        'ca55idy',
        'pestopasta74',
        'John.Doe',
        '#Maria'
]

        for name in invalid_names:
            self.assertFalse(self.validator.name(name))


    def test_valid_usernames(self):
        valid_usernames = [
        'username123',
        'USERNAME',
        'User123',
        'user',
        '1234567890',
        'abc123XYZ'
]
        for username in valid_usernames:
            self.assertTrue(self.validator.username(username))


    def test_invalid_usernames(self):
        # Invalid usernames
        invalid_usernames = [
        'username@',
        'user name',
        'user.name',
        'user-name',
        'user_name',
        '123@abc'
]

        for username in invalid_usernames:
            self.assertFalse(self.validator.username(username))


    def test_valid_birthdate(self):
        # Valid birthdates
        valid_birthdates = [
        '2000-01-01',
        '1990-12-31',
        '1990-01-01',
        '2000-12-31',
        '2007-05-21'
        ]

        for birthdate in valid_birthdates:
            self.assertTrue(self.validator.birthdate(birthdate))


    def test_invalid_birthdate(self):
        # Invalid birthdates
        invalid_birthdates = [
        '2000-01-32',
        '1990-12-32',
        '1990-00-01',
        '2000-13-31',
        '2007-05-32'
        ]

        for birthdate in invalid_birthdates:
            self.assertFalse(self.validator.birthdate(birthdate))


if __name__ == '__main__':
    unittest.main()