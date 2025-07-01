# Tetris AI Project

A sophisticated Tetris implementation featuring both manual gameplay and AI players with genetic algorithm optimization. This project includes multiple visualization options, advanced AI strategies, and a genetic algorithm framework for optimizing AI performance.

## Features

### Core Gameplay
- **Classic Tetris Mechanics**: Standard 10x24 game board with all 7 tetromino pieces
- **Advanced Features**: 
  - Bomb pieces that clear surrounding blocks
  - Discard tokens to skip unwanted pieces
  - Next piece preview
  - Score tracking

### AI Players
- **Custom AI Player**: Heuristic-based AI with configurable weights
- **Random Player**: Baseline random move generator
- **Genetic Algorithm**: Automated optimization of AI parameters
- **Multiple Heuristics**:
  - Height minimization
  - Hole counting
  - Surface smoothness
  - Line completion rewards
  - Bad line penalties
  - Right column height control

### Visualization Options
- **Terminal Interface**: Curses-based text interface with color coding
- **Tkinter GUI**: Cross-platform graphical interface
- **Pygame Interface**: Modern graphics with smooth animations

### Network Capabilities
- **Client-Server Architecture**: Multiplayer support via TCP/IP
- **Wire Protocol**: Custom communication protocol for game state synchronization

##  Installation

### Prerequisites
- Python 3.7+
- Required packages (install via pip):
  ```bash
  pip install pygame
  ```

### Setup
1. Clone the repository:
   ```bash
   git clone <repository-url>
   cd tetris-1
   ```

2. The project uses standard Python libraries except for pygame, which is used for the enhanced visual interface.

##  Usage

### Manual Gameplay

#### Terminal Interface
```bash
python cmdline.py --manual
```

**Controls:**
- Arrow keys: Move pieces
- Space: Drop piece
- Z/X: Rotate piece
- B: Use bomb
- D: Discard piece
- ESC/Q: Quit

#### Tkinter GUI
```bash
python visual.py --manual
```

#### Pygame Interface
```bash
python genetic_alg.py --manual
```

### AI Gameplay

#### Watch AI Play
```bash
# Terminal interface
python cmdline.py

# Tkinter GUI
python visual.py

# Pygame interface
python genetic_alg.py
```

#### Genetic Algorithm Training
```bash
python genetic_alg.py
```
The genetic algorithm will automatically run and optimize AI parameters for maximum score.

### Network Play

#### Start Server
```bash
python server.py
```

#### Connect Client
```bash
python client.py <server-ip>
```

## 🧠 AI Architecture

### Custom Player Heuristics
The AI uses a weighted combination of board evaluation metrics:

- **Height Heuristic**: Penalizes high stacks
- **Holes Heuristic**: Penalizes gaps under blocks
- **Smoothness Heuristic**: Rewards flat surfaces
- **Fourth Line Heuristic**: Rewards line completions
- **Bad Lines Heuristic**: Penalizes problematic line configurations
- **Right Column Height**: Controls right-side stacking

### Genetic Algorithm
The genetic algorithm optimizes these heuristic weights through:
- Population-based evolution
- Tournament selection
- Crossover breeding
- Mutation operators
- Fitness evaluation based on game scores

## 📁 Project Structure

```
tetris-1/
├── board.py              # Core game logic and board management
├── player.py             # AI player implementations
├── genetic_alg.py        # Genetic algorithm optimization
├── cmdline.py            # Terminal interface
├── visual.py             # Tkinter GUI
├── visual-pygame.py      # Pygame interface
├── server.py             # Network server
├── client.py             # Network client
├── adversary.py          # Piece generation and game flow
├── constants.py          # Game configuration
├── exceptions.py         # Custom exceptions
├── arguments.py          # Command line argument parsing
└── Segment7-4Gml.otf     # Font file for score display
```

##  Performance

The optimized AI can achieve scores of 50,000+ points through:
- Sophisticated board evaluation
- Look-ahead planning
- Strategic use of bombs and discards
- Genetic algorithm optimization

##  Configuration

### Game Parameters
Edit `constants.py` to modify:
- Board dimensions
- Game speed
- Block limits
- Default seed

### AI Parameters
Modify heuristic weights in `player.py` or use the genetic algorithm for automatic optimization.

