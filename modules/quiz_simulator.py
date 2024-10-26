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
            question, answer = self.generate_gravity_question()
        elif question_type == 'orbital_velocity':
            question, answer = self.generate_orbital_velocity_question()
        elif question_type == 'escape_velocity':
            question, answer = self.generate_escape_velocity_question()
        else:
            question, answer = self.generate_gravitational_field_strength_question()

        return question, answer

    def generate_gravity_question(self):
        use_real_values = random.choice([True, False])
        all_planets = cursor.execute("SELECT * FROM planets WHERE name != 'Sun'").fetchall()
        random_planet = random.choice(all_planets)

        m1 = random.uniform(1e22, 1e25) if not use_real_values else 1.989e30  # Mass of the Sun
        m2 = random.uniform(1e22, 1e25) if not use_real_values else random_planet[2]
        r = random.uniform(1e6, 1e9) if not use_real_values else random_planet[3]
        if use_real_values:
            question = f"What is the gravitational force between the Sun (1.989e30 kg) and {random_planet[1]} ({random_planet[2]}kg)?"
        else:
            question = f"What is the gravitational force between two masses of {m1:.2e} kg and {m2:.2e} kg separated by {r:.2e} meters?"
        answer = self.physics_simulator.gravitational_force(m1, m2, r)

        return question, answer

    def generate_orbital_velocity_question(self):
        use_real_values = random.choice([True, False])
        all_planets = cursor.execute("SELECT * FROM planets WHERE name != 'Sun'").fetchall()
        random_planet = random.choice(all_planets)

        M = random.uniform(1e30, 1e32) if not use_real_values else 1.989e30  # Mass of the Sun
        r = random.uniform(1e8, 1e10) if not use_real_values else random_planet[3]
        if use_real_values:
            question = f"What is the orbital velocity of {random_planet[1]} around the Sun (1.989e30 kg) at a distance of {random_planet[3]} meters?"
        else:
            question = f"What is the orbital velocity of a body in orbit around a mass of {M:.2e} kg at a distance of {r:.2e} meters?"
        answer = self.physics_simulator.orbital_velocity(M, r)

        return question, answer

    def generate_escape_velocity_question(self):
        use_real_values = random.choice([True, False])
        all_planets = cursor.execute("SELECT * FROM planets WHERE name != 'Sun'").fetchall()
        random_planet = random.choice(all_planets)

        M = random.uniform(1e30, 1e32) if not use_real_values else random_planet[2]
        r = random.uniform(1e8, 1e10) if not use_real_values else random_planet[3]
        if use_real_values:
            question = f"What is the escape velocity from {random_planet[1]} ({random_planet[2]} kg) at a distance of {random_planet[3]} meters?"
        else:
            question = f"What is the escape velocity from a mass of {M:.2e} kg at a distance of {r:.2e} meters?"
        answer = self.physics_simulator.escape_velocity(M, r)

        return question, answer

    def generate_gravitational_field_strength_question(self):
        use_real_values = random.choice([True, False])
        all_planets = cursor.execute("SELECT * FROM planets WHERE name != 'Sun'").fetchall()
        random_planet = random.choice(all_planets)

        m1 = random.uniform(1e22, 1e25) if not use_real_values else random_planet[2]
        r = random.uniform(1e6, 1e9) if not use_real_values else random_planet[3]
        if use_real_values:
            question = f"What is the gravitational field strength at a distance of {random_planet[3]} meters from {random_planet[1]} ({random_planet[2]} kg)?"
        else:
            question = f"What is the gravitational field strength at a distance of {r:.2e} meters from a mass of {m1:.2e} kg?"
        answer = self.physics_simulator.gravitational_field_strength(m1, r)

        return question, answer

    def ask_question(self):
        # Example of a quiz question
        question = "What is the gravitational force between two masses of 5.97e24 kg and 7.35e22 kg separated by 384.4e6 meters?"
        print(question)

        # Simulate the answer using PhysicsSimulator
        answer = self.physics_simulator.simulate_answer(
            'gravity', m1=5.97e24, m2=7.35e22, r=384.4e6)

        print(f"Simulated Answer: {answer:.2e} N")

# Example usage:
if __name__ == "__main__":
    quiz = QuizSimulator()
    quiz.start_quiz()
