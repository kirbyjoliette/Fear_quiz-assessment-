import csv
import random
import time
from datetime import datetime
from tkinter import *
from tkinter import ttk, messagebox
import json


class FearQuiz:
    def __init__(self, root):
        self.root = root
        self.root.title("Fear Quiz")
        self.root.geometry("800x600")

        # Theme settings
        self.theme = "light"
        self.colors = {
            "light": {
                "bg": "#ffffff",
                "fg": "#000000",
                "button": "#0057D8",
                "button_fg": "#ffffff"
            },
            "dark": {
                "bg": "#2d2d2d",
                "fg": "#ffffff",
                "button": "#404040",
                "button_fg": "#ffffff"
            }
        }

        # Quiz settings
        self.difficulty = StringVar(value="medium")
        self.difficulties = {
            "easy": {"time": 30, "hints": 2},
            "medium": {"time": 20, "hints": 1},
            "hard": {"time": 15, "hints": 0}
        }

        # Statistics
        self.stats = {
            "total_questions": 0,
            "correct_answers": 0,
            "incorrect_answers": 0,
            "fastest_time": float('inf'),
            "common_mistakes": {}
        }

        self.create_main_menu()

    def create_main_menu(self):
        self.clear_window()
        self.main_frame = Frame(self.root, bg=self.colors[self.theme]["bg"])
        self.main_frame.pack(expand=True, fill="both")

        # Title
        Label(self.main_frame,
              text="Fear Quiz",
              font=("Arial", 24, "bold"),
              bg=self.colors[self.theme]["bg"],
              fg=self.colors[self.theme]["fg"]).pack(pady=20)

        # Buttons
        buttons = [
            ("Start Quiz", self.show_quiz_settings),
            ("View Statistics", self.show_statistics),
            ("Toggle Theme", self.toggle_theme),
            ("Exit", self.root.quit)
        ]

        for text, command in buttons:
            Button(self.main_frame,
                   text=text,
                   font=("Arial", 12),
                   bg=self.colors[self.theme]["button"],
                   fg=self.colors[self.theme]["button_fg"],
                   width=20,
                   command=command).pack(pady=10)

    def show_quiz_settings(self):
        self.clear_window()
        settings_frame = Frame(self.root, bg=self.colors[self.theme]["bg"])
        settings_frame.pack(expand=True, fill="both")

        Label(settings_frame,
              text="Quiz Settings",
              font=("Arial", 20, "bold"),
              bg=self.colors[self.theme]["bg"],
              fg=self.colors[self.theme]["fg"]).pack(pady=20)

        # Number of questions
        Label(settings_frame,
              text="Number of Questions:",
              bg=self.colors[self.theme]["bg"],
              fg=self.colors[self.theme]["fg"]).pack()

        self.question_count = ttk.Spinbox(settings_frame,
                                          from_=5,
                                          to=20,
                                          width=10)
        self.question_count.set(10)
        self.question_count.pack(pady=10)

        # Difficulty selection
        Label(settings_frame,
              text="Difficulty:",
              bg=self.colors[self.theme]["bg"],
              fg=self.colors[self.theme]["fg"]).pack()

        for diff in ["easy", "medium", "hard"]:
            ttk.Radiobutton(settings_frame,
                            text=diff.capitalize(),
                            variable=self.difficulty,
                            value=diff).pack()

        # Start and Back buttons
        Button(settings_frame,
               text="Start Quiz",
               command=self.start_quiz,
               bg=self.colors[self.theme]["button"],
               fg=self.colors[self.theme]["button_fg"]).pack(pady=20)

        Button(settings_frame,
               text="Back to Menu",
               command=self.create_main_menu,
               bg=self.colors[self.theme]["button"],
               fg=self.colors[self.theme]["button_fg"]).pack()

    def clear_window(self):
        for widget in self.root.winfo_children():
            widget.destroy()

    def toggle_theme(self):
        self.theme = "dark" if self.theme == "light" else "light"
        self.create_main_menu()
