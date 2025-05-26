import csv
import random
from tkinter import *
from functools import partial  # To prevent unwanted windows


# helper functions go here

def get_round_fears():
    """
    Choose four fears from the CSV, ensuring their anxiety scores are different.
    :return: list of fears, median anxiety score (rounded), highest anxiety score
    """
    all_fear_list = get_fears()

    round_fears = []
    anxiety_levels = []

    # Loop until we have four fears with unique scores
    while len(round_fears) < 4:
        potential_fear = random.choice(all_fear_list)
        if potential_fear[1] not in anxiety_levels:
            round_fears.append(potential_fear)
            anxiety_levels.append(potential_fear[1])

    print("Round fears:", round_fears)
    print("Anxiety levels:", anxiety_levels)

    # Convert scores to integers and sort them
    int_levels = [int(score) for score in anxiety_levels]
    int_levels.sort()

    # Calculate the median
    median = (int_levels[1] + int_levels[2]) / 2
    median = round_ans(median)  # Use your custom round function

    highest = int_levels[-1]

    return round_fears, median, highest

def get_fears():
    """
    Retrieves fears from csv file
    :return: list fears which where each list item has the
    fear name
    """
    file = open("Fear_quiz_assessment/fear_list.csv", "r")
    all_fears = list(csv.reader(file, delimiter=","))
    file.close()
    # Remove the header row
    all_fears.pop(0)
    return all_fears

    # Remove the first row
    all_fears.pop(0)

    return all_fears


def get_round_fears():
    """
   Choose four fear from larger list ensuring that the scores are all different.
   :return: list of fear and score to beat (median of scores)
    """
    all_fear_list = get_fears()

    round_fears = []
    anxiety_levels = []

    # loop until we have four fear with different scores
    while len(round_fears) < 4:
        potential_fear = random.choice(all_fear_list)

        # Fet the score and check it's not a duplicate
        if potential_fear[1] not in anxiety_levels:
            round_fears.append(potential_fear)
            anxiety_levels.append(potential_fear[1])

        print(round_fears)
        print(anxiety_levels)

        # find target score (median)

    # change scores to integers
    int_levels = [int(x) for x in anxiety_levels]
    int_levels.sort()
    # Get median score / target score
    median = (int_levels[1] + int_levels[2]) / 2
    median = round_ans(median)
    highest = int_levels[-1]

    return round_fears, median, highest


def round_ans(val):
    """
    Rounds numbers to nearest integer
    :param val: number to be rounded
    :return:  number (on integer)
    """
    var_rounded = (val * 2 + 1) // 2
    raw_rounded = "{:.0f}".format(var_rounded)
    return int(raw_rounded)


class StartGame:
    def __init__(self):
        self.start_frame = Frame(padx=10, pady=10)
        self.start_frame.grid()

        intro_string = "In each round you will be presented with different fears. " \
                       "Your goal is to match the target anxiety level and learn " \
                       "about various phobias."
        choose_string = "How many questions would you like to attempt?"

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

        self.entry_area_frame = Frame(self.start_frame)
        self.entry_area_frame.grid(row=3)

        self.num_rounds_entry = Entry(self.entry_area_frame,
                                      font=("Arial", "20", "bold"), width=10)
        self.num_rounds_entry.grid(row=0, column=0, padx=10, pady=10)

        self.play_button = Button(self.entry_area_frame,
                                  font=("Arial", "16", "bold"),
                                  fg="#FFFFFF", bg="#9090D6",
                                  text="Start Quiz", width=10,
                                  command=self.check_rounds)
        self.play_button.grid(row=0, column=1)

    def check_rounds(self):
        rounds_wanted = self.num_rounds_entry.get()
        self.choose_label.config(fg="#009900", font=("Arial", "12", "bold"))
        self.num_rounds_entry.config(bg="#FFFFFF")

        error = "Oops - Please choose a whole number more than zero."
        has_errors = "no"

        try:
            rounds_wanted = int(rounds_wanted)
            if rounds_wanted > 0:
                Play(rounds_wanted)
                root.withdraw()
            else:
                has_errors = "yes"
        except ValueError:
            has_errors = "yes"

        if has_errors == "yes":
            self.choose_label.config(text=error, fg="#990000",
                                     font=("Arial", "10", "bold"))
            self.num_rounds_entry.config(bg="#F4CCCC")
            self.num_rounds_entry.delete(0, END)


