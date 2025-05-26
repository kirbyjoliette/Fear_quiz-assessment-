import csv
import random
from tkinter import *
from functools import partial

from Fear_quiz_assessment.fear_quiz_B import round_ans


def get_fears():
    """
    Retrieves fears from csv file
    :return: list fears where each list item has the 
    fear name, associated score and description
    """
    file = open("Fear_quiz_assessment/fear_list.csv", "r")
    all_fears = list(csv.reader(file, delimiter=","))
    file.close()

    # remove the first row (headers)
    all_fears.pop(0)

    return all_fears

def get_round_fears():
    """
    Choose four fears from larger list ensuring that the scores are all different.
    :return: list of fears and score to beat (median of scores)
    """
    all_fear_list = get_fears()
    round_fears = []
    fear_scores = []

    # loop until we have four fears with different scores
    while len(round_fears) < 4:
        potential_fear = random.choice(all_fear_list)

        if potential_fear[1] not in fear_scores:
            round_fears.append(potential_fear)
            fear_scores.append(potential_fear[1])

    # change scores to integers
    int_scores = [int(x) for x in fear_scores]

    # Get median score / target score
    int_scores.sort()
    median = (int_scores[1] + int_scores[2]) / 2
    median = round_ans(median)

    return round_fears, median

# ... rest of your code remains the same ...

class StartGame:
    def __init__(self):
        self.start_frame = Frame(padx=10, pady=10)
        self.start_frame.grid()

        # Update the intro string for fear quiz
        intro_string = "In each round you will be presented with different fears. Your goal is " \
                      "to identify the fear that matches the target anxiety level."

        choose_string = "How many rounds do you want to play?"

        start_label_list = [
            ["Fear Quiz", ("Arial", "16", "bold"), None],
            [intro_string, ("Arial", "12"), None],
            [choose_string, ("Arial", "12", "bold"), "#009900"]
        ]

        # ... rest of the StartGame class remains the same ...