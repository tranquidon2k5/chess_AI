# Chess AI Game

A chess game where you can play against an AI opponent using the Minimax algorithm with alpha-beta pruning.

## Features

- Graphical user interface using Pygame
- AI opponent using Minimax algorithm with alpha-beta pruning
- Legal move validation using python-chess
- Piece-square table evaluation for better AI play
- Visual move highlighting and piece selection
- Game state tracking (checkmate, stalemate, etc.)

## Setup

1. Install the required dependencies:
```bash
pip install -r requirements.txt
```

2. Create an `assets` directory in the project root:
```bash
mkdir assets
```

3. Download chess piece images:
   - You can find chess piece images online (e.g., from chess.com or other chess websites)
   - Save them in the `assets` directory with the following naming convention:
     - White pieces: `wp.png`, `wn.png`, `wb.png`, `wr.png`, `wq.png`, `wk.png`
     - Black pieces: `bp.png`, `bn.png`, `bb.png`, `br.png`, `bq.png`, `bk.png`
   - Make sure the images are square and preferably in PNG format with transparency

## How to Play

1. Run the game:
```bash
python main.py
```

2. Game Controls:
   - Left-click to select and move pieces
   - Press 'R' to reset the game
   - Close the window to quit

3. Game Rules:
   - You play as White
   - The AI plays as Black
   - Standard chess rules apply
   - The game will automatically detect checkmate, stalemate, and other game-ending conditions

## Project Structure

- `main.py`: Entry point of the game
- `game/`
  - `board.py`: Chess board state management
  - `game.py`: Main game logic and coordination
  - `move_generator.py`: Move evaluation and piece-square tables
- `ai/`
  - `minimax.py`: Minimax algorithm with alpha-beta pruning
- `gui/`
  - `gui.py`: Graphical interface using Pygame
- `assets/`: Chess piece images

## Future Improvements

- Add difficulty levels
- Implement move history and undo functionality
- Add sound effects
- Add a menu system
- Implement save/load game functionality
- Add multiplayer support 