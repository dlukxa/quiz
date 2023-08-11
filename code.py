import tkinter as tk
from tkinter import messagebox
import random
import csv

class QuizGame(tk.Tk):
    def __init__(self, question_sets):
        super().__init__()
        self.title("Quiz Game")
        self.geometry("1000x600")
        self.configure(bg="lightgray")

        self.question_sets = question_sets
        self.user_scores = {}  # Dictionary to store user scores

        self.load_scores_from_file()  # Load previous scores from the CSV file

        self.current_user = None

        self.create_widgets()

    def create_widgets(self):
        self.welcome_label = tk.Label(self, text="Welcome to the Quiz Game!", font=("Arial", 16), bg="lightgray")
        self.welcome_label.pack(pady=50)

        self.name_label = tk.Label(self, text="Enter your name:", font=("Arial", 12), bg="lightgray")
        self.name_label.pack()

        self.name_entry = tk.Entry(self, font=("Arial", 12))
        self.name_entry.pack(pady=10)

        self.start_button = tk.Button(self, text="Start Quiz", font=("Arial", 12), command=self.start_quiz)
        self.start_button.pack()

        self.question_label = tk.Label(self, text="", font=("Arial", 16), wraplength=800, bg="lightgray")
        self.question_label.pack(pady=50)

        self.answer_buttons = []
        for i in range(4):
            button = tk.Button(self, text="", font=("Arial", 12), width=20, height=2, command=lambda idx=i: self.check_answer(idx))
            self.answer_buttons.append(button)

        self.result_label = tk.Label(self, text="", font=("Arial", 16), bg="lightgray")

        self.new_game_button = tk.Button(self, text="New Game", font=("Arial", 12), command=self.new_game, state=tk.DISABLED)
        self.new_game_button.pack()

        # New label for displaying the timer countdown
        self.timer_label = tk.Label(self, text="", font=("Arial", 16), bg="lightgray")
        self.timer_label.pack()

    def start_quiz(self):
        self.current_user = self.name_entry.get()
        if self.current_user.strip() == "":
            return
        self.welcome_label.destroy()
        self.name_label.destroy()
        self.name_entry.destroy()
        self.start_button.destroy()

        self.new_game_button.config(state=tk.DISABLED)
        
        random.shuffle(self.question_sets)
        self.question_sets = self.question_sets[:8]  # Select 8 random questions
        self.current_question = 0
        self.score = 0
        self.update_question()

    def update_question(self):
        if self.current_question < len(self.question_sets):
            question_set = self.question_sets[self.current_question]
            question_text = question_set[0][0]
            answers = question_set[1]

            # Update the question label with the current question text
            self.question_label.config(text=question_text)

            for i in range(4):
                self.answer_buttons[i].config(text=answers[i])
                self.answer_buttons[i].pack(pady=10)

            # Reset the timer value and start the countdown
            self.timer_value = 7
            self.update_timer()

            self.current_question += 1
        else:
            self.show_result()

    def update_timer(self):
        if self.timer_value >= 0:
            self.timer_label.config(text=f"Time Remaining: {self.timer_value} seconds")
            self.timer_label.after(1000, self.update_timer)
            self.timer_value -= 1
        else:
            # Time's up, consider it as a wrong answer
            self.check_answer(-1)

    def check_answer(self, selected_idx):
        # Stop the timer countdown
        self.timer_label.config(text="")

        correct_answer = self.question_sets[self.current_question - 1][2]
        if selected_idx == ord(correct_answer) - ord("A"):
            self.score += 1
        for button in self.answer_buttons:
            button.pack_forget()
        self.update_question()

    def show_result(self):
        percentage_correct = self.score * 100 / len(self.question_sets)
        self.user_scores[self.current_user] = percentage_correct

        # New result message with the user's name, percentage correct, and timer value
        result_text = f"Congratulations {self.current_user}, your marks for the Quiz is {percentage_correct:.2f}%."
        self.question_label.config(text=result_text)

        # Display the scoreboard details
        self.show_scoreboard()

        self.save_scores_to_file()  # Save updated scores to the CSV file

        self.new_game_button.config(state=tk.NORMAL)

    def load_scores_from_file(self):
        try:
            with open('scores.csv', newline='') as csvfile:
                reader = csv.reader(csvfile)
                for row in reader:
                    user, score = row
                    self.user_scores[user] = float(score)
        except FileNotFoundError:
            pass

    def save_scores_to_file(self):
        with open('scores.csv', 'w', newline='') as csvfile:
            writer = csv.writer(csvfile)
            for user, score in self.user_scores.items():
                writer.writerow([user, score])

    def show_scoreboard(self):
        sorted_scores = sorted(self.user_scores.items(), key=lambda x: x[1], reverse=True)
        scoreboard_text = "Scoreboard:\n\n"
        for idx, (user, score) in enumerate(sorted_scores[:5], 1):  # Show only top 5 users
            scoreboard_text += f"{idx}. {user}: {score:.2f}% correct answers\n"
        self.timer_label.config(text=scoreboard_text)

    def new_game(self):
        self.destroy()


