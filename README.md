# 3D Minesweeper

A modern implementation of the classic Minesweeper game with advanced features like save states, scoreboards, and grid replays.

## Features & User Stories

### Menu System (Wissal)
- ✅ Interactive main menu with options to:
  - Start new game
  - View scoreboard
  - Quit game
- ✅ Difficulty selection:
  - Easy (9x9 grid, 10 mines)
  - Medium (16x16 grid, 40 mines)
  - Hard (30x16 grid, 99 mines)

### Grid Generation & Scoring (Martin)
- ✅ Dynamic grid generation based on difficulty
  - Ensures maximum of one mine per cell
  - Generates unique grid layouts
- ✅ Comprehensive scoring system
  - Player name registration
  - Score tracking per grid
  - Historical scores viewable per grid
- ✅ Grid replay functionality
  - Ability to replay any previously played grid
  - Maintains grid history across game sessions

### Gameplay Mechanics (Noah)
- ✅ Cell interaction system
  - Left-click to reveal cells
  - Right-click to place flags on suspected mines
  - Adjacent mine counter display
- ✅ First-click protection
  - Initial click always reveals a safe cell
  - Consistent first cell position on grid replays
- ✅ Auto-reveal mechanism
  - Recursively reveals adjacent empty cells
  - Shows numbers for cells adjacent to mines
- ✅ Win/Lose conditions
  - Game over on mine revelation
  - Victory when all mines are correctly flagged
  - All safe cells revealed

## Technical Implementation

### Grid Management
- Dynamic grid generation algorithm
- Mine placement optimization
- Adjacent mine calculation system

### Save System
- Persistent storage for game states
- Score tracking database
- Grid layout preservation

### User Interface
- Tkinter-based GUI
- Responsive grid display
- Interactive menu system

## Project Structure
├── main.py              # Game initialization and main loop
├── board.py             # Grid and cell management
├── cell.py              # Individual cell properties
├── game_manager.py      # Game state and logic handling
├── menu_manager.py      # Menu system and UI
└── save_manager.py      # Save state and scoring system



## Getting Started

1. Ensure Python 3.x is installed
2. Run `python main.py` to start the game
3. Select difficulty from the main menu
4. Left-click to reveal cells, right-click to place flags
5. Complete the grid by finding all mines

## Contributors
- Martin: Grid generation, scoring system, replay functionality
- Wissal: Menu system, difficulty management
- Noah: Core gameplay mechanics, win/lose conditions
