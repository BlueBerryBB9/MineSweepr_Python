class Cell:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.is_mine = False
        self.is_revealed = False
        self.is_flagged = False
        self.adjacent_mines = 0

class Difficulty:
    EASY = {"size": (9, 9), "mines": 10, "name": "Easy"}
    MEDIUM = {"size": (16, 16), "mines": 40, "name": "Medium"}
    HARD = {"size": (30, 16), "mines": 99, "name": "Hard"}