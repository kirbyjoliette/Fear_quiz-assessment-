import tkinter as tk
import csv
import random
import datetime

# Load fears from CSV
with open("Fear_quiz_assessment/fear_list.csv", newline='') as f:
    reader = csv.reader(f)
    next(reader)  # Skip header
    fear_list = list(reader)

class FearQuiz:
    def __init__(self, parent):
        self.parent = parent
        self.parent.title("Fear Quiz")

        self.score = 0
        self.round = 0
        self.total_rounds = 5
        self.used_questions = []

        self.stats = []

        self.setup_gui()
        self.next_question()

    def setup_gui(self):
        self.main_frame = tk.Frame(self.parent, padx=20, pady=20)
        self.main_frame.pack()

        self.title_label = tk.Label(self.main_frame, text="Fear Quiz", font=("Arial", 24, "bold"))
        self.title_label.grid(row=0, column=0, columnspan=4, pady=(0, 20))

        self.question_label = tk.Label(self.main_frame, text="", font=("Arial", 14), wraplength=400)
        self.question_label.grid(row=1, column=0, columnspan=4, pady=(0, 10))

        self.buttons = []
        for i in range(4):
            btn = tk.Button(self.main_frame, text="", width=30, height=2, command=lambda i=i: self.check_answer(i))
            btn.grid(row=2 + i // 2, column=i % 2, padx=5, pady=5)
            self.buttons.append(btn)

        self.feedback_label = tk.Label(self.main_frame, text="", font=("Arial", 12))
        self.feedback_label.grid(row=4, column=0, columnspan=4)

        self.hint_button = tk.Button(self.main_frame, text="Hint", command=self.show_hint)
        self.hint_button.grid(row=5, column=0, pady=10)

        self.export_button = tk.Button(self.main_frame, text="Export Stats", command=self.export_stats)
        self.export_button.grid(row=5, column=1, pady=10)

        self.quit_button = tk.Button(self.main_frame, text="Quit", command=self.parent.quit)
        self.quit_button.grid(row=5, column=2, pady=10)

    def next_question(self):
        if self.round >= self.total_rounds:
            self.end_quiz()
            return

        self.round += 1
        self.feedback_label.config(text="")

        self.correct_pair = random.choice([pair for pair in fear_list if pair not in self.used_questions])
        self.used_questions.append(self.correct_pair)

        correct_answer = self.correct_pair[1]
        # Select 3 incorrect answers
        all_answers = [pair[1] for pair in random.sample(fear_list, 4)]
        if correct_answer not in all_answers:
            all_answers[random.randint(0, 3)] = correct_answer
        else:
            all_answers.remove(correct_answer)
            all_answers.append(correct_answer)
        random.shuffle(all_answers)

        self.question_label.config(text=f"Round {self.round}: What is {self.correct_pair[0]} the fear of?")
        for i in range(4):
            self.buttons[i].config(text=all_answers[i], state="normal")

        self.hint_shown = False

    def check_answer(self, index):
        selected = self.buttons[index].cget("text")
        correct = self.correct_pair[1]

        for btn in self.buttons:
            btn.config(state="disabled")

        if selected == correct:
            self.score += 1
            self.feedback_label.config(text="✅ Correct!", fg="green")
            result = "Correct"
        else:
            self.feedback_label.config(text=f"❌ Incorrect! It was '{correct}'.", fg="red")
            result = "Incorrect"

        self.stats.append({
            "Round": self.round,
            "Phobia": self.correct_pair[0],
            "Your Answer": selected,
            "Correct Answer": correct,
            "Result": result
        })

        self.parent.after(1500, self.next_question)

    def show_hint(self):
        if not self.hint_shown:
            hint_text = f"The answer starts with: {self.correct_pair[1][0]}"
            self.feedback_label.config(text=hint_text, fg="blue")
            self.hint_shown = True

    def end_quiz(self):
        self.question_label.config(text=f"Quiz complete! Your score: {self.score}/{self.total_rounds}")
        for btn in self.buttons:
            btn.config(state="disabled")
        self.hint_button.config(state="disabled")

    def export_stats(self):
        filename = f"fear_quiz_stats_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
        with open(filename, "w", newline='') as f:
            writer = csv.DictWriter(f, fieldnames=["Round", "Phobia", "Your Answer", "Correct Answer", "Result"])
            writer.writeheader()
            writer.writerows(self.stats)
        self.feedback_label.config(text=f"Stats exported to {filename}", fg="purple")

if __name__ == "__main__":
    root = tk.Tk()
    app = FearQuiz(root)
    root.mainloop()
