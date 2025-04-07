import unittest
import data_validation as dv


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

    def test_valid_astronomical_uits(self):
        # Valid astronomical units
        valid_astronomical_units = [
        '1',
        '1.5',
        '0.5',
        '100',
        '1234567890'
        ]
        for unit in valid_astronomical_units:
            self.assertTrue(self.validator.astronomical_units(unit))

    def test_invalid_astronomical_units(self):
        # Invalid astronomical units
        invalid_astronomical_units = [
        '1.5.2',
        'abc',
        '-1',
        '-0.5',
        '0'
        ]
        for unit in invalid_astronomical_units:
            self.assertFalse(self.validator.astronomical_units(unit))

    def test_valid_standard_form(self):
        # Valid standard form numbers
        valid_standard_forms = [
        '1.23e10',
        '2.5E-3',
        '3.0e+2',
        '4.5678e5',
        '5.752x10^3',
        '6.0E+10',
        '7.89x10^2',
        '8.0e-1',
        '9.0x10^-3',
        ]
        # Test valid standard form numbers
        for standard_form in valid_standard_forms:
            self.assertTrue(self.validator.standard_form(standard_form))

    def test_invalid_standard_form(self):
        invalid_standard_forms = [
        '1.23e10.5',
        '2.5E-3.4',
        '3.0e+2.1',
        '4.5678e5.6',
        '5.752x10^3.7',
        '6.0E+10.8',
        '7.89x10^2.9'
        ]
        # Test invalid standard form numbers
        for standard_form in invalid_standard_forms:
            self.assertFalse(self.validator.standard_form(standard_form))

if __name__ == '__main__':
    unittest.main()

# import user_management as um
# import quiz_simulator as qs

# class TestQuizSimulator(unittest.TestCase):
#     def setUp(self):
#         # Create an instance of the QuizSimulator class to test the quiz simulator
#         self.quiz_simulator = qs.QuizSimulator()

#     def test_gravity_question(self):
#         # Test the generate_gravity_question method
#         question, answer = self.quiz_simulator.generate_gravity_question()
#         self.assertTrue(isinstance(question, str))
#         self.assertTrue(isinstance(answer, float))

#     def test_orbital_velocity_question(self):
#         # Test the generate_orbital_velocity_question method
#         question, answer = self.quiz_simulator.generate_orbital_velocity_question()
#         self.assertTrue(isinstance(question, str))
#         self.assertTrue(isinstance(answer, float))

#     def test_escape_velocity_question(self):
#         # Test the generate_escape_velocity_question method
#         question, answer = self.quiz_simulator.generate_escape_velocity_question()
#         self.assertTrue(isinstance(question, str))
#         self.assertTrue(isinstance(answer, float))

#     def test_gravitational_field_strength_question(self):
#         # Test the generate_gravitational_field_strength_question method
#         question, answer = self.quiz_simulator.generate_gravitational_field_strength_question()
#         self.assertTrue(isinstance(question, str))
#         self.assertTrue(isinstance(answer, float))

#     def test_generate_question(self):
#         # Test the generate_question method
#         question, answer = self.quiz_simulator.generate_question()
#         self.assertTrue(isinstance(question, str))
#         self.assertTrue(isinstance(answer, float))

#     def test_start_quiz(self):
#         # Test the start_quiz method
#         self.assertIsNone(self.quiz_simulator.start_quiz())

