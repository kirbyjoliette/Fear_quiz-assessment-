import tkinter as tk
from tkinter import ttk, messagebox
import csv
import random
import datetime
from functools import partial

# --- Data ---
questions_easy = {
    "Arachnophobia": "🕷️ Spider",
    "Acrophobia": "🏔️ Heights", 
    "Cynophobia": "🐶 Dogs",
    "Ophidiophobia": "🐍 Snakes",
    "Trypanophobia": "💉 Needles",
    "Agoraphobia": "🚪 Open spaces",
    "Claustrophobia": "📦 Enclosed spaces",
    "Aviophobia": "✈️ Flying"
}

questions_hard = {
    "Nomophobia": "📱 Being without a phone",
    "Atychiphobia": "❌ Failure", 
    "Taphophobia": "⚰️ Being buried alive",
    "Chronophobia": "⏰ Time",
    "Philophobia": "❤️ Love",
    "Thanatophobia": "💀 Death",
    "Ergophobia": "💼 Work",
    "Hippopotomonstrosesquippedaliophobia": "📚 Long words"
}

# Generate options for each phobia
def generate_options(correct_answer, all_questions):
    options = [correct_answer]
    other_answers = [ans for ans in all_questions.values() if ans != correct_answer]
    options.extend(random.sample(other_answers, min(3, len(other_answers))))
    
    # Pad with generic options if needed
    generic_options = ["🌊 Water", "🔥 Fire", "⚡ Thunder", "🦇 Bats", "🐱 Cats", "🧼 Soap"]
    while len(options) < 4:
        generic = random.choice(generic_options)
        if generic not in options:
            options.append(generic)
    
    return options[:4]

# --- Global Variables ---
score = 0
hints_used = 0
current_question = ""
total_questions = 0
asked_questions = []
level = "Easy"
stats_list = []
current_correct_answer = ""
round_number = 0

# --- Functions ---
def start_quiz():
    global total_questions, level, score, asked_questions, hints_used, stats_list, round_number
    try:
        num_input = num_questions_entry.get().strip()
        if not num_input:
            raise ValueError("Please enter a number")
        total_questions = int(num_input)
        if total_questions <= 0:
            raise ValueError("Number must be greater than zero")
    except ValueError:
        error_label.config(text="⚠️ Oops - Please choose a whole number more than zero", fg="#FF6B6B")
        return

    level = level_dropdown.get()
    if level not in ["Easy", "Hard"]:
        error_label.config(text="⚠️ Please choose a level", fg="#FF6B6B")
        return

    score = 0
    hints_used = 0
    asked_questions = []
    stats_list = []
    round_number = 0

    start_frame.pack_forget()
    quiz_frame.pack(fill="both", expand=True)
    next_question()

def next_question():
    global current_question, current_correct_answer, round_number
    
    question_pool = questions_easy if level == "Easy" else questions_hard
    remaining_questions = list(set(question_pool.keys()) - set(asked_questions))

    if not remaining_questions or len(asked_questions) >= total_questions:
        end_game()
        return

    round_number += 1
    current_question = random.choice(remaining_questions)
    asked_questions.append(current_question)
    current_correct_answer = question_pool[current_question]

    question_label.config(text=f"What is {current_question}?")
    round_label.config(text=f"Round {round_number} of {total_questions}")
    feedback_label.config(text="Choose your answer below! 🎯", fg="white")

    # Reset buttons
    for btn in answer_buttons:
        btn.config(state="normal", bg="#a89cc8", fg="white")

    # Generate and shuffle options
    options = generate_options(current_correct_answer, question_pool)
    random.shuffle(options)
    
    for i in range(4):
        answer_buttons[i].config(text=options[i])
    
    # Reset hint button
    hint_button.config(state="normal", text="💡 Hint")
    submit_button.config(state="normal")
    next_button.config(state="disabled")

