import sqlite3
import random

# Constants
G = 6.67430 * 10 ** -11  # Gravitational constant (m^3 kg^-1 s^-2)
AU = 1.496 * 10 ** 11  # Astronomical unit (m)
scale_factor = 5 * 10 ** 9  # Scaling factor for the solar system to fit on screen
time_step = 60 * 60 * 24  # Time step in seconds (1 day per update)

# Connecting to the database
conn = sqlite3.connect('database.db')
cursor = conn.cursor()

class Colours:
    red = (255, 0, 0)
    green = (0, 255, 0)
    blue = (0, 0, 255)
    yellow = (255, 255, 0)
    white = (255, 255, 255)
    black = (0, 0, 0)
    cyan = (0, 255, 255)
    magenta = (255, 0, 255)
    gray = (128, 128, 128)
    orange = (255, 165, 0)

def standard_form_converter(num):
    """"Given a number in base units (e.g. 1.989e30), returns the number in standard form (e.g. 1.989 x 10^30)."""
    num_str = f"{num:.2e}"
    base, exponent = num_str.split('e')
    return f"{base} x 10^{int(exponent)}"


class PhysicsSimulator:
    def __init__(self):
        pass

    def gravitational_force(self, m1, m2, r):
        """
        Calculates the gravitational force between two masses.
        F = G * m1 * m2 / r^2
        :param m1: Mass of object 1 (kg)
        :param m2: Mass of object 2 (kg)
        :param r: Distance between the objects (m)
        :return: Gravitational force (N)
        """
        return G * m1 * m2 / r**2

    def orbital_velocity(self, M, r):
        """
        Calculates the orbital velocity of a body in orbit around a mass.
        v = sqrt(G * M / r)
        :param M: Mass of the central body (kg)
        :param r: Distance from the center of mass (m)
        :return: Orbital velocity (m/s)
        """
        return (G * M / r) ** 0.5

    def escape_velocity(self, M, r):
        """
        Calculates the escape velocity from a gravitational field.
        v_escape = sqrt(2 * G * M / r)
        :param M: Mass of the planet or star (kg)
        :param r: Distance from the center of the planet or star (m)
        :return: Escape velocity (m/s)
        """
        return (2 * G * M / r) ** 0.5

    def gravitational_field_strength(self, m1, r):
        """
        Calculates the gravitational field strength at a distance r from a mass m1.
        g = G * m1 / r^2
        :param m1: Mass of the object creating the gravitational field (kg)
        :param r: Distance from the center of the mass (m)
        :return: Gravitational field strength (N/kg)
        """
        return - ((G * m1) / r**2)

    def simulate_answer(self, question_type, **kwargs):
        """
        Simulates the answer to a given question based on the type.
        :param question_type: Type of question ('gravity', 'orbital_velocity', 'escape_velocity')
        :param kwargs: Parameters required for the calculation
        :return: Simulated answer (float)
        """
        if question_type == 'gravity':
            return self.gravitational_force(kwargs['m1'], kwargs['m2'], kwargs['r'])
        elif question_type == 'orbital_velocity':
            return self.orbital_velocity(kwargs['M'], kwargs['r'])
        elif question_type == 'escape_velocity':
            return self.escape_velocity(kwargs['M'], kwargs['r'])
        elif question_type == 'gravitational_field_strength':
            return self.gravitational_field_strength(kwargs['m1'], kwargs['r'])
        else:
            raise ValueError("Invalid question type")