class Play:
    def __init__(self, how_many):
        # Integers / String Variables
        self.target_score = IntVar()

        # round played - start with zero
        self.rounds_played = IntVar()
        self.rounds_played.set(0)
        self.rounds_wanted = IntVar()
        self.rounds_wanted.set(how_many)
        self.rounds_won = IntVar()
        self.rounds_won.set(0)

        # Fear lists and score list
        self.round_fear_list = []
        self.all_scores_list = []
        self.all_medians_list = []
        self.all_high_score_list = []

        self.play_box = Toplevel()

        self.game_frame = Frame(self.play_box)
        self.game_frame.grid(padx=10, pady=10)

        # If users press the 'x' on the quiz window, end the entire quiz!
        self.play_box.protocol('WM_DELETE_WINDOW', root.destroy)

        # body font for most labels...
        body_font = ("Arial", "12")

        # List for label details (text | font | background | row)
        play_labels_list = [
            ["Round # of #", ("Arial", "12", "bold"), None, 0],
            ["Anxiety Level to Match: #", body_font, "#FFF2CC", 1],
            ["Choose a fear below. Good luck! 🎯", body_font, "#D5E8D4", 2],
            ["You chose, result", body_font, "#D5E8D4", 4]
        ]

        play_labels_ref = []
        for item in play_labels_list:
            self.make_label = Label(self.game_frame, text=item[0], font=item[1],
                                    bg=item[2], wraplength=300, justify="left")
            self.make_label.grid(row=item[3], pady=10, padx=10)
            play_labels_ref.append(self.make_label)

        self.heading_label = play_labels_ref[0]
        self.target_label = play_labels_ref[1]
        self.choose_label = play_labels_ref[2]
        self.results_label = play_labels_ref[3]

        # set up fear buttons...
        self.fear_frame = Frame(self.game_frame)
        self.fear_frame.grid(row=3)

        self.fear_button_ref = []
        self.button_fears_list = []

        # create four buttons in a 2 x 2 grid
        for item in range(0, 4):
            self.fear_button = Button(self.fear_frame, font=("Arial", "12"),
                                      text="Fear Name", width=20,
                                      command=partial(self.round_results, item))
            self.fear_button.grid(row=item // 2, column=item % 2,
                                  padx=5, pady=5)
            self.fear_button_ref.append(self.fear_button)

        self.hints_stats_frame = Frame(self.game_frame)
        self.hints_stats_frame.grid(row=6)

        control_buttons_list = [
            [self.game_frame, "Next Question", "#3E3A5C", self.new_round, 21, 5, None],
            [self.hints_stats_frame, "Hints", "#F4A261", self.to_hints, 10, 0, 0],
            [self.hints_stats_frame, "Stats", "#E1D5E7", self.to_stats, 10, 0, 1],
            [self.game_frame, "End Quiz", "#990000", self.close_play, 21, 7, None]
        ]

        control_ref_list = []
        for item in control_buttons_list:
            make_control_button = Button(item[0], text=item[1], bg=item[2],
                                         command=item[3], font=("Arial", "16", "bold"),
                                         fg="#FFFFFF", width=item[4])
            make_control_button.grid(row=item[5], column=item[6], padx=5, pady=5)
            control_ref_list.append(make_control_button)

        # Retrieve Labels so they can be configured later
        self.next_button = control_ref_list[0]
        self.hints_button = control_ref_list[1]
        self.stats_button = control_ref_list[2]
        self.end_game_button = control_ref_list[3]

        # Disable stats button at start!
        self.stats_button.config(state=DISABLED)

        # images for use on 'end game' / 'play again' button
        self.nervous_image = PhotoImage(file="Fear_quiz_assessment/nervous_30.png")
        self.brave_image = PhotoImage(file="Fear_quiz_assessment/brave_30.png")

        self.end_game_button.config(text="End Quiz", image=self.nervous_image,
                                    compound="right", width=280)

        # Once interface has been created, invoke newA
        # round function for first round.
        self.new_round()

    def new_round(self):
        """
        Choose four fears, works out median for score to beat. Configures
        buttons with chosen fear
        """

        # retrieve number of rounds played, add one to it and configure heading
        rounds_played = self.rounds_played.get()
        self.rounds_played.set(rounds_played)

        rounds_wanted = self.rounds_wanted.get()

        # get round fears and median score.
        self.round_fear_list, median, highest = get_round_fears()

        # Set target score as median (for later comparison)
        self.target_score.set(median)

        # add median and high score to lists for stats...
        self.all_high_score_list.append(highest)

        # Update heading, and score to beat labels, "Hide" results label
        self.heading_label.config(text=f"Question {rounds_played + 1} of {rounds_wanted}")
        self.target_label.config(text=f"Target Anxiety Level: {median}",
                                 font=("Arial", "14", "bold"))
        self.results_label.config(text="Choose a fear", bg="#F0F0F0")

        # configure buttons using foreground and background colours from list
        # enable fear buttons (disabled at the end of the last round)
        for count, item in enumerate(self.fear_button_ref):
            fear_name = self.round_fear_list[count][0]
            fear_description = self.round_fear_list[count][2]
            item.config(text=f"{fear_name}\n{fear_description}",
                        state=NORMAL, wraplength=150)

        self.next_button.config(state=DISABLED)

    def close_play(self):
        self.play_box.destroy()
        root.deiconify()

    def to_hints(self):
        DisplayHints(self, self.rounds_played.get())

    def to_stats(self):
        pass  # placeholder for stats display


    def round_results(self, user_choice):
        """
        Retrieves which button was pushed (index 0 - 3), retrieves
        score and then compares its median, updates results
        and adds results to stats list.
        """
        # enable stats button set after at least one round has been played.
        self.stats_button.config(state=NORMAL)

        # Get user score and fear based on button press 
        score = int(self.round_fear_list[user_choice][1])

        # Add one to the number of rounds played and retrieve
        # the number of rounds won
        rounds_played = self.rounds_played.get()
        rounds_played += 1
        self.rounds_played.set(rounds_played)
        

        rounds_won = self.rounds_won.get()

        # alternate way to get button name. Good for if buttons have been scrambled!
        fear_name = self.fear_button_ref[user_choice].cget('text')

        # retrieve target score and compare with user score to find round result
        target = self.target_score.get()
        self.all_medians_list.append(target)

        if score >= target:
            result_text = f"Success! {fear_name} earned you {score} points"
            result_bg = "#82B366"
            self.all_scores_list.append(score)

            rounds_won += 1
            self.rounds_won.set(rounds_won)

        else:
            result_text = f"Oops {fear_name} ({score}) is less than the target."
            result_bg = "#F8CECC"
            self.all_scores_list.append(0)

        self.results_label.config(text=result_text, bg=result_bg)

        # printing area to generate test data for stats (delete when done)
        print("all scores", self.all_scores_list)
        print("all medians:", self.all_medians_list)
        print("highest scores:", self.all_high_score_list)

        # enable stats & next button, disable fear buttons
        self.next_button.config(state=NORMAL)
        self.stats_button.config(state=NORMAL)

        # check to see if game is over
        rounds_wanted = self.rounds_wanted.get()

        # Code for when the game ends!
        if rounds_played == rounds_wanted:

            # work out success rate
            success_rate = rounds_won / rounds_played * 100
            success_string = (f"Success Rate: "
                              f"{rounds_won} / {rounds_played}"
                              f"({success_rate:.0f}%)")

            # Configure 'end game' labels / buttons
            self.heading_label.config(text="Game Over")
            self.target_label.config(text=success_string)
            self.choose_label.config(text="Please click the stats "
                                          "button for more info.")
            self.next_button.config(state=DISABLED, text="Game Over")
            self.stats_button.config(bg="#990000")
            self.end_game_button.config(text="Play Again", bg="#006600", image=self.thumb_up,
                                        compound="right", width=280)

            for item in self.fear_button_ref:
                item.config(state=DISABLED)