def check_answer(selected_index):
    global score
    selected_answer = answer_buttons[selected_index].cget("text")
    
    # Disable all buttons
    for btn in answer_buttons:
        btn.config(state="disabled")
    
    # Check if correct
    is_correct = selected_answer == current_correct_answer
    
    if is_correct:
        score += 10
        feedback_label.config(text="✅ Correct! Well done! 🎉", fg="#4ECDC4", bg="#2ECC71")
        answer_buttons[selected_index].config(bg="#2ECC71")
        result = "Correct"
    else:
        score -= 5
        feedback_label.config(text=f"❌ Incorrect! The answer was: {current_correct_answer}", 
                            fg="#FF6B6B", bg="#E74C3C")
        answer_buttons[selected_index].config(bg="#E74C3C")
        # Highlight correct answer
        for btn in answer_buttons:
            if btn.cget("text") == current_correct_answer:
                btn.config(bg="#2ECC71")
        result = "Incorrect"
    
    # Add to stats
    stats_list.append({
        "Round": round_number,
        "Phobia": current_question,
        "Your Answer": selected_answer,
        "Correct Answer": current_correct_answer,
        "Result": result,
        "Score": score,
        "Hints Used": hints_used
    })
    
    # Enable next button
    next_button.config(state="normal")
    submit_button.config(state="disabled")
    hint_button.config(state="disabled")
    stats_button.config(state="normal")

def use_hint():
    global hints_used, score
    
    # Remove one wrong answer
    wrong_options = []
    for i, btn in enumerate(answer_buttons):
        if btn.cget("text") != current_correct_answer:
            wrong_options.append(i)
    
    if wrong_options:
        remove_index = random.choice(wrong_options)
        answer_buttons[remove_index].config(state="disabled", bg="#666666", text="❌ Eliminated")
        
    hints_used += 1
    score = max(0, score - 2)  # Don't let score go negative
    
    hint_button.config(text=f"💡 Hint ({hints_used})", state="disabled")
    feedback_label.config(text="💡 Hint used! One wrong answer eliminated.", fg="#FFA07A")

def end_game():
    global score
    quiz_frame.pack_forget()
    
    success_rate = (sum(1 for stat in stats_list if stat["Result"] == "Correct") / len(stats_list) * 100) if stats_list else 0
    
    # Determine performance message
    if success_rate >= 80:
        performance_msg = "🏆 Excellent! You're a phobia expert!"
        performance_color = "#FFD700"
    elif success_rate >= 60:
        performance_msg = "🎉 Good job! You know your fears well!"
        performance_color = "#4ECDC4"
    elif success_rate >= 40:
        performance_msg = "👍 Not bad! Keep learning about phobias!"
        performance_color = "#FFA07A"
    else:
        performance_msg = "📚 Keep studying! There's room for improvement!"
        performance_color = "#FF6B6B"
    
    result_text = (f"Quiz Complete! 🎊\n\n"
                  f"Final Score: {score} points\n"
                  f"Correct Answers: {sum(1 for stat in stats_list if stat['Result'] == 'Correct')}/{len(stats_list)}\n"
                  f"Success Rate: {success_rate:.1f}%\n"
                  f"Hints Used: {hints_used}\n\n"
                  f"{performance_msg}")
    
    messagebox.showinfo("Game Over", result_text)
    
    # Show end game frame
    end_frame.pack(fill="both", expand=True)
    end_score_label.config(text=f"Final Score: {score} points", fg=performance_color)
    end_performance_label.config(text=performance_msg, fg=performance_color)

