import tkinter as tk
from tkinter import ttk, messagebox
import random

# --- Data ---
questions_easy = {
    "Arachnophobia": "🕷Spider",
    "Acrophobia": "🏔Heights",
    "Cynophobia": "🐶Dogs",
    "Ophidiophobia": "🐍Snakes",
    "Trypanophobia": "💉Needles"
}

questions_hard = {
    "Nomophobia": "📱Being without a phone",
    "Atychiphobia": "❌Failure",
    "Taphophobia": "⚰️Being buried alive",
    "Chronophobia": "⏰Time",
    "Philophobia": "❤️Love"
}

options = {
    "Arachnophobia": ["🕷Spider", "🦇Bats", "🌊Water", "⚡Thunder"],
    "Acrophobia": ["🧼Soap", "🏔Heights", "🔥Fire", "💦Drowning"],
    "Cynophobia": ["🐱Cats", "🐶Dogs", "🐍Snakes", "🦇Bats"],
    "Ophidiophobia": ["🌊Water", "🕷Spider", "🐍Snakes", "🦇Bats"],
    "Transphobia": ["⚡Thunder", "💉Needles", "🐶Dogs", "🧼Soap"],
    "Homophobia": ["🚪Open spaces", "📱Being without a phone", "❤️Love", "👻Ghosts"],
    "Atychiphobia": ["🕷Spider", "🐶Dogs", "❌Failure", "🎤Public speaking"],
    "Taphophobia": ["😴Sleep", "⚰️Being buried alive", "⏳Aging", "💦Drowning"],
    "Chronophobia": ["🧼Soap", "🦇Bats", "⏰Time", "🐱Cats"],
    "Philophobia": ["🕷Spider", "🐶Dogs", "❤️Love", "🌪Storms"]
}

# --- Global Variables ---
score = 0
hints_used = 0
current_question = ""
total_questions = 0
asked_questions = []
level = "Easy"


# --- Functions ---

def start_quiz():
    global total_questions, level, score, asked_questions, hints_used
    try:
        total_questions = int(num_questions_entry.get())
        if total_questions <= 0:
            raise ValueError
    except ValueError:
        error_label.config(text="⚠️ Oops - Please choose a whole number more than zero")
        return

    level = level_dropdown.get()
    if level not in ["Easy", "Hard"]:
        error_label.config(text="⚠️ Please choose a level")
        return

    score = 0
    hints_used = 0
    asked_questions = []

    start_frame.pack_forget()
    quiz_frame.pack()
    next_question()


def next_question():
    global current_question
    question_pool = questions_easy if level == "Easy" else questions_hard
    remaining_questions = list(set(question_pool.keys()) - set(asked_questions))

    if not remaining_questions or len(asked_questions) >= total_questions:
        end_game()
        return

    current_question = random.choice(remaining_questions)
    asked_questions.append(current_question)

    question_label.config(text=f"What is {current_question}?")
    round_label.config(text=f"Round {len(asked_questions)}")

    # Reset buttons
    for btn in answer_buttons:
        btn.config(state="normal", bg="#a89cc8")
        btn.deselect()

    opts = options[current_question]
    random.shuffle(opts)
    for i in range(4):
        answer_buttons[i].config(text=opts[i])


def submit_answer():
    global score
    selected = None
    for btn in answer_buttons:
        if btn.var.get():
            selected = btn.cget("text")
            break

    if not selected:
        messagebox.showinfo("Error", "Please select an answer!")
        return

    correct_answer = questions_easy[current_question] if level == "Easy" else questions_hard[current_question]
    if selected == correct_answer:
        score += 10
    else:
        score -= 5

    next_question()


def use_hint():
    global hints_used, score
    for btn in answer_buttons:
        if btn.cget("text") != (questions_easy if level == "Easy" else questions_hard)[current_question]:
            btn.config(state="disabled")
    score -= 2
    hints_used += 1


def end_game():
    quiz_frame.pack_forget()
    messagebox.showinfo("Game Over", f"Quiz complete!\nScore: {score}\nHints used: {hints_used}")
    start_frame.pack()


def show_stats():
    messagebox.showinfo("Statistics",
                        f"Score: {score}\nHints used: {hints_used}\nQuestions answered: {len(asked_questions)}")


# --- GUI Setup ---
root = tk.Tk()
root.title("Fear Quiz")
root.config(bg="#5a4e8d")
root.geometry("600x400")
root.resizable(False, False)

# --- Start Frame ---
start_frame = tk.Frame(root, bg="#5a4e8d")
start_frame.pack()

tk.Label(start_frame, text="Fear Quiz 👾", font=("Helvetica", 24, "bold"), fg="lavender", bg="#5a4e8d").pack(pady=10)
tk.Label(start_frame,
         text="In this quiz, you'll be shown the name of a phobia and must choose the correct answer from the given "
              "options.\nEach correct answer earns points, but using hints will reduce your final score.\nYour goal "
              "is to get the highest score possible. Ready to test your phobia knowledge?",
         font=("Helvetica", 10), fg="white", bg="#5a4e8d", justify="center", wraplength=500).pack(pady=10)

error_label = tk.Label(start_frame, text="", font=("Helvetica", 12), fg="yellow", bg="#5a4e8d")
error_label.pack()

num_questions_entry = tk.Entry(start_frame, font=("Helvetica", 14), justify="center")
num_questions_entry.insert(0, "Choose the number of questions")
num_questions_entry.pack(pady=10)

level_dropdown = ttk.Combobox(start_frame, values=["Easy", "Hard"], font=("Helvetica", 12))
level_dropdown.set("Levels")
level_dropdown.pack(pady=5)

tk.Button(start_frame, text="Start!", font=("Helvetica", 16, "bold"), bg="#b0a4e3", command=start_quiz).pack(pady=10)

# --- Quiz Frame ---
quiz_frame = tk.Frame(root, bg="#5a4e8d")

round_label = tk.Label(quiz_frame, text="Round #", font=("Helvetica", 22, "bold"), fg="white", bg="#5a4e8d")
round_label.pack(pady=10)

question_label = tk.Label(quiz_frame, text="", font=("Helvetica", 18, "bold"), fg="white", bg="#5a4e8d")
question_label.pack(pady=10)

answer_buttons = []
for _ in range(4):
    var = tk.BooleanVar()
    btn = tk.Checkbutton(quiz_frame, text="", variable=var, font=("Helvetica", 14, "bold"),
                         bg="#a89cc8", fg="white", selectcolor="#5a4e8d", width=20, indicatoron=False)
    btn.var = var
    btn.pack(pady=3)
    answer_buttons.append(btn)

tk.Button(quiz_frame, text="Submit Answer", font=("Helvetica", 14, "bold"), bg="green", fg="white",
          command=submit_answer).pack(pady=8)
tk.Button(quiz_frame, text="End Game", font=("Helvetica", 14, "bold"), bg="red", fg="white", command=end_game).pack(
    side="left", padx=20, pady=10)
tk.Button(quiz_frame, text="Next question", font=("Helvetica", 14, "bold"), bg="#5a4e8d", fg="white",
          command=next_question).pack(side="left", padx=20)
tk.Button(quiz_frame, text="Hint", font=("Helvetica", 14, "bold"), bg="orange", fg="white", command=use_hint).pack(
    side="left", padx=20)
tk.Button(quiz_frame, text="Stats", font=("Helvetica", 14, "bold"), bg="#d9c7e6", fg="black", command=show_stats).pack(
    side="left", padx=20)

root.mainloop()
