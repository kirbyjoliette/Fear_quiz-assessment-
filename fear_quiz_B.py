import csv
import random
from tkinter import *
from functools import partial  # To prevent unwanted windows
from tkinter import messagebox


class StartGame:
    def __init__(self):
        self.start_frame = Frame(padx=10, pady=10)
        self.start_frame.grid()

        # Strings for labels
        intro_string = "In each round you will be presented with different fears. " \
                       "Your goal is to identify the fear that matches the given description " \
                       "and anxiety level."

        choose_string = "How many questions would you like to answer?"

        # Labels
        start_label_list = [
            ["Fear Quiz", ("Arial", "16", "bold"), None],
            [intro_string, ("Arial", "12"), None],
            [choose_string, ("Arial", "12", "bold"), "#009900"]
        ]

        start_label_ref = []
        for count, item in enumerate(start_label_list):
            make_label = Label(self.start_frame, text=item[0], font=item[1],
                               fg=item[2], wraplength=350, justify="left", pady=10, padx=20)
            make_label.grid(row=count)
            start_label_ref.append(make_label)

        self.choose_label = start_label_ref[2]

        # Entry area and start button
        self.entry_area_frame = Frame(self.start_frame)
        self.entry_area_frame.grid(row=3)

        self.num_rounds_entry = Entry(self.entry_area_frame, font=("Arial", "20", "bold"),
                                      width=10)
        self.num_rounds_entry.grid(row=0, column=0, padx=10, pady=10)

        self.play_button = Button(self.entry_area_frame, font=("Arial", "16", "bold"),
                                  fg="#FFFFFF", bg="#0057D8", text="Start Quiz", width=10,
                                  command=self.check_rounds)
        self.play_button.grid(row=0, column=1)

    def check_rounds(self):
        try:
            to_play = int(self.num_rounds_entry.get())
            if to_play < 1:
                raise ValueError
            print(f"You chose to play {to_play} questions.")
            # In the future, this is where you'd move to the quiz screen
            fears, median, highest = get_round_fears()
            print("Selected fears:", fears)
            print("Median anxiety:", median)
            print("Highest anxiety:", highest)
        except ValueError:
            messagebox.showerror("Invalid Input", "Please enter a whole number greater than 0")


def get_fears():
    """
    Retrieves fears from CSV file.
    Returns: list of fears [Name, Description, AnxietyLevel]
    """
    try:
        with open("Fear_quiz_assessment/fear_list.csv", "r") as file:
            all_fears = list(csv.reader(file))
        all_fears.pop(0)  # remove headers
        return all_fears
    except FileNotFoundError:
        messagebox.showerror("File Error", "fear_list.csv not found.")
        return []


def get_round_fears():
    """
    Selects 4 fears with unique anxiety levels.
    Returns: round_fears list, median anxiety, highest anxiety
    """
    all_fear_list = get_fears()
    round_fears = []
    fear_levels = []

    while len(round_fears) < 4 and all_fear_list:
        potential_fear = random.choice(all_fear_list)
        if potential_fear[2] not in fear_levels:
            round_fears.append(potential_fear)
            fear_levels.append(potential_fear[2])

    int_levels = [int(x) for x in fear_levels]
    int_levels.sort()

    if len(int_levels) >= 3:
        median = round_ans((int_levels[1] + int_levels[2]) / 2)
    else:
        median = round_ans(sum(int_levels) / len(int_levels))

    highest = max(int_levels) if int_levels else 0
    return round_fears, median, highest


def round_ans(val):
    return round(val)


# Run the GUI
if __name__ == "__main__":
    root = Tk()
    root.title("Fear Quiz")
    StartGame()
    root.mainloop()
