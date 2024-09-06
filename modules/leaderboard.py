# leaderboard.py
from settings import *


def load_high_score(file_path='assets/highscore.txt'):
    try:
        with open(file_path, 'r') as file:
            return int(file.readline().strip())
    except:
        return 0

def save_high_score(score, file_path='assets/highscore.txt'):
    with open(file_path, 'w') as file:
        file.write(str(score))

def update_leaderboard(score):
    high_score = load_high_score()
    if score > high_score:
        save_high_score(score)
        return True  # New high score achieved
    return False
