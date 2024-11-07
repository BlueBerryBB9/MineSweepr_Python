import tkinter as tk
from old_cell import Cell
import random


class GameBoard:
    def __init__(self, root, size=10, mines=10):
        self.root = root
        self.size = size
        self.total_mines = mines
        self.cells = []
        self.first_click = True
        self.game_over = False

        self.create_board()

    def create_board(self):
        self.frame = tk.Frame(self.root)
        self.frame.pack()

        # Create cells
        for row in range(self.size):
            row_cells = []
            for col in range(self.size):
                button = tk.Button(
                    self.frame,
                    width=2,
                    height=1,
                    bg='lightgray'
                )
                button.grid(row=row, column=col)
                cell = Cell(button, row, col)
                button.bind('<Button-1>', lambda e, r=row, c=col: self.click(r, c))
                button.bind('<Button-3>', lambda e, r=row, c=col: self.flag(r, c))
                row_cells.append(cell)
            self.cells.append(row_cells)

    def place_mines(self, first_row, first_col):
        positions = [(r, c) for r in range(self.size) for c in range(self.size)
                     if (r, c) != (first_row, first_col)]
        mine_positions = random.sample(positions, self.total_mines)

        for row, col in mine_positions:
            self.cells[row][col].is_mine = True

        # Calculate neighbor mines
        for row in range(self.size):
            for col in range(self.size):
                if not self.cells[row][col].is_mine:
                    self.cells[row][col].neighbor_mines = self.count_neighbor_mines(row, col)

    def count_neighbor_mines(self, row, col):
        count = 0
        for r in range(max(0, row - 1), min(self.size, row + 2)):
            for c in range(max(0, col - 1), min(self.size, col + 2)):
                if self.cells[r][c].is_mine:
                    count += 1
        return count

    def click(self, row, col):
        if self.game_over:
            return

        cell = self.cells[row][col]

        if cell.is_flagged:
            return

        if self.first_click:
            self.first_click = False
            self.place_mines(row, col)

        if cell.is_mine:
            self.game_over = True
            self.reveal_all()
            self.show_message("Game Over!")
            return

        self.reveal_cell(row, col)

        if self.check_win():
            self.game_over = True
            self.show_message("You Win!")

    def reveal_cell(self, row, col):
        cell = self.cells[row][col]
        if cell.is_revealed or cell.is_flagged:
            return

        cell.is_revealed = True
        cell.button.config(relief=tk.SUNKEN)

        if cell.neighbor_mines == 0:
            cell.button.config(bg='white')
            # Reveal neighbors
            for r in range(max(0, row - 1), min(self.size, row + 2)):
                for c in range(max(0, col - 1), min(self.size, col + 2)):
                    if not self.cells[r][c].is_revealed:
                        self.reveal_cell(r, c)
        else:
            cell.button.config(
                text=cell.neighbor_mines,
                bg='white',
                fg=['blue', 'green', 'red', 'purple', 'maroon', 'turquoise', 'black', 'gray'][cell.neighbor_mines - 1]
            )

    def flag(self, row, col):
        if self.game_over:
            return

        cell = self.cells[row][col]
        if not cell.is_revealed:
            cell.is_flagged = not cell.is_flagged
            cell.button.config(text='🚩' if cell.is_flagged else '')

    def reveal_all(self):
        for row in self.cells:
            for cell in row:
                if cell.is_mine:
                    cell.button.config(text='💣', bg='red')

    def check_win(self):
        for row in self.cells:
            for cell in row:
                if not cell.is_mine and not cell.is_revealed:
                    return False
        return True

    def show_message(self, message):
        for row in self.cells:
            for cell in row:
                cell.button.config(state=tk.DISABLED)
        tk.messagebox.showinfo("Game Status", message)