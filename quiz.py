import tkinter as tk
import customtkinter as ctk
from tkinter import messagebox, ttk
import sqlite3
import random
import json
import os
import datetime
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

# Constants
G = 6.67430 * 10 ** -11  # Gravitational constant (m^3 kg^-1 s^-2)
AU = 1.496 * 10 ** 11  # Astronomical unit (m)

# Configure CustomTkinter
ctk.set_appearance_mode("light")
ctk.set_default_color_theme("blue")

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

class DatabaseManager:
    @staticmethod
    def init_database():
        """Initialize the database with necessary tables."""
        conn = sqlite3.connect('database.db')
        cursor = conn.cursor()

        # Create users table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS users (
                username TEXT PRIMARY KEY,
                password TEXT NOT NULL,
                role TEXT NOT NULL
            )
        ''')

        # Create planets table if not exists (for quiz questions)
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS planets (
                name TEXT PRIMARY KEY,
                mass REAL,
                radius REAL,
                orbital_distance REAL
            )
        ''')

        # Insert some default planets if table is empty
        cursor.execute("SELECT COUNT(*) FROM planets")
        if cursor.fetchone()[0] == 0:
            default_planets = [
                ('Sun', 1.989e30, 6.957e8, 0),
                ('Mercury', 3.3011e23, 2.4397e6, 5.79e10),
                ('Venus', 4.8675e24, 6.0518e6, 1.082e11),
                ('Earth', 5.97237e24, 6.371e6, 1.496e11),
                ('Mars', 6.4171e23, 3.3895e6, 2.279e11),
                ('Jupiter', 1.8982e27, 6.9911e7, 7.786e11),
                ('Saturn', 5.6834e26, 5.8232e7, 1.434e12),
                ('Uranus', 8.6810e25, 2.5362e7, 2.871e12),
                ('Neptune', 1.02413e26, 2.4622e7, 4.495e12)
            ]
            cursor.executemany(
                'INSERT INTO planets VALUES (?,?,?,?)',
                default_planets
            )

        conn.commit()
        conn.close()

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

class LoginPage:
    def __init__(self, master):
        self.master = master
        master.title("Physics Quiz Login")
        master.geometry("400x500")

        # Ensure database is initialized
        DatabaseManager.init_database()

        # Main frame
        self.frame = ctk.CTkFrame(master, corner_radius=15)
        self.frame.pack(pady=20, padx=20, fill="both", expand=True)

        # Title
        title_label = ctk.CTkLabel(
            self.frame,
            text="Physics Quiz Login",
            font=("Segoe UI", 24, "bold")
        )
        title_label.pack(pady=(40, 20))

        # Username
        self.username_entry = ctk.CTkEntry(
            self.frame,
            placeholder_text="Username",
            width=300
        )
        self.username_entry.pack(pady=10)

        # Password
        self.password_entry = ctk.CTkEntry(
            self.frame,
            placeholder_text="Password",
            show="*",
            width=300
        )
        self.password_entry.pack(pady=10)

        # Login Button
        login_button = ctk.CTkButton(
            self.frame,
            text="Login",
            command=self.login,
            width=300
        )
        login_button.pack(pady=10)

        # Register Button
        register_button = ctk.CTkButton(
            self.frame,
            text="Register",
            command=self.register,
            width=300,
            fg_color="green"
        )
        register_button.pack(pady=10)

    def login(self):
        username = self.username_entry.get()
        password = self.password_entry.get()

        conn = sqlite3.connect('database.db')
        cursor = conn.cursor()

        cursor.execute(
            'SELECT role FROM users WHERE username = ? AND password = ?',
            (username, password)
        )
        result = cursor.fetchone()
        conn.close()

        if result:
            role = result[0]
            self.master.destroy()

            root = ctk.CTk()
            if role == 'student':
                quiz_app = QuizApp(root, username)
            else:  # teacher
                results_app = TeacherResultsPage(root)
            root.mainloop()
        else:
            messagebox.showerror("Login Failed", "Invalid username or password")

    def register(self):
        username = self.username_entry.get()
        password = self.password_entry.get()

        if not username or not password:
            messagebox.showerror("Registration Failed", "Username and password cannot be empty")
            return

        conn = sqlite3.connect('database.db')
        cursor = conn.cursor()

        try:
            cursor.execute(
                'INSERT INTO users (username, password, role) VALUES (?, ?, ?)',
                (username, password, 'student')  # Default role is student
            )
            conn.commit()
            messagebox.showinfo("Registration Successful", "You can now log in")
        except sqlite3.IntegrityError:
            messagebox.showerror("Registration Failed", "Username already exists")
        finally:
            conn.close()

