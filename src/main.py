import tkinter as tk
from tkinter import messagebox, simpledialog
import time
from game_manager import GameManager
from menu_manager import MenuManager
from save_manager import SaveManager
from board import Board


class MinesweeperGame:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Minesweeper")
        self.root.geometry("800x600")
        self.root.configure(bg='#2C3E50')

        self.save_manager = SaveManager()
        self.menu_manager = MenuManager(self.root, self.save_manager)
        self.game_manager = None
        self.game_frame = None

        # Bind the menu_manager's start_game and load_game methods
        self.menu_manager.start_game = self.start_game
        self.menu_manager.load_game = self.load_game

        # Start with main menu
        self.menu_manager.create_main_menu()

    def clear_all_frames(self):
        # Clear menu frame
        if self.menu_manager.current_frame:
            self.menu_manager.current_frame.destroy()
            self.menu_manager.current_frame = None

        # Clear game frame
        if self.game_frame:
            self.game_frame.destroy()
            self.game_frame = None

    def create_game_grid(self):
        self.clear_all_frames()

        self.game_frame = tk.Frame(self.root, bg='#2C3E50')
        self.game_frame.pack(expand=True)

        # Create buttons grid
        self.buttons = []
        for x in range(self.game_manager.width):
            row = []
            for y in range(self.game_manager.height):
                btn = tk.Button(self.game_frame, width=2, height=1)
                btn.grid(row=y, column=x, padx=1, pady=1)
                btn.bind('<Button-1>', lambda e, x=x, y=y: self.handle_click(x, y))
                btn.bind('<Button-3>', lambda e, x=x, y=y: self.handle_right_click(x, y))
                row.append(btn)
            self.buttons.append(row)

        # Control buttons
        control_frame = tk.Frame(self.game_frame, bg='#2C3E50')
        control_frame.grid(row=self.game_manager.height + 1, column=0,
                           columnspan=self.game_manager.width, pady=10)

        tk.Button(control_frame, text="Return to Menu",
                  command=self.return_to_menu,
                  bg='#E74C3C', fg='white').pack(side=tk.LEFT, padx=5)

    def update_button(self, x, y):
        cell = self.game_manager.board.grid[x][y]
        btn = self.buttons[x][y]

        if cell.is_revealed:
            btn.config(relief=tk.SUNKEN)
            if cell.is_mine:
                btn.config(text="💣", bg="red")
            elif cell.adjacent_mines > 0:
                btn.config(text=str(cell.adjacent_mines),
                           fg=cell.get_color(),
                           bg='#ECF0F1')
            else:
                btn.config(text="", bg='#ECF0F1')
        elif cell.is_flagged:
            btn.config(text="🚩", bg='#BDC3C7')
        else:
            btn.config(text="", bg='#95A5A6')

    def handle_click(self, x, y):
        result = self.game_manager.make_move(x, y)
        self.update_display()

        if result in ["win", "game_over"]:
            self.handle_game_end(result == "win")

    def handle_right_click(self, x, y):
        self.game_manager.make_move(x, y, is_flag=True)
        self.update_display()

    def update_display(self):
        for x in range(self.game_manager.width):
            for y in range(self.game_manager.height):
                self.update_button(x, y)

    def handle_game_end(self, is_win):
        if is_win:
            message = "Congratulations! You won!"
        else:
            message = "Game Over! You hit a mine!"
            # Reveal all bombs
            for x in range(self.game_manager.width):
                for y in range(self.game_manager.height):
                    if self.game_manager.board.grid[x][y].is_mine:
                        self.game_manager.board.grid[x][y].is_revealed = True
            self.update_display()

        player_name = simpledialog.askstring("Game Over",
                                             f"{message}\nEnter your name:")
        if player_name:
            self.game_manager.save_score(player_name)

        self.return_to_menu()

    def return_to_menu(self):
        self.clear_all_frames()
        self.menu_manager.create_main_menu()

    def start_game(self, difficulty):
        self.game_manager = GameManager(difficulty, self.save_manager)
        self.game_manager.is_loaded_game = False
        self.create_game_grid()

    def load_game(self, game_data):
        # Create a src game manager with the saved difficulty
        self.game_manager = GameManager(game_data["difficulty"], self.save_manager)
        self.game_manager.is_loaded_game = True

        # Set the grid_id from the saved game
        self.game_manager.grid_id = game_data["grid_id"]

        # Update board dimensions and mines
        self.game_manager.width = game_data["width"]
        self.game_manager.height = game_data["height"]
        self.game_manager.mines = game_data["mines"]

        # Create a src board with saved dimensions
        self.game_manager.board = Board(game_data["width"], game_data["height"], game_data["mines"])

        # If this is a grid from grid details, set up the mines
        if "mine_positions" in game_data:
            for x, y in game_data["mine_positions"]:
                self.game_manager.board.grid[x][y].is_mine = True

            # Calculate adjacent mines
            for x in range(self.game_manager.width):
                for y in range(self.game_manager.height):
                    if not self.game_manager.board.grid[x][y].is_mine:
                        self.game_manager.board.grid[x][y].adjacent_mines = (
                            self.game_manager.board.count_adjacent_mines(x, y)
                        )

            # Set first cell if available
            if game_data.get("first_cell"):
                self.game_manager.board.first_cell = game_data["first_cell"]
                self.game_manager.board.first_move = False
                fx, fy = game_data["first_cell"]
                self.game_manager.board.reveal_cell(fx, fy)
        else:
            # Restore cell states from saved game
            for x in range(game_data["width"]):
                for y in range(game_data["height"]):
                    cell_data = game_data["grid"][x][y]
                    cell = self.game_manager.board.grid[x][y]
                    cell.is_mine = cell_data["is_mine"]
                    cell.is_revealed = cell_data["is_revealed"]
                    cell.is_flagged = cell_data["is_flagged"]
                    cell.adjacent_mines = cell_data["adjacent_mines"]

        # Set time elapsed
        self.game_manager.time_elapsed = game_data["time_elapsed"]

        # Create and update the game grid
        self.create_game_grid()
        self.update_display()

    def run(self):
        self.root.mainloop()


if __name__ == "__main__":
    game = MinesweeperGame()
    game.run()