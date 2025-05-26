import csv
import random
from datetime import datetime
from typing import List, Tuple, Dict


class QuizManager:
    def __init__(self):
        self.difficulty_levels = {
            'easy': {'time_limit': 30, 'hints': 2},
            'medium': {'time_limit': 20, 'hints': 1},
            'hard': {'time_limit': 15, 'hints': 0}
        }
        self.current_difficulty = 'medium'
        self.fears_database = self.load_fears()
        self.current_question = None
        self.score = 0
        self.stats = {
            'correct_answers': 0,
            'incorrect_answers': 0,
            'fastest_time': float('inf'),
            'mistakes': {}
        }

    def load_fears(self) -> List[Dict]:
        fears = []
        with open('data/fear_database.csv', 'r') as file:
            reader = csv.DictReader(file)
            for row in reader:
                fears.append({
                    'name': row['name'],
                    'description': row['description'],
                    'difficulty': row['difficulty'],
                    'hints': row['hints']
                })
        return fears

    def get_question(self) -> Dict:
        available_fears = [f for f in self.fears_database
                           if f['difficulty'] == self.current_difficulty]
        question_fear = random.choice(available_fears)
        wrong_answers = random.sample([f for f in available_fears
                                       if f != question_fear], 3)

        options = [question_fear['name']] + [f['name'] for f in wrong_answers]
        random.shuffle(options)

        self.current_question = {
            'fear': question_fear,
            'options': options,
            'correct_answer': question_fear['name'],
            'hint': question_fear['hints']
        }
        return self.current_question

    def check_answer(self, answer: str, time_taken: float) -> Tuple[bool, int]:
        is_correct = answer == self.current_question['correct_answer']
        if is_correct:
            self.stats['correct_answers'] += 1
            self.stats['fastest_time'] = min(self.stats['fastest_time'], time_taken)
            points = self.calculate_points(time_taken)
            self.score += points
        else:
            self.stats['incorrect_answers'] += 1
            self.stats['mistakes'][self.current_question['fear']['name']] = \
                self.stats['mistakes'].get(self.current_question['fear']['name'], 0) + 1
            points = 0

        return is_correct, points

    def calculate_points(self, time_taken: float) -> int:
        base_points = {
            'easy': 100,
            'medium': 150,
            'hard': 200
        }
        time_bonus = max(0, (self.difficulty_levels[self.current_difficulty]['time_limit'] - time_taken) * 2)
        return int(base_points[self.current_difficulty] + time_bonus)

    def export_results(self) -> str:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"exports/quiz_results/quiz_{timestamp}.csv"

        with open(filename, 'w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(['Quiz Results', datetime.now().strftime("%Y-%m-%d %H:%M:%S")])
            writer.writerow(['Score', self.score])
            writer.writerow(['Accuracy',
                             f"{(self.stats['correct_answers'] / (self.stats['correct_answers'] + self.stats['incorrect_answers'])) * 100:.2f}%"])
            writer.writerow(['Fastest Answer', f"{self.stats['fastest_time']:.2f}s"])
            writer.writerow(['Mistakes'])
            for fear, count in self.stats['mistakes'].items():
                writer.writerow([fear, count])

        return filename
