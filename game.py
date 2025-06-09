#!/usr/bin/env python3
"""
Kids 2048 Game - A colorful, kid-friendly version of the classic 2048 game.
"""
import os
import pygame
import sys
import random
import json
from utils.constants import COLORS
from utils.settings import Settings
from utils.tutorial import Tutorial


class Game:
    """Main game class that handles the game logic and rendering."""
    
    def __init__(self):
        """Initialize the game."""
        # Initialize pygame
        pygame.init()
        
        # Set up default attributes
        self.screen_width = 800
        self.screen_height = 600
        self.show_settings = False
        
        # Create screen
        self.screen = pygame.display.set_mode((self.screen_width, self.screen_height))
        pygame.display.set_caption("Kids 2048")
        
        # Initialize settings
        self.settings = Settings()
        
        # Initialize tutorial
        self.tutorial = Tutorial(self)
        
        # Game board setup
        self.grid_size = 4
        self.cell_size = 100
        self.grid_padding = 15
        self.board_width = self.grid_size * self.cell_size + (self.grid_size + 1) * self.grid_padding
        self.board_height = self.board_width
        self.board_x = (self.screen_width - self.board_width) // 2
        
        # Increase the vertical position of the board to create more space above
        self.board_y = (self.screen_height - self.board_height) // 2 + 140
        
        # Score tracking
        self.score = 0
        self.highest_score = self.load_highest_score()
        
        # Initialize the game grid
        self.grid = [[0 for _ in range(self.grid_size)] for _ in range(self.grid_size)]
        
        # Add initial tiles
        self.add_random_tile()
        self.add_random_tile()
        
        # Load font
        self.load_fonts()
            
        # Load or create settings icon
        self.load_settings_icon()
            
        # Button areas - Repositioned as requested
        self.restart_button_width = 150
        self.restart_button_height = 50
        self.restart_button_rect = pygame.Rect(
            self.board_x + (self.board_width - self.restart_button_width) // 2,  # Center horizontally
            self.board_y + self.board_height + 20,  # Directly below the tiles with less spacing
            self.restart_button_width, 
            self.restart_button_height
        )
        
        # Settings button in top right corner
        self.settings_button_rect = pygame.Rect(
            self.board_x + self.board_width - 50, 
            self.board_y - 60, 
            40, 
            40
        )
        
        # Always show tutorial at startup
        self.tutorial.show = True
    
    def load_fonts(self):
        """Load game fonts."""
        try:
            self.font = pygame.font.Font(os.path.join("assets", "fonts", "fredoka.ttf"), 36)
            self.small_font = pygame.font.Font(os.path.join("assets", "fonts", "fredoka.ttf"), 24)
            self.large_font = pygame.font.Font(os.path.join("assets", "fonts", "fredoka.ttf"), 48)
        except (FileNotFoundError, pygame.error):
            print("Font not found, using system font")
            self.font = pygame.font.SysFont(None, 36)
            self.small_font = pygame.font.SysFont(None, 24)
            self.large_font = pygame.font.SysFont(None, 48)
    
    def load_settings_icon(self):
        """Load or create settings icon."""
        try:
            self.settings_icon = pygame.image.load(os.path.join("assets", "images", "settings.png"))
            self.settings_icon = pygame.transform.scale(self.settings_icon, (40, 40))
        except (FileNotFoundError, pygame.error):
            # Create a simple gear icon if image not found
            self.settings_icon = self.create_settings_icon()
    
    def create_settings_icon(self):
        """Create a simple gear icon surface."""
        import math
        icon = pygame.Surface((40, 40), pygame.SRCALPHA)
        pygame.draw.circle(icon, (100, 100, 100), (20, 20), 15, 2)
        for i in range(8):
            angle = i * 45
            x = 20 + 18 * math.cos(math.radians(angle))
            y = 20 + 18 * math.sin(math.radians(angle))
            pygame.draw.circle(icon, (100, 100, 100), (int(x), int(y)), 4)
        return icon
    
    def check_first_run(self):
        """Check if this is the first time running the game - always return True to show tutorial."""
        return True
    
    def save_game_data(self):
        """Save game data to file."""
        data = {
            "highest_score": self.highest_score,
            "first_run": False
        }
        with open("game_data.json", "w") as f:
            json.dump(data, f)
    
    def load_highest_score(self):
        """Load highest score from file."""
        try:
            with open("game_data.json", "r") as f:
                data = json.load(f)
                return data.get("highest_score", 0)
        except (FileNotFoundError, json.JSONDecodeError):
            return 0
    
    def add_random_tile(self):
        """Add a random tile (2 or 4) to an empty cell."""
        empty_cells = [(i, j) for i in range(self.grid_size) for j in range(self.grid_size) if self.grid[i][j] == 0]
        if empty_cells:
            i, j = random.choice(empty_cells)
            self.grid[i][j] = 2 if random.random() < 0.9 else 4
    
    def draw_board(self):
        """Draw the game board with tiles."""
        theme = "dark" if self.settings.dark_mode else "light"
        colors = COLORS[theme]
        
        # Draw the board background
        pygame.draw.rect(
            self.screen, 
            colors["grid_background"],
            (self.board_x, self.board_y, self.board_width, self.board_height),
            border_radius=10
        )
        
        # Draw cells and tiles
        for i in range(self.grid_size):
            for j in range(self.grid_size):
                cell_x = self.board_x + self.grid_padding * (j + 1) + self.cell_size * j
                cell_y = self.board_y + self.grid_padding * (i + 1) + self.cell_size * i
                
                # Draw empty cell
                pygame.draw.rect(
                    self.screen,
                    colors["empty_cell"],
                    (cell_x, cell_y, self.cell_size, self.cell_size),
                    border_radius=5
                )
                
                # Draw tile if not empty
                if self.grid[i][j] != 0:
                    value = self.grid[i][j]
                    
                    # Determine tile color
                    if value <= 2048:
                        tile_color = colors[f"tile_{value}"]
                    else:
                        tile_color = colors["tile_super"]
                    
                    # Draw tile
                    pygame.draw.rect(
                        self.screen,
                        tile_color,
                        (cell_x, cell_y, self.cell_size, self.cell_size),
                        border_radius=5
                    )
                    
                    # Draw value text
                    text_color = colors["text"] if value < 8 else colors["button_text"]
                    font_size = self.font if value < 1000 else self.small_font
                    text_surface = font_size.render(str(value), True, text_color)
                    text_rect = text_surface.get_rect(center=(cell_x + self.cell_size // 2, cell_y + self.cell_size // 2))
                    self.screen.blit(text_surface, text_rect)
    
    def draw_ui(self):
        """Draw UI elements like score and buttons."""
        theme = "dark" if self.settings.dark_mode else "light"
        colors = COLORS[theme]
        
        # Draw game title - moved higher for better positioning
        title_text = self.large_font.render("Kids 2048", True, colors["text"])
        title_rect = title_text.get_rect(center=(self.board_x + self.board_width // 2, self.board_y - 150))
        self.screen.blit(title_text, title_rect)
        
        # Draw score boxes - Moved below the heading with increased spacing from tiles
        score_box_width = 150
        score_box_height = 70
        score_box_padding = 20
        
        # Current score box - positioned below the heading on the left with more space from tiles
        score_box_x = self.board_x
        score_box_y = self.board_y - 80  # Maintained spacing between score and tiles
        
        pygame.draw.rect(
            self.screen,
            colors["grid_background"],
            (score_box_x, score_box_y, score_box_width, score_box_height),
            border_radius=5
        )
        score_label = self.small_font.render("SCORE", True, colors["text"])
        score_value = self.font.render(str(self.score), True, colors["text"])
        score_label_rect = score_label.get_rect(center=(score_box_x + score_box_width // 2, score_box_y + 20))
        score_value_rect = score_value.get_rect(center=(score_box_x + score_box_width // 2, score_box_y + 45))
        self.screen.blit(score_label, score_label_rect)
        self.screen.blit(score_value, score_value_rect)
        
        # Highest score box - positioned below the heading on the right with more space from tiles
        best_box_x = self.board_x + self.board_width - score_box_width
        best_box_y = self.board_y - 80  # Maintained spacing between score and tiles
        
        pygame.draw.rect(
            self.screen,
            colors["grid_background"],
            (best_box_x, best_box_y, score_box_width, score_box_height),
            border_radius=5
        )
        highest_label = self.small_font.render("BEST", True, colors["text"])
        highest_value = self.font.render(str(self.highest_score), True, colors["text"])
        highest_label_rect = highest_label.get_rect(center=(best_box_x + score_box_width // 2, best_box_y + 20))
        highest_value_rect = highest_value.get_rect(center=(best_box_x + score_box_width // 2, best_box_y + 45))
        self.screen.blit(highest_label, highest_label_rect)
        self.screen.blit(highest_value, highest_value_rect)
        
        # Draw restart button - now below the board and centered
        pygame.draw.rect(
            self.screen,
            colors["button"],
            self.restart_button_rect,
            border_radius=5
        )
        restart_text = self.font.render("Restart", True, colors["button_text"])
        restart_text_rect = restart_text.get_rect(center=self.restart_button_rect.center)
        self.screen.blit(restart_text, restart_text_rect)
    
    def draw_settings(self):
        """Draw settings menu."""
        theme = "dark" if self.settings.dark_mode else "light"
        colors = COLORS[theme]
        
        # Draw settings panel (no overlay) - positioned slightly lower on screen
        panel_width = 300
        panel_height = 200
        panel_x = (self.screen_width - panel_width) // 2
        panel_y = (self.screen_height - panel_height) // 2 + 30  # Moved 30 pixels lower
        
        pygame.draw.rect(
            self.screen,
            colors["grid_background"],
            (panel_x, panel_y, panel_width, panel_height),
            border_radius=10
        )
        
        # Draw settings title
        settings_text = self.font.render("Settings", True, colors["text"])
        settings_rect = settings_text.get_rect(center=(panel_x + panel_width // 2, panel_y + 30))
        self.screen.blit(settings_text, settings_rect)
        
        # Draw theme toggle switch
        toggle_width = 60
        toggle_height = 30
        toggle_x = panel_x + panel_width // 2 - toggle_width // 2 + 30  # Moved right to make space for label
        toggle_y = panel_y + 90
        
        # Draw toggle background
        toggle_bg_color = colors["button"] if self.settings.dark_mode else colors["empty_cell"]
        pygame.draw.rect(
            self.screen,
            toggle_bg_color,
            (toggle_x, toggle_y, toggle_width, toggle_height),
            border_radius=15
        )
        
        # Draw toggle knob
        knob_size = toggle_height - 6
        knob_x = toggle_x + toggle_width - knob_size - 3 if self.settings.dark_mode else toggle_x + 3
        knob_y = toggle_y + 3
        pygame.draw.circle(
            self.screen,
            colors["button_text"],
            (knob_x + knob_size // 2, knob_y + knob_size // 2),
            knob_size // 2
        )
        
        # Draw theme labels with more padding
        theme_label = self.font.render("Theme:", True, colors["text"])
        theme_label_rect = theme_label.get_rect(midright=(toggle_x - 15, toggle_y + toggle_height // 2))
        self.screen.blit(theme_label, theme_label_rect)
        
        mode_text = "Dark" if self.settings.dark_mode else "Light"
        mode_label = self.small_font.render(mode_text, True, colors["text"])
        mode_label_rect = mode_label.get_rect(midleft=(toggle_x + toggle_width + 10, toggle_y + toggle_height // 2))
        self.screen.blit(mode_label, mode_label_rect)
        
        # Draw close button
        close_button_rect = pygame.Rect(panel_x + panel_width - 40, panel_y + 10, 30, 30)
        pygame.draw.rect(
            self.screen,
            colors["button"],
            close_button_rect,
            border_radius=15
        )
        
        # Draw X
        x_text = self.font.render("×", True, colors["button_text"])
        x_rect = x_text.get_rect(center=close_button_rect.center)
        self.screen.blit(x_text, x_rect)
        
        # Store button rects for click handling
        self.theme_button_rect = pygame.Rect(toggle_x, toggle_y, toggle_width, toggle_height)
        self.close_button_rect = close_button_rect
    
    def handle_input(self):
        """Handle user input events."""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.save_game_data()
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    if self.tutorial.show:
                        self.tutorial.show = False
                    else:
                        self.show_settings = not self.show_settings
                
                if not self.show_settings and not self.tutorial.show:
                    # Game controls
                    if event.key == pygame.K_UP:
                        self.move_tiles("up")
                    elif event.key == pygame.K_DOWN:
                        self.move_tiles("down")
                    elif event.key == pygame.K_LEFT:
                        self.move_tiles("left")
                    elif event.key == pygame.K_RIGHT:
                        self.move_tiles("right")
                elif self.tutorial.show:
                    if event.key == pygame.K_RIGHT:
                        self.tutorial.next_slide()
                    elif event.key == pygame.K_LEFT:
                        self.tutorial.prev_slide()
            
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                
                # Handle tutorial clicks
                if self.tutorial.show:
                    if self.tutorial.next_button_rect.collidepoint(mouse_pos):
                        self.tutorial.next_slide()
                    elif self.tutorial.prev_button_rect.collidepoint(mouse_pos):
                        self.tutorial.prev_slide()
                    elif self.tutorial.close_button_rect.collidepoint(mouse_pos):
                        self.tutorial.show = False
                # Handle settings clicks
                elif self.show_settings:
                    if self.theme_button_rect.collidepoint(mouse_pos):
                        self.settings.dark_mode = not self.settings.dark_mode
                    elif self.close_button_rect.collidepoint(mouse_pos):
                        self.show_settings = False
                # Handle main UI clicks
                else:
                    if self.restart_button_rect.collidepoint(mouse_pos):
                        self.restart_game()
                    elif self.settings_button_rect.collidepoint(mouse_pos):
                        self.show_settings = True
    
    def restart_game(self):
        """Reset the game to initial state."""
        self.grid = [[0 for _ in range(self.grid_size)] for _ in range(self.grid_size)]
        self.score = 0
        self.add_random_tile()
        self.add_random_tile()
    
    def move_tiles(self, direction):
        """Move tiles in the specified direction and merge if possible."""
        moved = False
        
        # Create a copy of the grid for comparison
        old_grid = [row[:] for row in self.grid]
        
        if direction == "up":
            moved = self._move_up()
        elif direction == "down":
            moved = self._move_down()
        elif direction == "left":
            moved = self._move_left()
        elif direction == "right":
            moved = self._move_right()
        
        # Check if the grid changed
        if moved:
            self.add_random_tile()
            
            # Update highest score
            if self.score > self.highest_score:
                self.highest_score = self.score
        
        return moved
    
    def _move_up(self):
        """Move tiles up and merge if possible."""
        moved = False
        old_grid = [row[:] for row in self.grid]
        
        for j in range(self.grid_size):
            # Compact column (move all tiles up)
            for i in range(1, self.grid_size):
                if self.grid[i][j] != 0:
                    k = i
                    while k > 0 and self.grid[k-1][j] == 0:
                        self.grid[k-1][j] = self.grid[k][j]
                        self.grid[k][j] = 0
                        k -= 1
            
            # Merge tiles
            for i in range(self.grid_size - 1):
                if self.grid[i][j] != 0 and self.grid[i][j] == self.grid[i+1][j]:
                    self.grid[i][j] *= 2
                    self.score += self.grid[i][j]
                    self.grid[i+1][j] = 0
            
            # Compact again after merging
            for i in range(1, self.grid_size):
                if self.grid[i][j] != 0:
                    k = i
                    while k > 0 and self.grid[k-1][j] == 0:
                        self.grid[k-1][j] = self.grid[k][j]
                        self.grid[k][j] = 0
                        k -= 1
        
        # Check if the grid changed
        return self.grid != old_grid
    
    def _move_down(self):
        """Move tiles down and merge if possible."""
        moved = False
        old_grid = [row[:] for row in self.grid]
        
        for j in range(self.grid_size):
            # Compact column (move all tiles down)
            for i in range(self.grid_size - 2, -1, -1):
                if self.grid[i][j] != 0:
                    k = i
                    while k < self.grid_size - 1 and self.grid[k+1][j] == 0:
                        self.grid[k+1][j] = self.grid[k][j]
                        self.grid[k][j] = 0
                        k += 1
            
            # Merge tiles
            for i in range(self.grid_size - 1, 0, -1):
                if self.grid[i][j] != 0 and self.grid[i][j] == self.grid[i-1][j]:
                    self.grid[i][j] *= 2
                    self.score += self.grid[i][j]
                    self.grid[i-1][j] = 0
            
            # Compact again after merging
            for i in range(self.grid_size - 2, -1, -1):
                if self.grid[i][j] != 0:
                    k = i
                    while k < self.grid_size - 1 and self.grid[k+1][j] == 0:
                        self.grid[k+1][j] = self.grid[k][j]
                        self.grid[k][j] = 0
                        k += 1
        
        # Check if the grid changed
        return self.grid != old_grid
    
    def _move_left(self):
        """Move tiles left and merge if possible."""
        moved = False
        old_grid = [row[:] for row in self.grid]
        
        for i in range(self.grid_size):
            # Compact row (move all tiles left)
            for j in range(1, self.grid_size):
                if self.grid[i][j] != 0:
                    k = j
                    while k > 0 and self.grid[i][k-1] == 0:
                        self.grid[i][k-1] = self.grid[i][k]
                        self.grid[i][k] = 0
                        k -= 1
            
            # Merge tiles
            for j in range(self.grid_size - 1):
                if self.grid[i][j] != 0 and self.grid[i][j] == self.grid[i][j+1]:
                    self.grid[i][j] *= 2
                    self.score += self.grid[i][j]
                    self.grid[i][j+1] = 0
            
            # Compact again after merging
            for j in range(1, self.grid_size):
                if self.grid[i][j] != 0:
                    k = j
                    while k > 0 and self.grid[i][k-1] == 0:
                        self.grid[i][k-1] = self.grid[i][k]
                        self.grid[i][k] = 0
                        k -= 1
        
        # Check if the grid changed
        return self.grid != old_grid
    
    def _move_right(self):
        """Move tiles right and merge if possible."""
        moved = False
        old_grid = [row[:] for row in self.grid]
        
        for i in range(self.grid_size):
            # Compact row (move all tiles right)
            for j in range(self.grid_size - 2, -1, -1):
                if self.grid[i][j] != 0:
                    k = j
                    while k < self.grid_size - 1 and self.grid[i][k+1] == 0:
                        self.grid[i][k+1] = self.grid[i][k]
                        self.grid[i][k] = 0
                        k += 1
            
            # Merge tiles
            for j in range(self.grid_size - 1, 0, -1):
                if self.grid[i][j] != 0 and self.grid[i][j] == self.grid[i][j-1]:
                    self.grid[i][j] *= 2
                    self.score += self.grid[i][j]
                    self.grid[i][j-1] = 0
            
            # Compact again after merging
            for j in range(self.grid_size - 2, -1, -1):
                if self.grid[i][j] != 0:
                    k = j
                    while k < self.grid_size - 1 and self.grid[i][k+1] == 0:
                        self.grid[i][k+1] = self.grid[i][k]
                        self.grid[i][k] = 0
                        k += 1
        
        # Check if the grid changed
        return self.grid != old_grid
    
    def run(self):
        """Main game loop."""
        clock = pygame.time.Clock()
        
        while True:
            # Handle input
            self.handle_input()
            
            # Draw everything
            theme = "dark" if self.settings.dark_mode else "light"
            self.screen.fill(COLORS[theme]["background"])
            
            # Draw settings icon aligned with the "KIDS 2048" heading
            settings_icon_rect = pygame.Rect(
                self.board_x + self.board_width - 50,  # Aligned with right edge of tile grid
                self.board_y - 150,  # Exactly aligned with "KIDS 2048" heading
                40, 
                40
            )
            self.settings_button_rect = settings_icon_rect
            
            pygame.draw.rect(
                self.screen,
                COLORS[theme]["button"],
                self.settings_button_rect,
                border_radius=5
            )
            self.screen.blit(self.settings_icon, self.settings_button_rect.topleft)
            
            self.draw_board()
            self.draw_ui()
            
            if self.show_settings:
                self.draw_settings()
                
            if self.tutorial.show:
                self.tutorial.draw(self.screen)
            
            # Update display
            pygame.display.flip()
            clock.tick(60)
