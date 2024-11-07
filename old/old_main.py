import tkinter as tk
from tkinter import messagebox
from old_game_board import GameBoard


class MinesweeperGame:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Minesweeper")

        # Menu
        menubar = tk.Menu(self.root)
        game_menu = tk.Menu(menubar, tearoff=0)
        game_menu.add_command(label="New Game", command=self.new_game)
        menubar.add_cascade(label="Game", menu=game_menu)
        self.root.config(menu=menubar)

        self.board = GameBoard(self.root)

    def new_game(self):
        self.board.frame.destroy()
        self.board = GameBoard(self.root)

    def run(self):
        self.root.mainloop()


if __name__ == "__main__":
    game = MinesweeperGame()
    game.run()