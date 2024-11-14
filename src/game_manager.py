import time
import tkinter as tk
from board import Board


class GameManager:
    def __init__(self, difficulty, save_manager):
        self.difficulties = {
            "Easy": (9, 9, 10),
            "Medium": (16, 16, 40),
            "Hard": (30, 16, 99)
        }
        self.difficulty = difficulty
        self.save_manager = save_manager
        self.width, self.height, self.mines = self.difficulties[difficulty]
        self.board = Board(self.width, self.height, self.mines)
        self.start_time = None
        self.time_elapsed = 0
        self.moves = []
        self.is_loaded_game = False
        self.grid_id = None

    def start_game(self):
        self.start_time = time.time()

    def make_move(self, x, y, is_flag=False):
        was_first_move = self.start_time is None

        if was_first_move:
            self.start_game()

        if is_flag:
            self.board.toggle_flag(x, y)
        else:
            self.board.reveal_cell(x, y)

        self.moves.append((x, y, is_flag))

        # Auto-save after first move only for src games
        if was_first_move and not is_flag and not self.is_loaded_game:
            # Calculate current time elapsed
            current_time = 0
            if self.start_time is not None:
                current_time = self.time_elapsed or (time.time() - self.start_time)
            self.save_game(current_time)
            # Generate grid_id after first move
            self.grid_id = self.save_manager.generate_grid_id(
                [[{
                    "is_mine": cell.is_mine,
                    "is_revealed": cell.is_revealed,
                    "is_flagged": cell.is_flagged,
                    "adjacent_mines": cell.adjacent_mines,
                    "first_cell": f"{self.board.first_cell[0]},{self.board.first_cell[1]}"
                } for cell in row] for row in self.board.grid]
            )

        if self.board.game_over:
            self.time_elapsed = time.time() - self.start_time
            return "game_over"

        if self.board.check_win():
            self.time_elapsed = time.time() - self.start_time
            return "win"

        return "continue"

    def save_game(self, current_time=None):
        if current_time is None:
            current_time = self.time_elapsed or (time.time() - self.start_time)

        self.save_manager.save_game(
            self.difficulty,
            self.board,
            current_time
        )

    def save_score(self, player_name):
        completion = self.board.get_completion_percentage()
        self.save_manager.save_score(
            self.difficulty,
            player_name,
            completion,
            self.time_elapsed,
            self.grid_id
        )

    def restart_game(self):
        self.board.reset_with_same_first_move()
        self.start_time = None
        self.time_elapsed = 0
        self.moves = []