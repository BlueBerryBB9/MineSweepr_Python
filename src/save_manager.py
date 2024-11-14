import json
import os
from datetime import datetime
import hashlib


class SaveManager:
    def __init__(self):
        self.save_file = "minesweeper_saves.json"
        self.ensure_save_file_exists()

    def ensure_save_file_exists(self):
        if not os.path.exists(self.save_file):
            initial_data = {
                "games": [],
                "grids": {},
                "scores": {}
            }
            with open(self.save_file, 'w') as f:
                json.dump(initial_data, f, indent=4)

    def generate_grid_id(self, grid_data):
        """Generate a unique ID for a grid based on its configuration"""
        grid_str = ""
        for x in range(len(grid_data)):
            for y in range(len(grid_data[x])):
                if grid_data[x][y]["is_mine"]:
                    grid_str += f"{x},{y};"

        # Add first cell coordinates if available
        if grid_data[0][0].get("first_cell"):
            grid_str += f"first:{grid_data[0][0]['first_cell']}"

        return hashlib.md5(grid_str.encode()).hexdigest()

    def save_game(self, difficulty, board, time_elapsed):
        grid_data = [[{
            "is_mine": cell.is_mine,
            "is_revealed": cell.is_revealed,
            "is_flagged": cell.is_flagged,
            "adjacent_mines": cell.adjacent_mines,
            "first_cell": f"{board.first_cell[0]},{board.first_cell[1]}" if board.first_cell else None
        } for cell in row] for row in board.grid]

        grid_id = self.generate_grid_id(grid_data)

        game_state = {
            "grid_id": grid_id,
            "difficulty": difficulty,
            "width": board.width,
            "height": board.height,
            "mines": board.mines,
            "grid": grid_data,
            "timestamp": datetime.now().isoformat(),
            "time_elapsed": time_elapsed
        }

        with open(self.save_file, 'r+') as f:
            data = json.load(f)

            # Store grid configuration if it's src
            if grid_id not in data["grids"]:
                data["grids"][grid_id] = {
                    "difficulty": difficulty,
                    "width": board.width,
                    "height": board.height,
                    "mines": board.mines,
                    "mine_positions": [(x, y) for x in range(board.width)
                                       for y in range(board.height)
                                       if board.grid[x][y].is_mine],
                    "first_cell": board.first_cell,
                    "created_at": datetime.now().isoformat()
                }

            data["games"].append(game_state)
            f.seek(0)
            json.dump(data, f, indent=4)
            f.truncate()

    def load_games(self):
        with open(self.save_file, 'r') as f:
            data = json.load(f)
            return data["games"]

    def save_score(self, difficulty, player_name, score, time_elapsed, grid_id):
        with open(self.save_file, 'r+') as f:
            data = json.load(f)

            # Initialize scores for this grid if needed
            if grid_id not in data["scores"]:
                data["scores"][grid_id] = []

            # Add score
            score_data = {
                "player": player_name,
                "score": score,
                "time": time_elapsed,
                "timestamp": datetime.now().isoformat(),
                "difficulty": difficulty,
                "grid_id": grid_id
            }

            data["scores"][grid_id].append(score_data)
            data["scores"][grid_id].sort(key=lambda x: (-x["score"], x["time"]))

            f.seek(0)
            json.dump(data, f, indent=4)
            f.truncate()

    def get_scores(self, difficulty=None, grid_id=None):
        with open(self.save_file, 'r') as f:
            data = json.load(f)

            if grid_id:
                return data["scores"].get(grid_id, [])
            elif difficulty:
                all_scores = []
                for grid_scores in data["scores"].values():
                    all_scores.extend([score for score in grid_scores
                                       if score["difficulty"] == difficulty])
                all_scores.sort(key=lambda x: (-x["score"], x["time"]))
                return all_scores
            return []

    def get_grid_info(self, grid_id):
        with open(self.save_file, 'r') as f:
            data = json.load(f)
            return data["grids"].get(grid_id)

    def get_all_grids(self):
        with open(self.save_file, 'r') as f:
            data = json.load(f)
            return data["grids"]