def run_quiz_game():
    question_sets = [
        [["How many e are in the periodic table?"], ["A. 116", "B. 117", "C. 118", "D. 119"], "C"],
        [["Which animal lays the largest eggs?"], ["A. Whale", "B. Crocodile", "C. Elephant", "D. Ostrich"], "D"],
        [["What is the most abundant gas in Earth's atmosphere?"], ["A. Nitrogen", "B. Oxygen", "C. Carbon-Dioxide", "D. Hydrogen"], "A"],
        [["How many bones are in the human body?"], ["A. 206", "B. 207", "C. 208", "D. 209"], "A"],
        [["Which planet in the solar system is the hottest?"], ["A. Mercury", "B. Venus", "C. Earth", "D. Mars"], "B"],
        [["What is the capital of France?"], ["A. Paris", "B. London", "C. Rome", "D. Berlin"], "A"],
        [["Who painted the Mona Lisa?"], ["A. Michelangelo", "B. Leonardo da Vinci", "C. Vincent van Gogh", "D. Pablo Picasso"], "B"],
        [["What is the largest mammal on Earth?"], ["A. Elephant", "B. Blue Whale", "C. Giraffe", "D. Lion"], "B"],
        [["What is the chemical symbol for water?"], ["A. H2O", "B. CO2", "C. O2", "D. NaCl"], "A"],
        [["Which country is known as the Land of the Rising Sun?"], ["A. China", "B. Japan", "C. South Korea", "D. Thailand"], "B"],
        [["Which instrument is used to measure atmospheric pressure?"], ["A. Thermometer", "B. Barometer", "C. Hygrometer", "D. Anemometer"], "B"],
        [["What is the largest organ in the human body?"], ["A. Liver", "B. Heart", "C. Skin", "D. Kidney"], "C"],
        [["Which gas is essential for photosynthesis?"], ["A. Carbon monoxide", "B. Oxygen", "C. Carbon dioxide", "D. Nitrogen"], "C"],
        [["What is the chemical symbol for gold?"], ["A. Go", "B. Au", "C. Ag", "D. Gd"], "B"],
        [["Which planet is known as the Red Planet?"], ["A. Jupiter", "B. Saturn", "C. Mars", "D. Neptune"], "C"],
        [["What is the largest ocean on Earth?"], ["A. Atlantic Ocean", "B. Indian Ocean", "C. Arctic Ocean", "D. Pacific Ocean"], "D"],
        [["Who wrote the play 'Romeo and Juliet'?"], ["A. William Shakespeare", "B. Charles Dickens", "C. Jane Austen", "D. Mark Twain"], "A"],
        [["Which gas do plants absorb from the atmosphere?"], ["A. Oxygen", "B. Carbon dioxide", "C. Nitrogen", "D. Hydrogen"], "B"],
        [["What is the capital city of Brazil?"], ["A. Rio de Janeiro", "B. Sao Paulo", "C. Brasilia", "D. Salvador"], "C"],
        [["What is the chemical symbol for iron?"], ["A. Ir", "B. Fe", "C. In", "D. Au"], "B"],
        [["Which natural disaster is measured using the Richter scale?"], ["A. Hurricane", "B. Tornado", "C. Earthquake", "D. Tsunami"], "C"]
    ]

    app = QuizGame(question_sets)
    app.mainloop()

while True:
    run_quiz_game()
    restart = messagebox.askyesno("Quiz Game", "Do you want to play again?")
    if not restart:
        break
