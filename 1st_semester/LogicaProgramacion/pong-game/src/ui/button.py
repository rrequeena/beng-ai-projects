"""
Button UI Component
SOLID: Single Responsibility - Button rendering and interaction only
"""
import pygame
from src import config


class Button:
    """
    Interactive button component for menus
    
    Features:
    - Hover effect (color change)
    - Click detection
    - Customizable text and colors
    """
    
    def __init__(self, x: int, y: int, width: int, height: int, text: str,
                 font_size: int = config.FONT_MEDIUM,
                 color: tuple = config.COLOR_WHITE,
                 hover_color: tuple = config.COLOR_CYAN,
                 text_color: tuple = config.COLOR_BLACK):
        """
        Initialize button
        
        Args:
            x: Center x position
            y: Center y position
            width: Button width
            height: Button height
            text: Button label
            font_size: Font size for text
            color: Normal background color
            hover_color: Background color when hovered
            text_color: Color of the text
        """
        self.rect = pygame.Rect(0, 0, width, height)
        self.rect.center = (x, y)
        
        self.text = text
        self.font = pygame.font.Font(None, font_size)
        self.color = color
        self.hover_color = hover_color
        self.text_color = text_color
        
        self.is_hovered = False
        self.is_clicked = False
    
    def update(self, mouse_pos: tuple, mouse_clicked: bool) -> bool:
        """
        Update button state based on mouse
        
        Args:
            mouse_pos: Current mouse position (x, y)
            mouse_clicked: Whether mouse was clicked this frame
            
        Returns:
            bool: True if button was clicked
        """
        self.is_hovered = self.rect.collidepoint(mouse_pos)
        self.is_clicked = self.is_hovered and mouse_clicked
        return self.is_clicked
    
    def draw(self, screen: pygame.Surface) -> None:
        """
        Render button to screen
        
        Args:
            screen: Pygame surface to draw on
        """
        # Choose color based on hover state
        current_color = self.hover_color if self.is_hovered else self.color
        
        # Draw button background
        pygame.draw.rect(screen, current_color, self.rect)
        
        # Draw border
        border_color = config.COLOR_WHITE if self.is_hovered else config.COLOR_GRAY
        pygame.draw.rect(screen, border_color, self.rect, 3)
        
        # Draw text centered on button
        text_surface = self.font.render(self.text, True, self.text_color)
        text_rect = text_surface.get_rect(center=self.rect.center)
        screen.blit(text_surface, text_rect)


class InputBox:
    """
    Text input box for numeric values (win points)
    
    Features:
    - Click to activate
    - Numeric input only
    - Min/max value constraints
    """
    
    def __init__(self, x: int, y: int, width: int, height: int, 
                 initial_value: int = 10,
                 min_value: int = 1,
                 max_value: int = 50,
                 label: str = ""):
        """
        Initialize input box
        
        Args:
            x: Center x position
            y: Center y position
            width: Box width
            height: Box height
            initial_value: Starting value
            min_value: Minimum allowed value
            max_value: Maximum allowed value
            label: Label text to display above the box
        """
        self.rect = pygame.Rect(0, 0, width, height)
        self.rect.center = (x, y)
        
        self.value = initial_value
        self.min_value = min_value
        self.max_value = max_value
        self.label = label
        
        self.font = pygame.font.Font(None, config.FONT_MEDIUM)
        self.label_font = pygame.font.Font(None, config.FONT_SMALL)
        
        self.is_active = False
        self.text = str(initial_value)
    
    def update(self, mouse_pos: tuple, mouse_clicked: bool, event: pygame.event.Event = None) -> None:
        """
        Update input box state
        
        Args:
            mouse_pos: Current mouse position
            mouse_clicked: Whether mouse was clicked
            event: Pygame event for keyboard input
        """
        # Check if clicked on box
        if mouse_clicked:
            self.is_active = self.rect.collidepoint(mouse_pos)
        
        # Handle keyboard input when active
        if event and self.is_active:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_BACKSPACE:
                    self.text = self.text[:-1]
                elif event.key == pygame.K_RETURN:
                    self.is_active = False
                    self._validate_value()
                elif event.unicode.isdigit() and len(self.text) < 3:
                    self.text += event.unicode
    
    def _validate_value(self) -> None:
        """Validate and clamp the input value"""
        if self.text:
            self.value = int(self.text)
            self.value = max(self.min_value, min(self.max_value, self.value))
            self.text = str(self.value)
        else:
            self.text = str(self.min_value)
            self.value = self.min_value
    
    def get_value(self) -> int:
        """Get current numeric value"""
        self._validate_value()
        return self.value
    
    def draw(self, screen: pygame.Surface) -> None:
        """
        Render input box to screen
        
        Args:
            screen: Pygame surface to draw on
        """
        # Draw label
        if self.label:
            label_surface = self.label_font.render(self.label, True, config.COLOR_WHITE)
            label_rect = label_surface.get_rect(center=(self.rect.centerx, self.rect.top - 25))
            screen.blit(label_surface, label_rect)
        
        # Draw box background
        bg_color = config.COLOR_GRAY if self.is_active else config.COLOR_BLACK
        pygame.draw.rect(screen, bg_color, self.rect)
        
        # Draw border
        border_color = config.COLOR_CYAN if self.is_active else config.COLOR_WHITE
        pygame.draw.rect(screen, border_color, self.rect, 3)
        
        # Draw value text
        display_text = self.text if self.text else "0"
        text_surface = self.font.render(display_text, True, config.COLOR_WHITE)
        text_rect = text_surface.get_rect(center=self.rect.center)
        screen.blit(text_surface, text_rect)
        
        # Draw cursor when active
        if self.is_active:
            cursor_x = text_rect.right + 2
            pygame.draw.line(screen, config.COLOR_WHITE, 
                           (cursor_x, self.rect.centery - 15),
                           (cursor_x, self.rect.centery + 15), 2)
