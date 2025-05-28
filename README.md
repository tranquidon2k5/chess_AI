# ♔ Chess AI Master ♔

A comprehensive chess application with advanced AI, modern UI, and multiple game modes.

![Chess AI Master](https://img.shields.io/badge/Version-2.0-blue.svg)
![Python](https://img.shields.io/badge/Python-3.7+-green.svg)
![License](https://img.shields.io/badge/License-MIT-orange.svg)

## ✨ Features

### 🎮 Game Modes
- **Play vs AI** - Challenge the computer with 4 difficulty levels
- **Play vs Player** - Local multiplayer on the same device  
- **AI vs AI** - Watch two AIs battle each other
- **Settings** - Customize your experience

### 🤖 AI Features
- **4 Difficulty Levels**: Easy (depth 2) → Expert (depth 5)
- **Smart Algorithm**: Minimax with alpha-beta pruning
- **Dual Color Support**: AI works perfectly as both White and Black
- **Position Evaluation**: Advanced piece-square tables and mobility
- **Move Ordering**: Optimized for better performance

### 🎨 Modern UI
- **Beautiful Interface**: Dark theme with modern design
- **Intuitive Controls**: Click-to-move with visual feedback
- **Real-time Status**: Game state and turn indicators
- **Move History**: Track all moves in the current game
- **Game Over Detection**: Checkmate, stalemate, and draw detection

### 🎛️ Game Controls
- **New Game**: Start fresh anytime
- **Undo Move**: Take back your last move
- **Hint**: Get AI suggestions when stuck
- **Settings**: Adjust difficulty and color preferences
- **Keyboard Shortcuts**: Quick access to all features

## 🚀 Quick Start

### Installation

1. **Clone the repository**:
```bash
git clone <repository-url>
cd Chess-AI
```

2. **Install dependencies**:
```bash
pip install -r requirements.txt
```

3. **Download piece images** (if needed):
```bash
python download_assets.py
```

4. **Run the application**:
```bash
python main.py
```

## 🎯 How to Play

### Main Menu
- **Play vs AI**: Choose this to play against the computer
- **Play vs Player**: For local multiplayer games
- **AI vs AI**: Watch two AIs play each other
- **Settings**: Configure game preferences

### Settings
- **AI Difficulty**: 
  - Easy (2-ply search)
  - Medium (3-ply search) 
  - Hard (4-ply search)
  - Expert (5-ply search)
- **Choose Your Side**: Play as White or Black

### Game Controls

#### Mouse Controls
- **Left Click**: Select piece and make moves
- **Click on buttons**: Access game functions

#### Keyboard Shortcuts
- **ESC**: Return to main menu
- **N**: New game
- **U**: Undo last move
- **H**: Get hint (vs AI mode only)

#### Game Buttons
- **New Game**: Restart the current mode
- **Undo Move**: Take back the last move(s)
- **Hint**: Get AI suggestion for your next move
- **Settings**: Open settings menu
- **Main Menu**: Return to main menu

## 🧠 AI Technical Details

### Algorithm
- **Minimax with Alpha-Beta Pruning**: Efficient game tree search
- **Iterative Deepening**: Configurable search depth
- **Move Ordering**: Captures and checks prioritized

### Evaluation Function
- **Material Value**: Standard piece values (P=100, N=320, B=330, R=500, Q=900)
- **Positional Evaluation**: Piece-square tables for all pieces
- **Mobility**: Bonus for having more legal moves
- **Color-Agnostic**: Works correctly for both White and Black

### Performance
- **Nodes Evaluated**: Displayed after each AI move
- **Search Depth**: 2-5 plies depending on difficulty
- **Threading**: AI calculations run in background threads

## 📁 Project Structure

```
Chess-AI/
├── main.py                 # Application entry point
├── chess_app.py           # Main application class
├── requirements.txt       # Python dependencies
├── README.md             # This file
├── settings.json         # User settings (auto-generated)
│
├── ai/
│   ├── minimax.py        # AI algorithm implementation
│   └── __pycache__/
│
├── game/
│   ├── board.py          # Chess board wrapper
│   ├── game.py           # Legacy game class
│   ├── move_generator.py # Board evaluation functions
│   └── __pycache__/
│
├── gui/
│   ├── ui_manager.py     # Main menu and settings UI
│   ├── game_gui.py       # In-game interface
│   ├── gui.py            # Legacy GUI (kept for compatibility)
│   └── __pycache__/
│
└── assets/               # Chess piece images
    ├── wp.png, wn.png, ... # White pieces
    └── bp.png, bn.png, ... # Black pieces
```

## ⚙️ Configuration

Settings are automatically saved to `settings.json`:

```json
{
  "ai_difficulty": "HARD",
  "player_color": true,
  "ai_color": false,
  "sound_enabled": true,
  "animations_enabled": true
}
```

## 🎮 Game Modes Explained

### 1. Play vs AI
- Human player vs computer AI
- Choose your color in settings (White/Black)
- AI automatically plays the opposite color
- Undo takes back both your move and AI's response
- Hint feature available

### 2. Play vs Player  
- Two human players on same device
- Players alternate turns
- No AI involvement
- Undo takes back one move at a time

### 3. AI vs AI
- Watch two AIs play each other
- Both AIs use the selected difficulty
- Fully automated gameplay
- Good for testing AI strength

## 🔧 Advanced Features

### Custom AI Difficulty
Modify `gui/ui_manager.py` to add custom difficulties:

```python
class AIDifficulty(Enum):
    BEGINNER = ("Beginner", 1)
    EASY = ("Easy", 2)
    MEDIUM = ("Medium", 3)
    HARD = ("Hard", 4)
    EXPERT = ("Expert", 5)
    MASTER = ("Master", 6)
```

### AI Evaluation Tuning
Edit piece values and position tables in `game/move_generator.py`:

```python
PIECE_VALUES = {
    chess.PAWN: 100,
    chess.KNIGHT: 320,
    chess.BISHOP: 330,
    chess.ROOK: 500,
    chess.QUEEN: 900,
    chess.KING: 20000
}
```

## 🚀 Performance Tips

1. **Lower Difficulty**: For faster moves, use Easy or Medium
2. **Close Other Applications**: More RAM = faster AI calculations
3. **SSD Storage**: Faster file access for piece images

## 🐛 Troubleshooting

### Common Issues

**"Could not load image" warnings**:
- Run `python download_assets.py` to get piece images
- Check that `assets/` folder exists

**Slow AI moves**:
- Lower the AI difficulty in settings
- The AI shows "thinking..." status during calculation

**Game freezes**:
- AI calculations run in background threads
- Wait for the move to complete
- ESC to return to menu if needed

### Performance Monitoring

The game displays "Nodes evaluated" after each AI move to show search efficiency.

## 🤝 Contributing

Feel free to contribute improvements:

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Submit a pull request

## 📝 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🎯 Future Enhancements

- [ ] Online multiplayer
- [ ] Chess engine integration (Stockfish)
- [ ] Tournament mode
- [ ] Game analysis and replay
- [ ] Custom themes and piece sets
- [ ] Sound effects and animations
- [ ] Opening book integration
- [ ] Endgame tablebase support

---

**Enjoy playing Chess AI Master! ♔** 