import tkinter as tk

class Cell:
    def __init__(self, button, row, col):
        self.button = button
        self.row = row
        self.col = col
        self.is_mine = False
        self.is_revealed = False
        self.is_flagged = False
        self.neighbor_mines = 0