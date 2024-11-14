import random
from src.cell import Cell


class Board:
    def __init__(self, width, height, mines):
        self.width = width
        self.height = height
        self.mines = mines
        self.grid = [[Cell(x, y) for y in range(height)] for x in range(width)]
        self.first_move = True
        self.first_cell = None
        self.game_over = False
        self.won = False

    def place_mines(self, first_x, first_y):
        self.first_cell = (first_x, first_y)
        # Clear area around first click
        safe_cells = [(x, y) for x in range(max(0, first_x - 1), min(self.width, first_x + 2))
                      for y in range(max(0, first_y - 1), min(self.height, first_y + 2))]

        # Place mines randomly
        possible_positions = [(x, y) for x in range(self.width) for y in range(self.height)
                              if (x, y) not in safe_cells]
        mine_positions = random.sample(possible_positions, self.mines)

        for x, y in mine_positions:
            self.grid[x][y].is_mine = True

        # Calculate adjacent mines
        for x in range(self.width):
            for y in range(self.height):
                if not self.grid[x][y].is_mine:
                    self.grid[x][y].adjacent_mines = self.count_adjacent_mines(x, y)

    def reset_with_same_first_move(self):
        if self.first_cell is None:
            return

        for x in range(self.width):
            for y in range(self.height):
                self.grid[x][y].reset()

        self.game_over = False
        self.won = False
        self.first_move = False

        # Place mines keeping the same first cell
        self.place_mines(*self.first_cell)
        # Reveal the first cell
        self.reveal_cell(*self.first_cell)

    def count_adjacent_mines(self, x, y):
        count = 0
        for dx in [-1, 0, 1]:
            for dy in [-1, 0, 1]:
                if dx == 0 and dy == 0:
                    continue
                new_x, new_y = x + dx, y + dy
                if (0 <= new_x < self.width and
                        0 <= new_y < self.height and
                        self.grid[new_x][new_y].is_mine):
                    count += 1
        return count

    def reveal_cell(self, x, y):
        if self.first_move:
            self.place_mines(x, y)
            self.first_move = False

        cell = self.grid[x][y]
        if cell.is_flagged or cell.is_revealed:
            return

        cell.is_revealed = True

        if cell.is_mine:
            self.game_over = True
            return

        if cell.adjacent_mines == 0:
            self.reveal_adjacent_cells(x, y)

    def reveal_adjacent_cells(self, x, y):
        for dx in [-1, 0, 1]:
            for dy in [-1, 0, 1]:
                if dx == 0 and dy == 0:
                    continue
                new_x, new_y = x + dx, y + dy
                if (0 <= new_x < self.width and
                        0 <= new_y < self.height and
                        not self.grid[new_x][new_y].is_revealed):
                    self.reveal_cell(new_x, new_y)

    def toggle_flag(self, x, y):
        cell = self.grid[x][y]
        if not cell.is_revealed:
            cell.is_flagged = not cell.is_flagged

    def check_win(self):
        for x in range(self.width):
            for y in range(self.height):
                cell = self.grid[x][y]
                if cell.is_mine and not cell.is_flagged:
                    return False
                if not cell.is_mine and not cell.is_revealed:
                    return False
        self.won = True
        return True

    def get_completion_percentage(self):
        total_cells = self.width * self.height
        revealed_cells = sum(1 for x in range(self.width)
                             for y in range(self.height)
                             if self.grid[x][y].is_revealed and not self.grid[x][y].is_mine)
        correct_flags = sum(1 for x in range(self.width)
                            for y in range(self.height)
                            if self.grid[x][y].is_flagged and self.grid[x][y].is_mine)
        return ((revealed_cells + correct_flags) / total_cells) * 100