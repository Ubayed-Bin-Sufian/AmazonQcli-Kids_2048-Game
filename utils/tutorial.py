"""
Tutorial module for the Kids 2048 game.
"""
import pygame

class Tutorial:
    """Class to handle the game tutorial."""
    
    def __init__(self, game):
        """Initialize tutorial."""
        self.show = False
        self.current_slide = 0
        self.game = game
        self.slides = [
            {
                "title": "Welcome to Kids 2048!",
                "content": "A fun puzzle game where you combine numbers to reach 2048!",
                "image": None
            },
            {
                "title": "How to Play",
                "content": "Use arrow keys to move all tiles. When two tiles with the same number touch, they merge into one!",
                "image": None
            },
            {
                "title": "Game Objective",
                "content": "Try to create a tile with the number 2048 to win the game!",
                "image": None
            },
            {
                "title": "Game Over",
                "content": "The game ends when there are no more moves possible.",
                "image": None
            },
            {
                "title": "Ready to Play?",
                "content": "Press the X button or ESC key to close this tutorial and start playing!",
                "image": None
            }
        ]
        
        # Initialize button rects
        self.next_button_rect = pygame.Rect(0, 0, 0, 0)
        self.prev_button_rect = pygame.Rect(0, 0, 0, 0)
        self.close_button_rect = pygame.Rect(0, 0, 0, 0)
        
    def next_slide(self):
        """Go to the next slide."""
        if self.current_slide < len(self.slides) - 1:
            self.current_slide += 1
        else:
            self.show = False
    
    def prev_slide(self):
        """Go to the previous slide."""
        if self.current_slide > 0:
            self.current_slide -= 1
    
    def draw(self, screen):
        """Draw the tutorial slide."""
        from utils.constants import COLORS
        
        theme = "dark" if self.game.settings.dark_mode else "light"
        colors = COLORS[theme]
        
        # Draw tutorial panel
        panel_width = 500
        panel_height = 350
        panel_x = (self.game.screen_width - panel_width) // 2
        panel_y = (self.game.screen_height - panel_height) // 2
        
        pygame.draw.rect(
            screen,
            colors["grid_background"],
            (panel_x, panel_y, panel_width, panel_height),
            border_radius=10
        )
        
        # Draw slide content
        slide = self.slides[self.current_slide]
        
        # Draw title
        title_text = self.game.font.render(slide["title"], True, colors["text"])
        title_rect = title_text.get_rect(center=(panel_x + panel_width // 2, panel_y + 50))
        screen.blit(title_text, title_rect)
        
        # Draw content (wrap text)
        content_lines = self.wrap_text(slide["content"], panel_width - 60, self.game.small_font)
        for i, line in enumerate(content_lines):
            line_text = self.game.small_font.render(line, True, colors["text"])
            screen.blit(line_text, (panel_x + 30, panel_y + 100 + i * 30))
        
        # Draw navigation buttons
        button_width = 100
        button_height = 40
        button_y = panel_y + panel_height - 60
        
        # Previous button
        if self.current_slide > 0:
            prev_button_rect = pygame.Rect(panel_x + 30, button_y, button_width, button_height)
            pygame.draw.rect(
                screen,
                colors["button"],
                prev_button_rect,
                border_radius=5
            )
            prev_text = self.game.small_font.render("Previous", True, colors["button_text"])
            prev_text_rect = prev_text.get_rect(center=prev_button_rect.center)
            screen.blit(prev_text, prev_text_rect)
            self.prev_button_rect = prev_button_rect
        else:
            self.prev_button_rect = pygame.Rect(0, 0, 0, 0)
        
        # Next/Finish button
        next_button_rect = pygame.Rect(panel_x + panel_width - 30 - button_width, button_y, button_width, button_height)
        pygame.draw.rect(
            screen,
            colors["button"],
            next_button_rect,
            border_radius=5
        )
        
        if self.current_slide < len(self.slides) - 1:
            next_text = self.game.small_font.render("Next", True, colors["button_text"])
        else:
            next_text = self.game.small_font.render("Finish", True, colors["button_text"])
            
        next_text_rect = next_text.get_rect(center=next_button_rect.center)
        screen.blit(next_text, next_text_rect)
        self.next_button_rect = next_button_rect
        
        # Close button
        close_button_rect = pygame.Rect(panel_x + panel_width - 40, panel_y + 10, 30, 30)
        pygame.draw.rect(
            screen,
            colors["button"],
            close_button_rect,
            border_radius=15
        )
        
        # Draw X
        x_text = self.game.font.render("×", True, colors["button_text"])
        x_rect = x_text.get_rect(center=close_button_rect.center)
        screen.blit(x_text, x_rect)
        self.close_button_rect = close_button_rect
        
        # Draw slide indicator
        for i in range(len(self.slides)):
            indicator_x = panel_x + panel_width // 2 - (len(self.slides) * 15) // 2 + i * 15
            indicator_y = panel_y + panel_height - 25
            indicator_radius = 5
            
            if i == self.current_slide:
                pygame.draw.circle(screen, colors["text"], (indicator_x, indicator_y), indicator_radius)
            else:
                pygame.draw.circle(screen, colors["text"], (indicator_x, indicator_y), indicator_radius, 1)
    
    def wrap_text(self, text, max_width, font):
        """Wrap text to fit within a given width."""
        words = text.split(' ')
        lines = []
        current_line = []
        
        for word in words:
            test_line = ' '.join(current_line + [word])
            if font.size(test_line)[0] <= max_width:
                current_line.append(word)
            else:
                lines.append(' '.join(current_line))
                current_line = [word]
                
        if current_line:
            lines.append(' '.join(current_line))
            
        return lines