def show_detailed_stats():
    if not stats_list:
        messagebox.showinfo("Stats", "No game data available yet!")
        return
    
    stats_window = tk.Toplevel(root)
    stats_window.title("Detailed Statistics")
    stats_window.config(bg="#5a4e8d")
    stats_window.geometry("800x600")
    
    # Create scrollable frame
    canvas = tk.Canvas(stats_window, bg="#5a4e8d")
    scrollbar = ttk.Scrollbar(stats_window, orient="vertical", command=canvas.yview)
    scrollable_frame = tk.Frame(canvas, bg="#5a4e8d")
    
    scrollable_frame.bind(
        "<Configure>",
        lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
    )
    
    canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
    canvas.configure(yscrollcommand=scrollbar.set)
    
    # Title
    tk.Label(scrollable_frame, text="📊 Detailed Quiz Statistics", 
             font=("Helvetica", 18, "bold"), fg="lavender", bg="#5a4e8d").pack(pady=10)
    
    # Summary stats
    correct_count = sum(1 for stat in stats_list if stat["Result"] == "Correct")
    total_count = len(stats_list)
    success_rate = (correct_count / total_count * 100) if total_count > 0 else 0
    
    summary_text = (f"Level: {level} | Total Questions: {total_count} | "
                   f"Correct: {correct_count} | Success Rate: {success_rate:.1f}%\n"
                   f"Final Score: {score} | Hints Used: {hints_used}")
    
    tk.Label(scrollable_frame, text=summary_text, font=("Helvetica", 12), 
             fg="white", bg="#5a4e8d", justify="center").pack(pady=10)
    
    # Individual question results
    for i, stat in enumerate(stats_list, 1):
        color = "#4ECDC4" if stat["Result"] == "Correct" else "#FF6B6B"
        result_emoji = "✅" if stat["Result"] == "Correct" else "❌"
        
        question_frame = tk.Frame(scrollable_frame, bg=color, relief="raised", bd=2)
        question_frame.pack(fill="x", padx=20, pady=5)
        
        question_text = (f"{result_emoji} Round {stat['Round']}: {stat['Phobia']}\n"
                        f"Your Answer: {stat['Your Answer']}\n"
                        f"Correct Answer: {stat['Correct Answer']}")
        
        tk.Label(question_frame, text=question_text, font=("Helvetica", 10), 
                bg=color, fg="white", justify="left", wraplength=700).pack(pady=10, padx=10)
    
    canvas.pack(side="left", fill="both", expand=True)
    scrollbar.pack(side="right", fill="y")

def export_stats():
    if not stats_list:
        messagebox.showinfo("Export", "No game data to export yet!")
        return
        
    filename = f"fear_quiz_stats_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
    try:
        with open(filename, "w", newline='') as f:
            fieldnames = ["Round", "Phobia", "Your Answer", "Correct Answer", "Result", "Score", "Hints Used"]
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(stats_list)
        messagebox.showinfo("Export Successful", f"📊 Stats exported to {filename}")
    except Exception as e:
        messagebox.showerror("Export Error", f"Failed to export stats: {str(e)}")

def restart_quiz():
    end_frame.pack_forget()
    start_frame.pack(fill="both", expand=True)
    
    # Reset entry field
    num_questions_entry.delete(0, tk.END)
    level_dropdown.set("Easy")
    error_label.config(text="")

# --- GUI Setup ---
root = tk.Tk()
root.title("Fear Quiz 👻")
root.config(bg="#5a4e8d")
root.geometry("700x500")
root.resizable(True, True)

# --- Start Frame ---
start_frame = tk.Frame(root, bg="#5a4e8d")
start_frame.pack(fill="both", expand=True)

tk.Label(start_frame, text="Fear Quiz 👾", font=("Helvetica", 28, "bold"), 
         fg="lavender", bg="#5a4e8d").pack(pady=20)

intro_text = ("In this quiz, you'll be shown the name of a phobia and must choose the correct answer from the given options.\n"
             "Each correct answer earns 10 points, but wrong answers cost 5 points.\n"
             "Using hints will reduce your score by 2 points but eliminate one wrong answer.\n"
             "Your goal is to get the highest score possible. Ready to test your phobia knowledge? 🧠")

tk.Label(start_frame, text=intro_text, font=("Helvetica", 14), fg="white", bg="#5a4e8d", 
         justify="center", wraplength=600).pack(pady=20)

error_label = tk.Label(start_frame, text="", font=("Helvetica", 12), fg="#FF6B6B", bg="#5a4e8d")
error_label.pack(pady=5)

# Input frame
input_frame = tk.Frame(start_frame, bg="#5a4e8d")
input_frame.pack(pady=20)

tk.Label(input_frame, text="Number of Questions:", font=("Helvetica", 12), 
         fg="white", bg="#5a4e8d").pack()
num_questions_entry = tk.Entry(input_frame, font=("Helvetica", 14), justify="center", width=10)
num_questions_entry.pack(pady=5)

tk.Label(input_frame, text="Difficulty Level:", font=("Helvetica", 12), 
         fg="white", bg="#5a4e8d").pack(pady=(10,0))
level_dropdown = ttk.Combobox(input_frame, values=["Easy", "Hard"], font=("Helvetica", 12), 
                             state="readonly", width=10)
level_dropdown.set("Easy")
level_dropdown.pack(pady=5)

start_button = tk.Button(start_frame, text="🚀 Start Quiz!", font=("Helvetica", 16, "bold"), 
                        bg="#4ECDC4", fg="white", command=start_quiz, padx=30, pady=10)