class DisplayHints:
    def __init__(self, partner, rounds_played):
        self.rounds_played = rounds_played
        background = "#ffe6cc"
        self.help_box = Toplevel()

        partner.hints_button.config(state=DISABLED)
        partner.end_game_button.config(state=DISABLED)
        partner.stats_button.config(state=DISABLED)

        self.help_box.protocol('WM_DELETE_WINDOW',
                               partial(self.close_hints, partner))

        self.help_frame = Frame(self.help_box, bg=background)
        self.help_frame.grid()

        self.help_heading_label = Label(self.help_frame,
                                        bg=background,
                                        text="How to Play",
                                        font=("Arial", "14", "bold"))
        self.help_heading_label.grid(row=0)

        help_text = ("Each fear has an anxiety level from 1-10.\n\n"
                     "Your goal is to match the target anxiety level.\n\n"
                     "Read the fear description carefully - more severe "
                     "fears typically have higher anxiety levels.\n\n"
                     "Common fears like spiders or heights often have "
                     "moderate anxiety levels (5-7).\n\n"
                     "Rare or extreme fears usually have higher "
                     "anxiety levels (8-10).")

        self.help_text_label = Label(self.help_frame, bg=background,
                                     text=help_text, wraplength=350,
                                     justify="left")
        self.help_text_label.grid(row=1, padx=10)

        self.dismiss_button = Button(self.help_frame,
                                     font=("Arial", "12", "bold"),
                                     text="Dismiss", bg="#CC6600",
                                     fg="#FFFFFF",
                                     command=partial(self.close_hints, partner))
        self.dismiss_button.grid(row=2, padx=10, pady=10)

        # closes help dialogue (used by button and x at top of dialogue)

    def close_hints(self, partner):
        # put help button back to normal...
        partner.hints_button.config(state=NORMAL)
        partner.end_game_button.config(state=NORMAL)
        if self.rounds_played >= 1:
            partner.stats_button.config(state=NORMAL)
        self.help_box.destroy()


# -------------------------
# Start the program
# -------------------------
root = Tk()
root.title("Fear Quiz")
start_game = StartGame()
root.mainloop()