class QuizSimulator:
    def __init__(self):
        self.physics_simulator = PhysicsSimulator()

    def start_quiz(self):
        print("Starting physics quiz...")
        self.ask_question()

    def generate_question(self):
        question_types = ['gravity', 'orbital_velocity', 'escape_velocity', 'gravitational_field_strength']
        question_type = random.choice(question_types)

        if question_type == 'gravity':
            question, answer, units = self.generate_gravity_question()
        elif question_type == 'orbital_velocity':
            question, answer, units = self.generate_orbital_velocity_question()
        elif question_type == 'escape_velocity':
            question, answer, units = self.generate_escape_velocity_question()
        else:
            question, answer, units = self.generate_gravitational_field_strength_question()

        return question, answer, units

    def generate_gravity_question(self):
        use_real_values = random.choice([True, False])
        all_planets = cursor.execute("SELECT * FROM planets WHERE name != 'Sun'").fetchall()
        random_planet = random.choice(all_planets)

        m1 = random.uniform(1e22, 1e25) if not use_real_values else 1.989e30  # Mass of the Sun
        m2 = random.uniform(1e22, 1e25) if not use_real_values else random_planet[2]  # Mass
        r = random.uniform(1e6, 1e9) if not use_real_values else random_planet[3]  # Radius
        if use_real_values:
            question = f"What is the gravitational force between the Sun ({standard_form_converter(1.989e30)} kg) and {random_planet[1]} ({standard_form_converter(random_planet[2])} kg)?"
        else:
            question = f"What is the gravitational force between two masses of {standard_form_converter(m1)} kg and {standard_form_converter(m2)} kg separated by {standard_form_converter(r)} meters?"
        answer = self.physics_simulator.gravitational_force(m1, m2, r)

        return question, answer, "N"

    def generate_orbital_velocity_question(self):
        use_real_values = random.choice([True, False])
        all_planets = cursor.execute("SELECT * FROM planets WHERE name != 'Sun'").fetchall()
        random_planet = random.choice(all_planets)

        M = random.uniform(1e30, 1e32) if not use_real_values else 1.989e30  # Mass of the Sun
        r = random.uniform(1e8, 1e10) if not use_real_values else random_planet[4]  # Orbital radius
        if use_real_values:
            question = f"What is the orbital velocity of {random_planet[1]} around the Sun ({standard_form_converter(1.989e30)} kg) at a distance of {standard_form_converter(random_planet[4])} meters?"
        else:
            question = f"What is the orbital velocity of a body in orbit around a mass of {standard_form_converter(M)} kg at a distance of {standard_form_converter(r)} meters?"
        answer = self.physics_simulator.orbital_velocity(M, r)

        return question, answer, "m/s"

    def generate_escape_velocity_question(self):
        use_real_values = random.choice([True, False])
        all_planets = cursor.execute("SELECT * FROM planets WHERE name != 'Sun'").fetchall()
        random_planet = random.choice(all_planets)

        M = random.uniform(1e30, 1e32) if not use_real_values else random_planet[2]  # Mass
        r = random.uniform(1e8, 1e10) if not use_real_values else random_planet[3]  # Radius
        if use_real_values:
            question = f"What is the escape velocity from {random_planet[1]} ({standard_form_converter(random_planet[2])} kg) at a distance of {standard_form_converter(random_planet[3])} meters?"
        else:
            question = f"What is the escape velocity from a mass of {standard_form_converter(M)} kg at a distance of {standard_form_converter(r)} meters?"
        answer = self.physics_simulator.escape_velocity(M, r)

        return question, answer, "m/s"

    def generate_gravitational_field_strength_question(self):
        use_real_values = random.choice([True, False])
        all_planets = cursor.execute("SELECT * FROM planets WHERE name != 'Sun'").fetchall()
        random_planet = random.choice(all_planets)

        m1 = random.uniform(1e22, 1e25) if not use_real_values else random_planet[2]  # Mass
        r = random.uniform(1e6, 1e9) if not use_real_values else random_planet[3]  # Radius
        if use_real_values:
            question = f"What is the gravitational field strength at a distance of {standard_form_converter(random_planet[3])} meters from {random_planet[1]} ({standard_form_converter(random_planet[2])} kg)?"
        else:
            question = f"What is the gravitational field strength at a distance of {standard_form_converter(r)} meters from a mass of {standard_form_converter(m1)} kg?"
        answer = self.physics_simulator.gravitational_field_strength(m1, r)

        return question, answer, "N/kg"

    def user_input_to_float(self, user_input):
        """Allows converting 10e10 or 1x10^10 or 1*10^-10 to a float."""
        user_input = user_input.replace('x', '*').replace('^', '**')
        number, exponent = user_input.split('*10**')
        return float(number) * 10 ** int(exponent)

    def ask_question(self):
        question, answer, units = self.generate_question()
        print(question)
        user_answer = input("Your answer: ")
        formatted = self.user_input_to_float(user_answer)
        isEqual = abs(formatted - answer) < 0.01
        print(f"Simulated Answer: {standard_form_converter(answer)} {units}")
        print(f"Your Answer: {user_answer} {'Correct' if isEqual else 'Incorrect'}")




# Example usage:
if __name__ == "__main__":
    quiz = QuizSimulator()
    quiz.start_quiz()
