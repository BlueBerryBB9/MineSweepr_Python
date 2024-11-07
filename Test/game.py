import tkinter as tk
from tkinter import messagebox, ttk, simpledialog
import random
import json
from datetime import datetime
from models import Cell, Difficulty

class Minesweeper:
    def __init__(self):
        self.window = tk.Tk()
        self.window.title("Minesweeper")
        self.current_difficulty = None
        self.grid = []
        self.buttons = []
        self.first_move = True
        self.first_cell = None
        self.game_frame = None
        self.score_label = None
        self.start_time = None
        self.load_scores()
        self.create_menu()

    def load_scores(self):
        try:
            with open('scores.json', 'r') as f:
                self.scores = json.load(f)
        except FileNotFoundError:
            self.scores = {"Easy": [], "Medium": [], "Hard": []}

    def save_scores(self):
        with open('scores.json', 'w') as f:
            json.dump(self.scores, f)

    def create_menu(self):
        self.menu_frame = tk.Frame(self.window)
        self.menu_frame.pack(padx=20, pady=20)

        tk.Label(self.menu_frame, text="Minesweeper", font=('Arial', 24, 'bold')).pack(pady=10)

        difficulties = [Difficulty.EASY, Difficulty.MEDIUM, Difficulty.HARD]
        for diff in difficulties:
            btn = tk.Button(
                self.menu_frame,
                text=f"{diff['name']} ({diff['size'][0]}x{diff['size'][1]}, {diff['mines']} mines)",
                command=lambda d=diff: self.start_game(d)
            )
            btn.pack(pady=5)

        tk.Button(self.menu_frame, text="View Scores", command=self.show_scores).pack(pady=5)
        tk.Button(self.menu_frame, text="Quit", command=self.window.quit).pack(pady=5)

    def show_scores(self):
        score_window = tk.Toplevel(self.window)
        score_window.title("High Scores")

        notebook = ttk.Notebook(score_window)
        notebook.pack(padx=10, pady=10)

        for difficulty in ["Easy", "Medium", "Hard"]:
            frame = ttk.Frame(notebook)
            notebook.add(frame, text=difficulty)

            scores = sorted(self.scores[difficulty], key=lambda x: x['time'])
            for i, score in enumerate(scores[:10], 1):
                tk.Label(
                    frame,
                    text=f"{i}. {score['name']}: {score['time']} seconds"
                ).pack(pady=2)

    def start_game(self, difficulty):
        self.current_difficulty = difficulty
        self.menu_frame.pack_forget()

        if self.game_frame:
            self.game_frame.destroy()

        self.game_frame = tk.Frame(self.window)
        self.game_frame.pack(padx=20, pady=20)

        self.score_label = tk.Label(self.game_frame, text="Time: 0")
        self.score_label.pack(pady=5)

        tk.Button(self.game_frame, text="Back to Menu", command=self.return_to_menu).pack(pady=5)

        self.initialize_grid(difficulty['size'][0], difficulty['size'][1])
        self.create_buttons()
        self.first_move = True
        self.start_time = datetime.now()
        self.update_timer()

    def return_to_menu(self):
        if self.game_frame:
            self.game_frame.destroy()
        self.menu_frame.pack()

    def initialize_grid(self, width, height):
        self.grid = [[Cell(x, y) for y in range(height)] for x in range(width)]
        self.buttons = [[None for _ in range(height)] for _ in range(width)]

    def create_buttons(self):
        buttons_frame = tk.Frame(self.game_frame)
        buttons_frame.pack()

        for x in range(len(self.grid)):
            for y in range(len(self.grid[0])):
                btn = tk.Button(
                    buttons_frame,
                    width=2,
                    height=1,
                    command=lambda x=x, y=y: self.handle_click(x, y)
                )
                btn.grid(row=y, column=x)
                btn.bind('<Button-3>', lambda e, x=x, y=y: self.handle_right_click(x, y))
                self.buttons[x][y] = btn

    def place_mines(self, first_x, first_y):
        width = len(self.grid)
        height = len(self.grid[0])
        mine_count = self.current_difficulty['mines']

        positions = [(x, y) for x in range(width) for y in range(height)
                    if not (abs(x - first_x) <= 1 and abs(y - first_y) <= 1)]

        mine_positions = random.sample(positions, mine_count)

        for x, y in mine_positions:
            self.grid[x][y].is_mine = True

        for x in range(width):
            for y in range(height):
                if not self.grid[x][y].is_mine:
                    self.grid[x][y].adjacent_mines = self.count_adjacent_mines(x, y)

    def count_adjacent_mines(self, x, y):
        count = 0
        for dx in [-1, 0, 1]:
            for dy in [-1, 0, 1]:
                if dx == 0 and dy == 0:
                    continue
                new_x, new_y = x + dx, y + dy
                if (0 <= new_x < len(self.grid) and
                    0 <= new_y < len(self.grid[0]) and
                    self.grid[new_x][new_y].is_mine):
                    count += 1
        return count

    def handle_click(self, x, y):
        if self.first_move:
            self.first_move = False
            self.first_cell = (x, y)
            self.place_mines(x, y)
            self.reveal_cell(x, y)
        else:
            if not self.grid[x][y].is_flagged:
                if self.grid[x][y].is_mine:
                    self.game_over()
                else:
                    self.reveal_cell(x, y)
                    if self.check_win():
                        self.handle_win()

    def handle_right_click(self, x, y, event=None):
        if not self.grid[x][y].is_revealed:
            cell = self.grid[x][y]
            cell.is_flagged = not cell.is_flagged
            self.buttons[x][y].configure(
                text='🚩' if cell.is_flagged else '',
                fg='red' if cell.is_flagged else 'black'
            )
            if self.check_win():
                self.handle_win()

    def reveal_cell(self, x, y):
        cell = self.grid[x][y]
        if cell.is_revealed or cell.is_flagged:
            return

        cell.is_revealed = True
        if cell.adjacent_mines == 0:
            self.buttons[x][y].configure(text='', relief=tk.SUNKEN)
            for dx in [-1, 0, 1]:
                for dy in [-1, 0, 1]:
                    new_x, new_y = x + dx, y + dy
                    if (0 <= new_x < len(self.grid) and
                        0 <= new_y < len(self.grid[0])):
                        self.reveal_cell(new_x, new_y)
        else:
            self.buttons[x][y].configure(
                text=str(cell.adjacent_mines),
                relief=tk.SUNKEN
            )

    def check_win(self):
        for x in range(len(self.grid)):
            for y in range(len(self.grid[0])):
                cell = self.grid[x][y]
                if not cell.is_mine and not cell.is_revealed:
                    return False
                if cell.is_mine and not cell.is_flagged:
                    return False
        return True

    def game_over(self):
        for x in range(len(self.grid)):
            for y in range(len(self.grid[0])):
                if self.grid[x][y].is_mine:
                    self.buttons[x][y].configure(text='💣', bg='red')
        messagebox.showinfo("Game Over", "You hit a mine!")
        self.return_to_menu()

    def handle_win(self):
        elapsed_time = int((datetime.now() - self.start_time).total_seconds())
        name = simpledialog.askstring("Congratulations!",
            f"You won in {elapsed_time} seconds!\nEnter your name:")

        if name:
            self.scores[self.current_difficulty['name']].append({
                'name': name,
                'time': elapsed_time
            })
            self.save_scores()

        self.return_to_menu()

    def update_timer(self):
        if self.score_label and not self.first_move:
            elapsed_time = int((datetime.now() - self.start_time).total_seconds())
            self.score_label.configure(text=f"Time: {elapsed_time}")
        self.window.after(1000, self.update_timer)

    def run(self):
        self.window.mainloop()