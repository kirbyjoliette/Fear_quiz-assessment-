from tkinter import *
from functools import partial
import random
import csv

# Global variables
fear_list = []
rounds_played = 0
rounds_won = 0

# ------------------ Functions ------------------ #

def get_fears():
    """Reads fear data from CSV file and returns a list."""
    try:
        with open("fear_list.csv", "r") as file:
            all_fears = list(csv.reader(file))
        all_fears.pop(0)  # remove header
        return all_fears
    except FileNotFoundError:
        print("Error: 'fear_list.csv' not found.")
        return []

def get_round_fears():
    """Chooses 4 random fears and returns them with the median and highest anxiety levels."""
    round_fears = random.sample(fear_list, 4)
    anxiety_levels = [int(fear[1]) for fear in round_fears]
    anxiety_levels.sort()
    median = anxiety_levels[1]  # second lowest out of four
    highest = anxiety_levels[-1]
    return round_fears, median, highest

# ------------------ Classes ------------------ #

class StartGame:
    def __init__(self):
        self.start_frame = Frame()
        self.start_frame.grid()

        self.intro_label = Label(self.start_frame, text="Welcome to the Fear Quiz!",
                                 font="Arial 16 bold", pady=10)
        self.intro_label.grid(row=0)

        self.instructions = Label(self.start_frame,
                                  text="Try to match the correct fear to the anxiety level shown.",
                                  wraplength=300, justify="left")
        self.instructions.grid(row=1)

        self.start_button = Button(self.start_frame, text="Start",
                                   command=self.to_play, width=10, bg="light green")
        self.start_button.grid(row=2, pady=10)

    def to_play(self):
        self.start_frame.destroy()
        Play()

class Play:
    def __init__(self):
        global fear_list, rounds_played, rounds_won
        fear_list = get_fears()

        self.play_frame = Frame()
        self.play_frame.grid()

        self.title_label = Label(self.play_frame, text="Fear Quiz Round",
                                 font="Arial 16 bold")
        self.title_label.grid(row=0, column=0, columnspan=4, pady=10)

        self.target_score = IntVar()
        self.target_label = Label(self.play_frame, text="Target Anxiety Level: ?",
                                  font="Arial 14", fg="dark red")
        self.target_label.grid(row=1, column=0, columnspan=4)

        self.fear_button_ref = []
        for i in range(4):
            btn = Button(self.play_frame, text="Fear", width=20, height=2,
                         command=partial(self.round_results, i), wraplength=150)
            btn.grid(row=2 + (i // 2), column=i % 2, padx=5, pady=5)
            self.fear_button_ref.append(btn)

        self.results_label = Label(self.play_frame, text="", fg="blue")
        self.results_label.grid(row=4, column=0, columnspan=4)

        self.next_button = Button(self.play_frame, text="Next", state=DISABLED,
                                  command=self.new_round, width=10, bg="light blue")
        self.next_button.grid(row=5, column=0, pady=10)

        self.stats_button = Button(self.play_frame, text="Stats", state=DISABLED,
                                   command=self.to_stats, width=10)
        self.stats_button.grid(row=5, column=1)

        self.rounds_played = IntVar(value=rounds_played)
        self.rounds_won = IntVar(value=rounds_won)

        self.stats_label = Label(self.play_frame, text="Rounds Played: 0 | Correct: 0")
        self.stats_label.grid(row=6, column=0, columnspan=4)

        self.new_round()

    def new_round(self):
        global rounds_played
        self.round_fear_list, median, highest = get_round_fears()
        self.target_score.set(median)
        self.target_label.config(text=f"Target Anxiety Level: {median}")
        self.results_label.config(text="")

        for i in range(4):
            fear = self.round_fear_list[i][0]
            self.fear_button_ref[i].config(text=fear, state=NORMAL)

        self.next_button.config(state=DISABLED)
        self.stats_button.config(state=DISABLED)

        rounds_played += 1
        self.rounds_played.set(rounds_played)
        self.stats_label.config(text=f"Rounds Played: {rounds_played} | Correct: {self.rounds_won.get()}")

    def round_results(self, index):
        global rounds_won
        chosen_score = int(self.round_fear_list[index][1])
        target = self.target_score.get()

        if chosen_score == target:
            result = "🎯 You matched the anxiety level! Great job."
            rounds_won += 1
            self.rounds_won.set(rounds_won)
        else:
            result = f"❌ You chose {chosen_score}. Correct was {target}."

        self.results_label.config(text=result)

        for btn in self.fear_button_ref:
            btn.config(state=DISABLED)

        self.next_button.config(state=NORMAL)
        self.stats_button.config(state=NORMAL)

        self.stats_label.config(text=f"Rounds Played: {self.rounds_played.get()} | Correct: {self.rounds_won.get()}")

    def to_stats(self):
        self.play_frame.destroy()
        Stats(self)

class Stats:
    def __init__(self, parent):
        self.stats_frame = Frame()
        self.stats_frame.grid()

        self.title = Label(self.stats_frame, text="Game Stats", font="Arial 16 bold")
        self.title.grid(row=0, pady=10)

        total = parent.rounds_played.get()
        correct = parent.rounds_won.get()

        if total > 0:
            percent = (correct / total) * 100
            summary = f"You got {correct} out of {total} correct. ({percent:.1f}%)"
        else:
            summary = "No rounds played yet."

        self.stats_summary = Label(self.stats_frame, text=summary, wraplength=300)
        self.stats_summary.grid(row=1, padx=10)

        self.dismiss_button = Button(self.stats_frame, text="Dismiss", command=self.to_play)
        self.dismiss_button.grid(row=2, pady=10)

    def to_play(self):
        self.stats_frame.destroy()
        Play()

# ------------------ Main Routine ------------------ #

if __name__ == "__main__":
    root = Tk()
    root.title("Fear Quiz")
    StartGame()
    root.mainloop()
