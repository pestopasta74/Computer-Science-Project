import tkinter as tk
from tkinter import messagebox, ttk
import random
import sqlite3
import json
import os
from datetime import datetime

# Constants
G = 6.67430 * 10 ** -11  # Gravitational constant (m^3 kg^-1 s^-2)
AU = 1.496 * 10 ** 11  # Astronomical unit (m)

def standard_form_converter(num):
    """Given a number in base units, returns the number in standard form."""
    num_str = f"{num:.2e}"
    base, exponent = num_str.split('e')
    return f"{base} x 10^{int(exponent)}"

def parse_standard_form(input_str):
    """Parse standard form input like '1.5 x 10^23' into a float."""
    try:
        # Remove any whitespace
        input_str = input_str.replace(' ', '')

        # Split into base and exponent parts
        parts = input_str.lower().split('x10^')
        base = float(parts[0])
        exponent = int(parts[1])

        return base * (10 ** exponent)
    except (ValueError, IndexError):
        return None

class PhysicsSimulator:
    def __init__(self):
        pass

    def gravitational_force(self, m1, m2, r):
        """Calculates the gravitational force between two masses."""
        return G * m1 * m2 / r**2

    def orbital_velocity(self, M, r):
        """Calculates the orbital velocity of a body in orbit around a mass."""
        return (G * M / r) ** 0.5

    def escape_velocity(self, M, r):
        """Calculates the escape velocity from a gravitational field."""
        return (2 * G * M / r) ** 0.5

    def gravitational_field_strength(self, m1, r):
        """Calculates the gravitational field strength at a distance r from a mass m1."""
        return - ((G * m1) / r**2)