class QuizApp:
    def __init__(self, master, username):
        self.master = master
        self.username = username
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

        # Ensure results directory exists
        os.makedirs('quiz_results', exist_ok=True)

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
            'username': self.username,
            'date': datetime.datetime.now().isoformat(),
            'score': score,
            'total_questions': len(self.questions),
            'score_percentage': score_percentage,
            'wrong_questions': wrong_questions
        }

        # Save results to JSON file
        results_filename = f"quiz_results/quiz_result_{self.username}_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        with open(results_filename, 'w') as f:
            json.dump(quiz_results, f, indent=4)

        # Clear previous widgets
        for widget in self.master.winfo_children():
            widget.destroy()

        # Results screen
        results_label = ctk.CTkLabel(
            self.master,
            text=f"Quiz Completed!\nScore: {score}/{len(self.questions)} ({score_percentage:.1f}%)",
            font=("Helvetica", 20, "bold")
        )
        results_label.pack(pady=20)

        # Restart quiz button
        restart_button = ctk.CTkButton(
            self.master,
            text="Take Another Quiz",
            command=self.setup_start_screen
        )
        restart_button.pack(pady=10)

class TeacherResultsPage:
    def __init__(self, master):
        # Configure main window
        self.master = master
        master.title("Physics Quiz Analytics Dashboard")
        master.geometry("1400x800")

        # Color scheme
        self.colors = {
            'primary': '#3498db',
            'secondary': '#2ecc71',
            'text_dark': '#2c3e50',
            'background_light': '#f0f0f0'
        }

        # Results directory
        self.results_dir = 'quiz_results'
        if not os.path.exists(self.results_dir):
            messagebox.showwarning("Warning", f"Results directory '{self.results_dir}' not found.")
            os.makedirs(self.results_dir)

        # Cache for students and results to reduce file I/O
        self.student_cache = None
        self.results_cache = {}

        # Create UI
        self.create_ui()

    def create_ui(self):
        # Main container
        self.main_container = ctk.CTkFrame(self.master, corner_radius=10)
        self.main_container.pack(fill="both", expand=True, padx=10, pady=10)

        # Title
        title_label = ctk.CTkLabel(
            self.main_container,
            text="Physics Quiz Analytics",
            font=("Segoe UI", 24, "bold")
        )
        title_label.pack(pady=(20, 10))

        # Content frame
        content_frame = ctk.CTkFrame(self.main_container)
        content_frame.pack(fill="both", expand=True, padx=10, pady=10)

        # Left side - Student List
        left_frame = ctk.CTkFrame(content_frame, width=300)
        left_frame.pack(side="left", fill="y", padx=(0, 10))

        # Search entry
        self.search_var = ctk.StringVar()
        search_entry = ctk.CTkEntry(
            left_frame,
            textvariable=self.search_var,
            placeholder_text="Search Students"
        )
        search_entry.pack(fill="x", padx=10, pady=(10, 5))
        search_entry.bind('<KeyRelease>', self.filter_students)

        # Student listbox with scrollbar
        self.student_listbox = ctk.CTkScrollableFrame(left_frame)
        self.student_listbox.pack(fill="both", expand=True, padx=10, pady=10)

        self.student_buttons = []
        self.populate_students()

        # Right side - Details and Graphs
        self.right_frame = ctk.CTkTabview(content_frame)
        self.right_frame.pack(side="right", fill="both", expand=True, padx=(10, 0))

        # Create tabs
        self.performance_tab = self.right_frame.add("Performance")
        self.details_tab = self.right_frame.add("Detailed Results")
        self.wrong_questions_tab = self.right_frame.add("Wrong Questions")

    def populate_students(self):
        # Clear existing buttons
        for btn in self.student_buttons:
            btn.destroy()
        self.student_buttons.clear()

        # Collect students efficiently
        if self.student_cache is None:
            students = set()
            for filename in os.listdir(self.results_dir):
                if filename.endswith('.json'):
                    try:
                        username = filename.split('_')[2]
                        students.add(username)
                    except IndexError:
                        continue
            self.student_cache = sorted(students)

        # Create buttons for each student
        for student in self.student_cache:
            btn = ctk.CTkButton(
                self.student_listbox,
                text=student,
                command=lambda s=student: self.show_student_details(s),
                width=250
            )
            btn.pack(pady=5)
            self.student_buttons.append(btn)

    def filter_students(self, event=None):
        search_term = self.search_var.get().lower()

        # Clear existing buttons
        for btn in self.student_buttons:
            btn.destroy()
        self.student_buttons.clear()

        # Filter students
        filtered_students = [
            student for student in self.student_cache
            if search_term in student.lower()
        ]

        # Create buttons for filtered students
        for student in filtered_students:
            btn = ctk.CTkButton(
                self.student_listbox,
                text=student,
                command=lambda s=student: self.show_student_details(s),
                width=250
            )
            btn.pack(pady=5)
            self.student_buttons.append(btn)

    def get_student_results(self, student: str):
        # Use cache to reduce file I/O
        if student not in self.results_cache:
            student_results = []
            for filename in os.listdir(self.results_dir):
                if filename.endswith('.json') and student in filename:
                    with open(os.path.join(self.results_dir, filename), 'r') as f:
                        student_results.append(json.load(f))

            # Sort results by date
            student_results.sort(key=lambda x: x['date'])
            self.results_cache[student] = student_results

        return self.results_cache[student]

    def show_student_details(self, student: str):
        # Clear previous content in tabs
        for tab in [self.performance_tab, self.details_tab, self.wrong_questions_tab]:
            for widget in tab.winfo_children():
                widget.destroy()

        # Get student results
        student_results = self.get_student_results(student)

        # Performance Tab
        self.create_performance_graph(student, student_results)

        # Detailed Results Tab
        self.create_detailed_results(student_results)

        # Wrong Questions Tab
        self.create_wrong_questions(student_results)

    def create_performance_graph(self, student: str, student_results):
        # Create figure for performance graphs
        fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(10, 8))

        # Scores over time
        dates = [datetime.datetime.fromisoformat(result['date']).strftime('%Y-%m-%d') for result in student_results]
        scores = [result['score_percentage'] for result in student_results]

        ax1.plot(dates, scores, marker='o', color=self.colors['primary'])
        ax1.set_title(f"{student}'s Quiz Performance", fontsize=16)
        ax1.set_xlabel("Quiz Date", fontsize=12)
        ax1.set_ylabel("Score (%)", fontsize=12)
        plt.setp(ax1.get_xticklabels(), rotation=45, ha='right')

        # Wrong question distribution
        wrong_questions_count = sum(len(result['wrong_questions']) for result in student_results)
        total_questions_count = sum(result['total_questions'] for result in student_results)

        ax2.pie([wrong_questions_count, total_questions_count - wrong_questions_count],
                colors=[self.colors['primary'], self.colors['secondary']],
                labels=['Wrong Questions', 'Correct Questions'],
                autopct='%1.1f%%')
        ax2.set_title("Overall Question Accuracy", fontsize=16)

        plt.tight_layout()

        # Embed matplotlib figure in CustomTkinter
        canvas = FigureCanvasTkAgg(fig, master=self.performance_tab)
        canvas_widget = canvas.get_tk_widget()
        canvas_widget.pack(fill="both", expand=True)

    def create_detailed_results(self, student_results):
        # Use standard Tkinter Treeview inside CTkFrame
        frame = ctk.CTkFrame(self.details_tab)
        frame.pack(fill="both", expand=True, padx=10, pady=10)

        # Scrollbar for Treeview
        scrollbar = ctk.CTkScrollbar(frame)
        scrollbar.pack(side="right", fill="y")

        # Create a standard Tkinter Treeview
        results_tree = ttk.Treeview(
            frame,
            columns=('Date', 'Score', 'Total Questions', 'Percentage'),
            show='headings',
            yscrollcommand=scrollbar.set
        )

        # Configure Treeview columns
        results_tree.heading('Date', text='Date')
        results_tree.heading('Score', text='Score')
        results_tree.heading('Total Questions', text='Total Questions')
        results_tree.heading('Percentage', text='Percentage')

        results_tree.column('Date', anchor='center', width=150)
        results_tree.column('Score', anchor='center', width=100)
        results_tree.column('Total Questions', anchor='center', width=120)
        results_tree.column('Percentage', anchor='center', width=100)

        # Populate treeview with quiz results
        for result in student_results:
            results_tree.insert('', 'end', values=(
                datetime.datetime.fromisoformat(result['date']).strftime('%Y-%m-%d %H:%M'),
                f"{result['score']}/{result['total_questions']}",
                result['total_questions'],
                f"{result['score_percentage']:.1f}%"
            ))

        # Configure scrollbar
        scrollbar.configure(command=results_tree.yview)

        # Pack Treeview
        results_tree.pack(side="left", fill="both", expand=True)

    def create_wrong_questions(self, student_results):
        # Create a frame with scrollbar
        frame = ctk.CTkFrame(self.wrong_questions_tab)
        frame.pack(fill="both", expand=True, padx=10, pady=10)

        # Standard Tkinter Text widget inside CTkFrame
        text_widget = tk.Text(
            frame,
            wrap="word",
            font=("Consolas", 12),
            yscrollcommand=tk.Scrollbar(frame).set
        )
        text_widget.pack(side="left", fill="both", expand=True)

        # Add scrollbar
        scrollbar = ctk.CTkScrollbar(frame, command=text_widget.yview)
        scrollbar.pack(side="right", fill="y")
        text_widget.configure(yscrollcommand=scrollbar.set)

        # Populate wrong questions
        for result in student_results:
            for q in result['wrong_questions']:
                text_widget.insert("end",
                    f"Date: {datetime.datetime.fromisoformat(result['date']).strftime('%Y-%m-%d %H:%M')}\n"
                    f"Question: {q['question']}\n"
                    f"Your Answer: {q['user_answer']}\n"
                    f"Correct Answer: {q['correct_answer']}\n\n"
                )

        text_widget.configure(state="disabled")

    def get_student_results(self, student: str):
        """Retrieve all quiz results for a specific student"""
        if student not in self.results_cache:
            student_results = []
            for filename in os.listdir(self.results_dir):
                if filename.endswith('.json') and f"quiz_result_{student}_" in filename:
                    with open(os.path.join(self.results_dir, filename), 'r') as f:
                        student_results.append(json.load(f))

            # Sort results by date
            student_results.sort(key=lambda x: x['date'])
            self.results_cache[student] = student_results

        return self.results_cache[student]

def main():
    root = ctk.CTk()
    login_page = LoginPage(root)
    root.mainloop()

if __name__ == "__main__":
    main()