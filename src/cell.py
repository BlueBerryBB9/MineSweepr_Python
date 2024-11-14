class Cell:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.is_mine = False
        self.is_revealed = False
        self.is_flagged = False
        self.adjacent_mines = 0

    def reset(self):
        self.is_mine = False
        self.is_revealed = False
        self.is_flagged = False
        self.adjacent_mines = 0

    def get_color(self):
        colors = {
            1: '#0000FF',  # Blue
            2: '#008000',  # Green
            3: '#FF0000',  # Red
            4: '#000080',  # Navy
            5: '#800000',  # Maroon
            6: '#008080',  # Teal
            7: '#000000',  # Black
            8: '#808080'  # Gray
        }
        return colors.get(self.adjacent_mines, '#000000')