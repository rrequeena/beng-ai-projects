# PONG Game - Python Implementation

A fully-featured Pong game implementation in Python using Pygame, following SOLID principles and modern game architecture patterns.

## Features

✅ Single player vs CPU with 3 difficulty levels (Easy, Medium, Hard)  
✅ Customizable win points (1-50)  
✅ Advanced ball physics with spin calculation  
✅ Predictive AI algorithm for Hard difficulty  
✅ Fixed timestep 60 FPS game loop  
✅ Clean architecture with separated systems  
✅ Comprehensive collision detection  
✅ Visual feedback and UI  

## Architecture Overview

### Design Patterns
- **State Pattern**: Game state management (Menu, In-Game, Game-Over)
- **Strategy Pattern**: AI difficulty levels
- **MVC-like Architecture**: Entities (Model), Rendering (View), Systems (Controller)
- **Factory Pattern**: Entity creation

### SOLID Principles
- **Single Responsibility**: Each class has one reason to change
- **Open/Closed**: Open for extension, closed for modification
- **Liskov Substitution**: Entities are interchangeable
- **Interface Segregation**: Focused interfaces for each system
- **Dependency Inversion**: Depend on abstractions, not concrete implementations

### System Architecture
```
Game Manager (PongGame)
├── Physics System (movement calculations)
├── Collision System (collision detection/response)
├── AI System (CPU decision making)
├── Input Handler (keyboard input)
└── State Manager (game flow)
```

## How to Run

### Setup
```bash
# Clone repository
git clone <your-repo>
cd pong-game

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

### Run Game
```bash
python -m src.main
```

## Game Controls

| Key | Action |
|-----|--------|
| **W** | Move paddle up |
| **S** | Move paddle down |
| **SPACE** | Start game / Pause |
| **ESC** | Return to menu |

## Game Physics

### Ball Movement
- Constant velocity model
- Bounces off top/bottom walls
- Speed increases 5% on each paddle hit
- Maximum speed capped at 500 px/sec
- Angular velocity (spin) based on hit location

### Paddle Interaction
- Hit location determines ball spin
- Center hit = no vertical velocity
- Top hit = negative vertical velocity (ball curves up)
- Bottom hit = positive vertical velocity (ball curves down)

### AI Strategies

**Easy Mode**: Tracks ball center at 60% speed

**Medium Mode**: Tracks ball at 80% speed with ±20px random error

**Hard Mode**: Predicts ball trajectory and moves to intercept point at 95% speed

## Scoring

- First player to reach target points wins
- Configurable target (1-50 points)
- Ball resets after each point
- Score displayed in top corners

## Technical Specifications

- **Language**: Python 3.8+
- **Framework**: Pygame 2.5.2
- **Target FPS**: 60
- **Resolution**: 1280x720
- **Physics Model**: Fixed timestep, constant velocity

## File Structure

```
pong-game/
├── README.md
├── requirements.txt
├── .gitignore
├── docs/
│   ├── 01_flowcharts.md
│   ├── 02_architecture.md
│   └── 03_design_patterns.md
├── src/
│   ├── __init__.py
│   ├── main.py
│   ├── config.py
│   ├── core/
│   │   ├── __init__.py
│   │   ├── game.py
│   │   ├── game_state.py
│   │   └── game_loop.py
│   ├── entities/
│   │   ├── __init__.py
│   │   ├── paddle.py
│   │   ├── ball.py
│   │   └── entity.py
│   ├── systems/
│   │   ├── __init__.py
│   │   ├── physics.py
│   │   ├── collision.py
│   │   ├── ai.py
│   │   └── input_handler.py
│   ├── ui/
│   │   ├── __init__.py
│   │   ├── menu.py
│   │   ├── ui_manager.py
│   │   └── button.py
│   └── utils/
│       ├── __init__.py
│       └── constants.py
└── tests/
    ├── __init__.py
    ├── test_ball.py
    └── test_paddle.py
```

## Testing

```bash
# Run tests
pytest tests/

# Run with coverage
pytest --cov=src tests/
```

## Future Enhancements

- [ ] Sound effects and music
- [ ] Particle effects on collisions
- [ ] Power-ups
- [ ] Two-player multiplayer mode
- [ ] Different game modes
- [ ] Leaderboard system
- [ ] Settings menu with graphics options

## Performance Metrics

- **Fixed Timestep**: 60 FPS (16.67ms per frame)
- **Physics Update**: O(n) where n = entities
- **Collision Detection**: O(n) AABB checks
- **Rendering**: O(n) draw calls
- **AI Calculation**: O(1) per update

## License

MIT License