class QuizApp:
    def __init__(self, master):
        self.master = master
        master.title("Physics Quiz")
        master.geometry("600x500")

        # Physics simulator
        self.physics_simulator = PhysicsSimulator()

        # Database connection
        self.conn = sqlite3.connect('database.db')
        self.cursor = self.conn.cursor()

        # Quiz variables
        self.current_question = 0
        self.questions = []
        self.user_answers = []
        self.correct_answers = []

        # Generate 10 questions
        self.generate_questions()

        # Setup initial UI
        self.setup_start_screen()

    def generate_questions(self):
        """Generate 10 random physics questions"""
        question_types = ['gravity', 'orbital_velocity', 'escape_velocity', 'gravitational_field_strength']

        for _ in range(10):
            question_type = random.choice(question_types)

            if question_type == 'gravity':
                question, answer, units = self.generate_gravity_question()
            elif question_type == 'orbital_velocity':
                question, answer, units = self.generate_orbital_velocity_question()
            elif question_type == 'escape_velocity':
                question, answer, units = self.generate_escape_velocity_question()
            else:
                question, answer, units = self.generate_gravitational_field_strength_question()

            self.questions.append({
                'type': question_type,
                'question': question,
                'correct_answer': answer,
                'units': units
            })

    def generate_gravity_question(self):
        use_real_values = random.choice([True, False])
        all_planets = self.cursor.execute("SELECT * FROM planets WHERE name != 'Sun'").fetchall()
        random_planet = random.choice(all_planets)

        m1 = random.uniform(1e22, 1e25) if not use_real_values else 1.989e30
        m2 = random.uniform(1e22, 1e25) if not use_real_values else random_planet[2]
        r = random.uniform(1e6, 1e9) if not use_real_values else random_planet[3]

        if use_real_values:
            question = f"What is the gravitational force between the Sun ({standard_form_converter(1.989e30)} kg) and {random_planet[1]} ({standard_form_converter(random_planet[2])} kg)?"
        else:
            question = f"What is the gravitational force between two masses of {standard_form_converter(m1)} kg and {standard_form_converter(m2)} kg separated by {standard_form_converter(r)} meters?"

        answer = self.physics_simulator.gravitational_force(m1, m2, r)
        return question, answer, ["N", "N (Newton)"]

    def generate_orbital_velocity_question(self):
        use_real_values = random.choice([True, False])
        all_planets = self.cursor.execute("SELECT * FROM planets WHERE name != 'Sun'").fetchall()
        random_planet = random.choice(all_planets)

        M = random.uniform(1e30, 1e32) if not use_real_values else 1.989e30
        r = random.uniform(1e8, 1e10) if not use_real_values else random_planet[4]

        if use_real_values:
            question = f"What is the orbital velocity of {random_planet[1]} around the Sun ({standard_form_converter(1.989e30)} kg) at a distance of {standard_form_converter(random_planet[4])} meters?"
        else:
            question = f"What is the orbital velocity of a body in orbit around a mass of {standard_form_converter(M)} kg at a distance of {standard_form_converter(r)} meters?"

        answer = self.physics_simulator.orbital_velocity(M, r)
        return question, answer, ["m/s", "meters/second"]

    def generate_escape_velocity_question(self):
        use_real_values = random.choice([True, False])
        all_planets = self.cursor.execute("SELECT * FROM planets WHERE name != 'Sun'").fetchall()
        random_planet = random.choice(all_planets)

        M = random.uniform(1e30, 1e32) if not use_real_values else random_planet[2]
        r = random.uniform(1e8, 1e10) if not use_real_values else random_planet[3]

        if use_real_values:
            question = f"What is the escape velocity from {random_planet[1]} ({standard_form_converter(random_planet[2])} kg) at a distance of {standard_form_converter(random_planet[3])} meters?"
        else:
            question = f"What is the escape velocity from a mass of {standard_form_converter(M)} kg at a distance of {standard_form_converter(r)} meters?"

        answer = self.physics_simulator.escape_velocity(M, r)
        return question, answer, ["m/s", "meters/second"]

    def generate_gravitational_field_strength_question(self):
        use_real_values = random.choice([True, False])
        all_planets = self.cursor.execute("SELECT * FROM planets WHERE name != 'Sun'").fetchall()
        random_planet = random.choice(all_planets)

        m1 = random.uniform(1e22, 1e25) if not use_real_values else random_planet[2]
        r = random.uniform(1e6, 1e9) if not use_real_values else random_planet[3]

        if use_real_values:
            question = f"What is the gravitational field strength at a distance of {standard_form_converter(random_planet[3])} meters from {random_planet[1]} ({standard_form_converter(random_planet[2])} kg)?"
        else:
            question = f"What is the gravitational field strength at a distance of {standard_form_converter(r)} meters from a mass of {standard_form_converter(m1)} kg?"

        answer = self.physics_simulator.gravitational_field_strength(m1, r)
        return question, answer, ["N/kg", "Newtons/kg"]

    def setup_start_screen(self):
        """Create the start screen for the quiz"""
        # Clear any existing widgets
        for widget in self.master.winfo_children():
            widget.destroy()

        # Title
        title_label = tk.Label(self.master, text="Physics Quiz", font=("Helvetica", 24, "bold"))
        title_label.pack(pady=20)

        # Description
        desc_label = tk.Label(self.master, text="Test your knowledge of physics concepts!", font=("Helvetica", 16))
        desc_label.pack(pady=10)

        # Start Button
        start_button = tk.Button(self.master, text="Start Quiz", command=self.start_quiz)
        start_button.pack(pady=20)

    def start_quiz(self):
        """Start the quiz by showing the first question"""
        self.current_question = 0
        self.user_answers = []
        self.correct_answers = []
        self.show_question()

    def show_question(self):
        """Display the current question"""
        # Clear previous widgets
        for widget in self.master.winfo_children():
            widget.destroy()

        # Current question
        question_data = self.questions[self.current_question]

        # Question label
        question_label = tk.Label(self.master, text=question_data['question'], wraplength=500, font=("Helvetica", 16))
        question_label.pack(pady=20)

        # Answer input frame
        answer_frame = tk.Frame(self.master)
        answer_frame.pack(pady=10)

        # Answer entry
        tk.Label(answer_frame, text="Answer:").pack(side=tk.LEFT)
        self.answer_entry = tk.Entry(answer_frame, width=20)
        self.answer_entry.pack(side=tk.LEFT, padx=5)

        # Unit dropdown
        tk.Label(answer_frame, text="Units:").pack(side=tk.LEFT)
        self.unit_var = tk.StringVar()
        self.unit_dropdown = ttk.Combobox(answer_frame, textvariable=self.unit_var, values=question_data['units'], state="readonly", width=15)
        self.unit_dropdown.set(question_data['units'][0])
        self.unit_dropdown.pack(side=tk.LEFT, padx=5)

        # Navigation buttons
        button_frame = tk.Frame(self.master)
        button_frame.pack(pady=10)

        prev_button = tk.Button(button_frame, text="Previous",
                                command=self.previous_question,
                                state=tk.NORMAL if self.current_question > 0 else tk.DISABLED)
        prev_button.pack(side=tk.LEFT, padx=5)

        next_button = tk.Button(button_frame, text="Next",
                                command=self.next_question)
        next_button.pack(side=tk.LEFT, padx=5)

        # Question counter
        counter_label = tk.Label(self.master,
                                 text=f"Question {self.current_question + 1} of {len(self.questions)}")
        counter_label.pack(pady=10)

    def next_question(self):
        """Move to the next question or submit quiz"""
        # Save current answer
        try:
            # Try parsing standard form first
            user_input = parse_standard_form(self.answer_entry.get())

            # If standard form parsing fails, try float conversion
            if user_input is None:
                user_input = float(self.answer_entry.get())

            self.user_answers.append(user_input)
        except ValueError:
            messagebox.showerror("Error", "Please enter a valid number or standard form (e.g., 1.5 x 10^23).")
            return

        # Move to next question or submit quiz
        self.current_question += 1
        if self.current_question < len(self.questions):
            self.show_question()
        else:
            self.submit_quiz()

    def previous_question(self):
        """Move to the previous question"""
        if self.current_question > 0:
            # Save current answer if possible
            try:
                # Try parsing standard form first
                user_input = parse_standard_form(self.answer_entry.get())

                # If standard form parsing fails, try float conversion
                if user_input is None:
                    user_input = float(self.answer_entry.get())

                self.user_answers.append(user_input)
            except ValueError:
                pass

            self.current_question -= 1
            self.show_question()

    def submit_quiz(self):
        """Submit the quiz and show results"""
        # Evaluate answers
        score = 0
        wrong_questions = []

        for i, (question, user_answer) in enumerate(zip(self.questions, self.user_answers)):
            correct_answer = question['correct_answer']

            # Check if answer is within 1% of correct answer
            if abs(user_answer - correct_answer) / correct_answer < 0.01:
                score += 1
            else:
                wrong_questions.append({
                    'question': question['question'],
                    'correct_answer': standard_form_converter(correct_answer),
                    'user_answer': standard_form_converter(user_answer),
                    'units': question['units'][0]
                })

        # Calculate score percentage
        score_percentage = (score / len(self.questions)) * 100

        # Save quiz results to JSON
        quiz_results = {
            'date': datetime.now().isoformat(),
            'score': score,
            'total_questions': len(self.questions),
            'score_percentage': score_percentage,
            'wrong_questions': wrong_questions
        }

        # Create results directory if it doesn't exist
        os.makedirs('quiz_results', exist_ok=True)

        # Save results to JSON file
        results_filename = f"quiz_results/quiz_result_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        with open(results_filename, 'w') as f:
            json.dump(quiz_results, f, indent=4)

        # Clear previous widgets
        for widget in self.master.winfo_children():
            widget.destroy()

        # Results screen
        results_label = tk.Label(self.master,
                                 text=f"Quiz Completed!\nScore: {score}/{len(self.questions)} ({score_percentage:.1f}%)",
                                 font=("Helvetica", 20, "bold"))
        results_label.pack(pady=20)

        # Wrong questions button
        wrong_questions_button = tk.Button(self.master,
                                           text="View Wrong Questions",
                                           command=lambda: self.show_wrong_questions(wrong_questions))
        wrong_questions_button.pack(pady=10)

        # Restart quiz button
        restart_button = tk.Button(self.master, text="Take Another Quiz", command=self.setup_start_screen)
        restart_button.pack(pady=10)

    def show_wrong_questions(self, wrong_questions):
        """Display the wrong questions in a new window"""
        wrong_questions_window = tk.Toplevel(self.master)
        wrong_questions_window.title("Wrong Questions")
        wrong_questions_window.geometry("600x500")

        # Title
        title_label = tk.Label(wrong_questions_window,
                               text="Wrong Questions Review",
                               font=("Helvetica", 20, "bold"))
        title_label.pack(pady=10)

        # Scrollbar for wrong questions
        canvas = tk.Canvas(wrong_questions_window)
        scrollbar = tk.Scrollbar(wrong_questions_window, orient="vertical", command=canvas.yview)
        scrollable_frame = tk.Frame(canvas)

        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(
                scrollregion=canvas.bbox("all")
            )
        )

        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)

        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        # Display each wrong question
        for i, q in enumerate(wrong_questions, 1):
            question_frame = tk.Frame(scrollable_frame)
            question_frame.pack(pady=5, fill='x')

            # Question details
            tk.Label(question_frame, text=f"Question {i}: {q['question']}", wraplength=500, justify=tk.LEFT, anchor='w').pack(anchor='w')
            tk.Label(question_frame, text=f"Your Answer: {q['user_answer']} {q['units']}", fg='red').pack(anchor='w')
            tk.Label(question_frame, text=f"Correct Answer: {q['correct_answer']} {q['units']}", fg='green').pack(anchor='w')

            # Separator
            tk.Frame(question_frame, height=1, bd=1, relief=tk.SUNKEN).pack(fill='x', pady=5)

    def run(self):
        """Run the quiz application"""
        self.master.mainloop()


def main():
    try:
        # Create root window
        root = tk.Tk()

        # Verify database connection
        conn = sqlite3.connect('database.db')
        cursor = conn.cursor()

        # Check if planets table exists and has data
        cursor.execute("SELECT COUNT(*) FROM planets")
        planet_count = cursor.fetchone()[0]

        if planet_count == 0:
            messagebox.showwarning("Warning", "Planets table is empty. Some quiz features may not work correctly.")

        # Create the quiz app and run it
        quiz_app = QuizApp(root)
        root.mainloop()

    except sqlite3.OperationalError:
        messagebox.showerror("Database Error", "Could not connect to the database.\nPlease ensure 'database.db' exists and contains a 'planets' table.")
    except Exception as e:
        messagebox.showerror("Unexpected Error", f"An unexpected error occurred: {e}")
    finally:
        # Close database connection if it was opened
        if 'conn' in locals():
            conn.close()

if __name__ == "__main__":
    main()