"""
Game Entry Point
"""
from src.core.game import PongGame

def main():
    """Initialize and run the game"""
    game = PongGame()
    try:
        game.run()
    except KeyboardInterrupt:
        print("Game interrupted by user")
    finally:
        game.quit()

if __name__ == "__main__":
    main()
