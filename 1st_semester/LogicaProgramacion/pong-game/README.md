# PONG Game - Python Implementation

A fully-featured Pong game implementation in Python using Pygame.

Author: Requena Patricio

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
git clone https://github.com/rrequeena/beng-ai-projects/
cd 1st_semester/LogicaProgramacion/pong-game

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
```
