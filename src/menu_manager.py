import tkinter as tk
from tkinter import ttk
from datetime import datetime


def format_timestamp(iso_timestamp):
    """Convert ISO timestamp to short readable format"""
    timestamp = datetime.fromisoformat(iso_timestamp)
    return timestamp.strftime("%m/%d/%y %I:%M %p")


class MenuManager:

    def __init__(self, root, save_manager):
        self.root = root
        self.save_manager = save_manager
        self.current_frame = None

    def clear_window(self):
        if self.current_frame:
            self.current_frame.destroy()

    def create_main_menu(self):
        self.clear_window()
        frame = tk.Frame(self.root, bg='#2C3E50')
        frame.pack(expand=True)
        self.current_frame = frame

        title = tk.Label(frame, text="MINESWEEPER",
                         font=('Helvetica', 32, 'bold'),
                         fg='#E74C3C', bg='#2C3E50')
        title.pack(pady=30)

        self.create_menu_button(frame, "Play", self.create_play_menu, '#2ECC71')
        self.create_menu_button(frame, "Scoreboard", self.create_scoreboard_menu, '#3498DB')
        self.create_menu_button(frame, "Quit", self.root.quit, '#E74C3C')

    def create_menu_button(self, parent, text, command, color):
        btn = tk.Button(
            parent,
            text=text,
            command=command,
            width=20,
            font=('Helvetica', 12, 'bold'),
            bg=color,
            fg='white',
            relief=tk.RAISED,
            bd=0,
            padx=20,
            pady=10
        )
        btn.pack(pady=10)

    def create_play_menu(self):
        self.clear_window()
        frame = tk.Frame(self.root, bg='#2C3E50')
        frame.pack(expand=True)
        self.current_frame = frame

        title = tk.Label(frame, text="Play Game",
                         font=('Helvetica', 24, 'bold'),
                         fg='#ECF0F1', bg='#2C3E50')
        title.pack(pady=30)

        self.create_menu_button(frame, "New Game", self.create_difficulty_menu, '#2ECC71')
        self.create_menu_button(frame, "Load Game", self.create_load_game_menu, '#3498DB')
        self.create_menu_button(frame, "Return", self.create_main_menu, '#E74C3C')

    def create_difficulty_menu(self):
        self.clear_window()
        frame = tk.Frame(self.root, bg='#2C3E50')
        frame.pack(expand=True)
        self.current_frame = frame

        title = tk.Label(frame, text="Select Difficulty",
                         font=('Helvetica', 24, 'bold'),
                         fg='#ECF0F1', bg='#2C3E50')
        title.pack(pady=30)

        difficulties = {
            "Easy": {'size': (9, 9), 'mines': 10, 'color': '#2ECC71'},
            "Medium": {'size': (16, 16), 'mines': 40, 'color': '#F1C40F'},
            "Hard": {'size': (30, 16), 'mines': 99, 'color': '#E74C3C'}
        }

        for diff_name, settings in difficulties.items():
            size = settings['size']
            mines = settings['mines']
            text = f"{diff_name}\n{size[0]}x{size[1]}, {mines} mines"
            self.create_menu_button(frame, text,
                                    lambda d=diff_name: self.start_game(d),
                                    settings['color'])

        self.create_menu_button(frame, "Return", self.create_play_menu, '#7F8C8D')

    def create_scoreboard_menu(self):
        self.clear_window()
        frame = tk.Frame(self.root, bg='#2C3E50')
        frame.pack(expand=True)
        self.current_frame = frame

        title = tk.Label(frame, text="High Scores",
                         font=('Helvetica', 24, 'bold'),
                         fg='#ECF0F1', bg='#2C3E50')
        title.pack(pady=30)

        # Create notebook for tabs
        notebook = ttk.Notebook(frame)
        notebook.pack(pady=10, expand=True, fill='both')

        # Tab for difficulty-based scores
        diff_frame = tk.Frame(notebook, bg='#2C3E50')
        notebook.add(diff_frame, text='By Difficulty')

        difficulties = ["Easy", "Medium", "Hard"]

        for difficulty in difficulties:
            tk.Label(diff_frame, text=f"{difficulty} Scores:",
                     fg='#ECF0F1', bg='#2C3E50',
                     font=('Helvetica', 14, 'bold')).pack(pady=10)

            scores = self.save_manager.get_scores(difficulty=difficulty)
            if not scores:
                tk.Label(diff_frame, text="No scores yet",
                         fg='#ECF0F1', bg='#2C3E50').pack()
            else:
                for score in scores[:5]:  # Show top 5 scores
                    score_text = f"{score['player']}: {score['score']:.1f}% ({score['time']:.1f}s)"
                    btn = tk.Button(diff_frame, text=score_text,
                                    command=lambda s=score: self.show_grid_details(s.get('grid_id')),
                                    bg='#34495E', fg='#ECF0F1')
                    btn.pack(pady=2)

        # Tab for grid-based scores
        grid_frame = tk.Frame(notebook, bg='#2C3E50')
        notebook.add(grid_frame, text='By Grid')

        grids = self.save_manager.get_all_grids()
        if not grids:
            tk.Label(grid_frame, text="No grids available",
                     fg='#ECF0F1', bg='#2C3E50').pack(pady=20)
        else:
            for grid_id, grid_info in grids.items():
                grid_scores = self.save_manager.get_scores(grid_id=grid_id)
                if grid_scores:
                    frame = tk.Frame(grid_frame, bg='#2C3E50')
                    frame.pack(fill='x', pady=5)

                    header = f"Grid {grid_id[:8]} ({grid_info['difficulty']})"
                    btn = tk.Button(frame, text=header,
                                    command=lambda gid=grid_id: self.show_grid_details(gid),
                                    bg='#34495E', fg='#ECF0F1')
                    btn.pack(fill='x')

        frame = self.current_frame
        self.create_menu_button(frame, "Return", self.create_main_menu, '#E74C3C')

    def show_grid_details(self, grid_id):
        if not grid_id:
            return

        grid_info = self.save_manager.get_grid_info(grid_id)
        if not grid_info:
            return

        self.clear_window()
        frame = tk.Frame(self.root, bg='#2C3E50')
        frame.pack(expand=True)
        self.current_frame = frame

        title = tk.Label(frame, text="Grid Details",
                         font=('Helvetica', 24, 'bold'),
                         fg='#ECF0F1', bg='#2C3E50')
        title.pack(pady=20)

        info_frame = tk.Frame(frame, bg='#2C3E50')
        info_frame.pack(pady=10)

        tk.Label(info_frame, text=f"Difficulty: {grid_info['difficulty']}",
                 fg='#ECF0F1', bg='#2C3E50', font=('Helvetica', 12)).pack()
        tk.Label(info_frame, text=f"Size: {grid_info['width']}x{grid_info['height']}",
                 fg='#ECF0F1', bg='#2C3E50', font=('Helvetica', 12)).pack()
        tk.Label(info_frame, text=f"Mines: {grid_info['mines']}",
                 fg='#ECF0F1', bg='#2C3E50', font=('Helvetica', 12)).pack()

        scores = self.save_manager.get_scores(grid_id=grid_id)
        if scores:
            tk.Label(frame, text="Top Scores:", fg='#ECF0F1', bg='#2C3E50',
                     font=('Helvetica', 14, 'bold')).pack(pady=10)
            for score in scores[:5]:
                score_text = f"{score['player']}: {score['score']:.1f}% ({score['time']:.1f}s)"
                tk.Label(frame, text=score_text,
                         fg='#ECF0F1', bg='#2C3E50').pack(pady=2)

        # Create a game state object from grid info
        game_state = {
            "grid_id": grid_id,
            "difficulty": grid_info["difficulty"],
            "width": grid_info["width"],
            "height": grid_info["height"],
            "mines": grid_info["mines"],
            "mine_positions": grid_info["mine_positions"],
            "first_cell": grid_info["first_cell"],
            "timestamp": grid_info["created_at"],
            "time_elapsed": 0  # Start fresh
        }

        self.create_menu_button(frame, "Play This Grid",
                                lambda: self.load_game(game_state), '#2ECC71')
        self.create_menu_button(frame, "Back",
                                self.create_scoreboard_menu, '#E74C3C')

    def create_load_game_menu(self):
        self.clear_window()
        frame = tk.Frame(self.root, bg='#2C3E50')
        frame.pack(expand=True)
        self.current_frame = frame

        title = tk.Label(frame, text="Load Game",
                         font=('Helvetica', 24, 'bold'),
                         fg='#ECF0F1', bg='#2C3E50')
        title.pack(pady=30)

        games = self.save_manager.load_games()
        if not games:
            tk.Label(frame, text="No saved games found",
                     fg='#ECF0F1', bg='#2C3E50').pack(pady=20)
        else:
            for game in games:
                formatted_time = format_timestamp(game['timestamp'])
                game_text = f"{game['difficulty']} - {formatted_time}"
                self.create_menu_button(frame, game_text,
                                        lambda g=game: self.load_game(g), '#3498DB')

        self.create_menu_button(frame, "Return", self.create_play_menu, '#E74C3C')

    # These methods will be bound by the main game class
    def start_game(self, difficulty):
        pass

    def load_game(self, game_data):
        pass