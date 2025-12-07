"""
Main Game Manager - Orchestrates all systems
SOLID: Dependency Inversion - Depends on abstractions (systems)
"""

import pygame
from src.entities.ball import Ball
from src.entities.paddle import Paddle
from src.systems.physics import PhysicsSystem
from src.systems.collision import CollisionSystem
from src.systems.ai import AISystem
from src.systems.input_handler import InputHandler
from src.core.game_state import GameStateManager
from src.utils.constants import GameState, PLAYER_WINS, CPU_WINS, NO_WINNER
from src.ui import UIManager
from src import config


class PongGame:
    """
    Main game orchestrator

    Responsibilities:
    - Initialize game systems and entities
    - Coordinate system updates
    - Manage game flow and score
    - Render game state

    Architecture: All systems are loosely coupled through this manager
    """

    def __init__(self):
        """Initialize all game systems and entities"""
        pygame.init()

        self.screen = pygame.display.set_mode(
            (config.SCREEN_WIDTH, config.SCREEN_HEIGHT)
        )
        pygame.display.set_caption(config.TITLE)
        self.clock = pygame.time.Clock()

        # Initialize game entities
        self.player_paddle = Paddle(
            config.PADDLE_MARGIN,
            config.SCREEN_HEIGHT // 2 - config.PADDLE_HEIGHT // 2,
            is_left=True,
        )
        self.cpu_paddle = Paddle(
            config.SCREEN_WIDTH - config.PADDLE_MARGIN - config.PADDLE_WIDTH,
            config.SCREEN_HEIGHT // 2 - config.PADDLE_HEIGHT // 2,
            is_left=False,
        )
        self.ball = Ball(config.SCREEN_WIDTH // 2, config.SCREEN_HEIGHT // 2)

        # Initialize systems
        self.physics = PhysicsSystem(config.SCREEN_WIDTH, config.SCREEN_HEIGHT)
        self.ai = AISystem(config.AIDifficulty.MEDIUM)
        self.input_handler = InputHandler()
        self.state_manager = GameStateManager()

        # Initialize UI Manager
        self.ui_manager = UIManager(config.SCREEN_WIDTH, config.SCREEN_HEIGHT)

        # Game state
        self.player_score = 0
        self.cpu_score = 0
        self.running = True
        self.font_large = pygame.font.Font(None, config.FONT_LARGE)
        self.font_medium = pygame.font.Font(None, config.FONT_MEDIUM)
        self.font_small = pygame.font.Font(None, config.FONT_SMALL)

    def handle_input(self) -> None:
        """
        Process player input and update paddle

        System Integration: InputHandler → Paddle Movement
        """
        # Process all pygame events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
                return

            # Handle UI events based on current state
            self.ui_manager.handle_event(event, self.state_manager.current_state)

            # Handle keyboard events
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    if self.state_manager.current_state == GameState.IN_GAME:
                        self.state_manager.transition_to(GameState.PAUSED)
                    elif self.state_manager.current_state in [
                        GameState.PAUSED,
                        GameState.GAME_OVER,
                    ]:
                        self.state_manager.transition_to(GameState.MENU)
                        self.ui_manager.reset_menu()

                if event.key == pygame.K_SPACE:
                    if self.state_manager.current_state == GameState.IN_GAME:
                        self.state_manager.transition_to(GameState.PAUSED)
                    elif self.state_manager.current_state == GameState.PAUSED:
                        self.state_manager.transition_to(GameState.IN_GAME)
                    elif self.state_manager.current_state == GameState.PLAYER_SCORED:
                        # Continue game after player scored
                        self.state_manager.transition_to(GameState.IN_GAME)

        # Update UI and get actions
        ui_actions = self.ui_manager.update(self.state_manager.current_state)

        # Handle UI actions
        if ui_actions["start_game"]:
            win_points = ui_actions["win_points"]
            if win_points:
                self.state_manager.set_win_points(win_points)
            self.reset_game()

        if ui_actions["resume_game"]:
            self.state_manager.transition_to(GameState.IN_GAME)

        if ui_actions["quit_to_menu"]:
            self.state_manager.transition_to(GameState.MENU)
            self.ui_manager.reset_menu()

        if ui_actions["play_again"]:
            self.reset_game()

        if ui_actions["quit_game"]:
            self.running = False

        # Update player paddle movement (only during gameplay)
        if self.state_manager.is_in_game():
            keys = pygame.key.get_pressed()
            if keys[pygame.K_w]:
                self.player_paddle.move_up()
            elif keys[pygame.K_s]:
                self.player_paddle.move_down()
            else:
                self.player_paddle.stop()

    def update(self, dt: float) -> None:
        """
        Update game logic

        Update Order (important for correctness):
        1. Handle input (done separately now)
        2. Update physics
        3. Update AI
        4. Check collisions
        5. Update scores

        Args:
            dt: Delta time (seconds)
        """
        if not self.state_manager.is_in_game():
            return

        # Update entity positions (Physics System)
        entities = [self.player_paddle, self.cpu_paddle, self.ball]
        goal_scored = self.physics.update(entities, dt)

        # Update AI (AI System)
        self.ai.update(self.cpu_paddle, self.ball, dt)

        # Check collisions (Collision System)
        paddle_hit = CollisionSystem.check_multiple_paddles(
            self.ball, [self.player_paddle, self.cpu_paddle]
        )
        if paddle_hit:
            CollisionSystem.handle_paddle_collision(self.ball, paddle_hit)

        # Handle goal scoring
        if goal_scored:
            self._handle_goal()

    def _handle_goal(self) -> None:
        """
        Handle goal scoring logic

        Algorithm:
        1. Determine which side scored
        2. Increment score
        3. Reset ball
        4. Check win condition
        5. If player scored, pause and show message
        """
        # Determine which player scored based on ball position
        # Ball goes past left side (x < 0) = CPU scores (player missed)
        # Ball goes past right side (x > screen width) = Player scores (CPU missed)
        player_scored = False
        if self.ball.x < 0:
            # Ball went past left side -> CPU scores
            self.cpu_score += 1
        else:
            # Ball went past right side -> Player scores
            self.player_score += 1
            player_scored = True

        # Reset ball for next round
        self.ball.reset()

        # Check win condition
        winner = self._check_win_condition()
        if winner != NO_WINNER:
            player_won = winner == PLAYER_WINS
            self.ui_manager.set_game_over_result(
                self.player_score, self.cpu_score, player_won
            )
            self.state_manager.transition_to(GameState.GAME_OVER)
        elif player_scored:
            # Pause to celebrate player scoring
            self.state_manager.transition_to(GameState.PLAYER_SCORED)

    def _check_win_condition(self) -> int:
        """
        Check if anyone has won

        Returns:
            PLAYER_WINS, CPU_WINS, or NO_WINNER
        """
        win_points = self.state_manager.win_points

        if self.player_score >= win_points:
            return PLAYER_WINS
        elif self.cpu_score >= win_points:
            return CPU_WINS
        else:
            return NO_WINNER

    def draw(self) -> None:
        """
        Render game state to screen

        Rendering Order (back to front):
        1. Background
        2. Center line (only during gameplay)
        3. Game entities
        4. UI elements (scores, etc.)
        """
        # Clear screen
        self.screen.fill(config.COLOR_BLACK)

        # Draw center dashed line only during gameplay states
        if self.state_manager.current_state in [
            GameState.IN_GAME,
            GameState.PAUSED,
            GameState.PLAYER_SCORED,
        ]:
            self._draw_center_line()

        if self.state_manager.is_in_game():
            # Draw entities
            self.player_paddle.draw(self.screen)
            self.cpu_paddle.draw(self.screen)
            self.ball.draw(self.screen)

            # Draw scores
            self._draw_scores()

        elif self.state_manager.current_state == GameState.PLAYER_SCORED:
            # Draw game elements
            self.player_paddle.draw(self.screen)
            self.cpu_paddle.draw(self.screen)
            self.ball.draw(self.screen)
            self._draw_scores()

            # Draw "YOU SCORED" message
            self._draw_player_scored()

        elif self.state_manager.current_state == GameState.PAUSED:
            # Draw game elements in background
            self.player_paddle.draw(self.screen)
            self.cpu_paddle.draw(self.screen)
            self.ball.draw(self.screen)
            self._draw_scores()

            # Draw pause menu overlay
            self.ui_manager.draw(self.screen, self.state_manager.current_state)

        elif self.state_manager.current_state == GameState.MENU:
            # Draw menu using UI manager
            self.ui_manager.draw(self.screen, self.state_manager.current_state)

        elif self.state_manager.current_state == GameState.GAME_OVER:
            # Draw game over using UI manager
            self.ui_manager.draw(self.screen, self.state_manager.current_state)

        pygame.display.flip()

    def _draw_player_scored(self) -> None:
        """Draw 'YOU SCORED' celebration message"""
        # Semi-transparent overlay
        overlay = pygame.Surface((config.SCREEN_WIDTH, config.SCREEN_HEIGHT))
        overlay.fill(config.COLOR_BLACK)
        overlay.set_alpha(150)
        self.screen.blit(overlay, (0, 0))

        # "YOU SCORED" text
        scored_text = self.font_large.render("YOU SCORED!", True, config.COLOR_CYAN)
        scored_rect = scored_text.get_rect(
            center=(config.SCREEN_WIDTH // 2, config.SCREEN_HEIGHT // 2 - 30)
        )
        self.screen.blit(scored_text, scored_rect)

        # "Press SPACE to continue" text
        continue_text = self.font_small.render(
            "Press SPACE to continue", True, config.COLOR_WHITE
        )
        continue_rect = continue_text.get_rect(
            center=(config.SCREEN_WIDTH // 2, config.SCREEN_HEIGHT // 2 + 40)
        )
        self.screen.blit(continue_text, continue_rect)

    def _draw_center_line(self) -> None:
        """Draw center dashed line"""
        center_x = config.SCREEN_WIDTH // 2
        dash_height = config.CENTER_LINE_DASH

        y = 0
        while y < config.SCREEN_HEIGHT:
            pygame.draw.line(
                self.screen,
                config.COLOR_GRAY,
                (center_x, y),
                (center_x, y + dash_height),
                config.CENTER_LINE_WIDTH,
            )
            y += dash_height * 2

    def _draw_scores(self) -> None:
        """Draw current scores"""
        player_text = self.font_large.render(
            str(self.player_score), True, config.COLOR_WHITE
        )
        cpu_text = self.font_large.render(str(self.cpu_score), True, config.COLOR_WHITE)

        # Position scores with margins
        margin = 50
        self.screen.blit(player_text, (margin, 50))
        self.screen.blit(
            cpu_text, (config.SCREEN_WIDTH - margin - cpu_text.get_width(), 50)
        )

    def _draw_menu(self) -> None:
        """Draw main menu"""
        title = self.font_large.render("PONG", True, config.COLOR_CYAN)
        title_rect = title.get_rect(center=(config.SCREEN_WIDTH // 2, 100))
        self.screen.blit(title, title_rect)

        menu_text = self.font_medium.render(
            "Press SPACE to Start", True, config.COLOR_WHITE
        )
        menu_rect = menu_text.get_rect(
            center=(config.SCREEN_WIDTH // 2, config.SCREEN_HEIGHT // 2)
        )
        self.screen.blit(menu_text, menu_rect)

        instructions = self.font_small.render(
            "W/S to move | SPACE to pause | ESC for menu", True, config.COLOR_GRAY
        )
        instr_rect = instructions.get_rect(
            center=(config.SCREEN_WIDTH // 2, config.SCREEN_HEIGHT - 100)
        )
        self.screen.blit(instructions, instr_rect)

    def _draw_game_over(self) -> None:
        """Draw game over screen"""
        # Draw final scores
        self._draw_scores()

        # Determine winner
        if self.player_score >= self.state_manager.win_points:
            winner_text = self.font_large.render("YOU WIN!", True, config.COLOR_CYAN)
        else:
            winner_text = self.font_large.render("GAME OVER", True, config.COLOR_CYAN)

        winner_rect = winner_text.get_rect(
            center=(config.SCREEN_WIDTH // 2, config.SCREEN_HEIGHT // 2 - 50)
        )
        self.screen.blit(winner_text, winner_rect)

        restart_text = self.font_small.render(
            "Press SPACE to play again or ESC for menu", True, config.COLOR_WHITE
        )
        restart_rect = restart_text.get_rect(
            center=(config.SCREEN_WIDTH // 2, config.SCREEN_HEIGHT // 2 + 100)
        )
        self.screen.blit(restart_text, restart_rect)

    def reset_game(self) -> None:
        """Reset game to initial state"""
        self.player_score = 0
        self.cpu_score = 0
        self.ball.reset()
        # Reset paddle positions to center
        self.player_paddle.y = config.SCREEN_HEIGHT // 2 - config.PADDLE_HEIGHT // 2
        self.cpu_paddle.y = config.SCREEN_HEIGHT // 2 - config.PADDLE_HEIGHT // 2
        self.player_paddle.stop()
        self.cpu_paddle.stop()
        self.state_manager.transition_to(GameState.IN_GAME)

    def run(self) -> None:
        """
        Main game loop

        Fixed Timestep Implementation:
        - Target FPS: 60
        - Each frame: Input → Update → Render
        - Ensures deterministic physics
        """
        while self.running:
            dt = self.clock.tick(config.FPS) / 1000.0  # Convert to seconds

            # Game loop phases
            self.handle_input()  # Process input first
            self.update(dt)  # Update game state
            self.draw()  # Render frame

    def quit(self) -> None:
        """Clean shutdown"""
        pygame.quit()
