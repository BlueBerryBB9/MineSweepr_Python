import tkinter
from game_board

class Game:
    def __init__(self):
        in_menu = True
        
        board = GameBoard()

    def run(self):
        self.root.mainloop()

if __name__ == "__main__":
    game = Game()
    Game.launch()