start_button.pack(pady=20)

# --- Quiz Frame ---
quiz_frame = tk.Frame(root, bg="#5a4e8d")

round_label = tk.Label(quiz_frame, text="Round #", font=("Helvetica", 20, "bold"), 
                      fg="lavender", bg="#5a4e8d")
round_label.pack(pady=10)

question_label = tk.Label(quiz_frame, text="", font=("Helvetica", 16, "bold"), 
                         fg="white", bg="#5a4e8d", wraplength=600)
question_label.pack(pady=10)

feedback_label = tk.Label(quiz_frame, text="", font=("Helvetica", 12), 
                         fg="white", bg="#5a4e8d", wraplength=600)
feedback_label.pack(pady=5)

# Answer buttons frame
answer_frame = tk.Frame(quiz_frame, bg="#5a4e8d")
answer_frame.pack(pady=20)

answer_buttons = []
for i in range(4):
    btn = tk.Button(answer_frame, text="", font=("Helvetica", 12, "bold"),
                   bg="#a89cc8", fg="white", width=25, height=2,
                   command=lambda i=i: check_answer(i), wraplength=200)
    btn.grid(row=i//2, column=i%2, padx=10, pady=5)
    answer_buttons.append(btn)

# Control buttons frame
control_frame = tk.Frame(quiz_frame, bg="#5a4e8d")
control_frame.pack(pady=20)

submit_button = tk.Button(control_frame, text="✅ Submit", font=("Helvetica", 12, "bold"),
                         bg="#4ECDC4", fg="white", state="disabled")
submit_button.pack(side="left", padx=5)

hint_button = tk.Button(control_frame, text="💡 Hint", font=("Helvetica", 12, "bold"),
                       bg="#FFA07A", fg="white", command=use_hint)
hint_button.pack(side="left", padx=5)

next_button = tk.Button(control_frame, text="➡️ Next", font=("Helvetica", 12, "bold"),
                       bg="#9B59B6", fg="white", command=next_question, state="disabled")
next_button.pack(side="left", padx=5)

stats_button = tk.Button(control_frame, text="📊 Stats", font=("Helvetica", 12, "bold"),
                        bg="#E67E22", fg="white", command=show_detailed_stats, state="disabled")
stats_button.pack(side="left", padx=5)

end_quiz_button = tk.Button(control_frame, text="🛑 End Quiz", font=("Helvetica", 12, "bold"),
                           bg="#E74C3C", fg="white", command=end_game)
end_quiz_button.pack(side="left", padx=5)

# --- End Frame ---
end_frame = tk.Frame(root, bg="#5a4e8d")

tk.Label(end_frame, text="🎊 Quiz Complete! 🎊", font=("Helvetica", 24, "bold"), 
         fg="lavender", bg="#5a4e8d").pack(pady=30)

end_score_label = tk.Label(end_frame, text="", font=("Helvetica", 18, "bold"), 
                          fg="white", bg="#5a4e8d")
end_score_label.pack(pady=10)

end_performance_label = tk.Label(end_frame, text="", font=("Helvetica", 14), 
                                fg="white", bg="#5a4e8d", wraplength=500)
end_performance_label.pack(pady=10)

# End game buttons
end_button_frame = tk.Frame(end_frame, bg="#5a4e8d")
end_button_frame.pack(pady=30)

tk.Button(end_button_frame, text="🔄 Play Again", font=("Helvetica", 14, "bold"),
         bg="#4ECDC4", fg="white", command=restart_quiz, padx=20, pady=10).pack(side="left", padx=10)

tk.Button(end_button_frame, text="📊 View Stats", font=("Helvetica", 14, "bold"),
         bg="#E67E22", fg="white", command=show_detailed_stats, padx=20, pady=10).pack(side="left", padx=10)

tk.Button(end_button_frame, text="💾 Export Stats", font=("Helvetica", 14, "bold"),
         bg="#9B59B6", fg="white", command=export_stats, padx=20, pady=10).pack(side="left", padx=10)

tk.Button(end_button_frame, text="🚪 Quit", font=("Helvetica", 14, "bold"),
         bg="#E74C3C", fg="white", command=root.quit, padx=20, pady=10).pack(side="left", padx=10)

# Start the application
root.mainloop()