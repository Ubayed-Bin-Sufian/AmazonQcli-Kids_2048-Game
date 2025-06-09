"""
Animation system for the 2048 game.
"""
import pygame

class Animation:
    def __init__(self, start_pos, end_pos, duration, value):
        """Initialize an animation."""
        self.start_pos = start_pos
        self.end_pos = end_pos
        self.duration = duration
        self.elapsed = 0
        self.value = value
        self.active = True
    
    def update(self, dt):
        """Update the animation."""
        if not self.active:
            return
        
        self.elapsed += dt
        if self.elapsed >= self.duration:
            self.active = False
    
    def get_current_pos(self):
        """Get the current position of the animated object."""
        if not self.active:
            return self.end_pos
        
        progress = min(self.elapsed / self.duration, 1.0)
        x = self.start_pos[0] + (self.end_pos[0] - self.start_pos[0]) * progress
        y = self.start_pos[1] + (self.end_pos[1] - self.start_pos[1]) * progress
        return (x, y)

class AnimationManager:
    def __init__(self):
        """Initialize the animation manager."""
        self.animations = []
    
    def add_move_animation(self, start_pos, end_pos, value, duration=200):
        """Add a new move animation."""
        self.animations.append(Animation(start_pos, end_pos, duration, value))
    
    def add_merge_animation(self, pos, value, duration=150):
        """Add a new merge animation."""
        # This could be expanded to include scaling or other effects
        pass
    
    def update(self, dt):
        """Update all animations."""
        for animation in self.animations:
            animation.update(dt)
        
        # Remove completed animations
        self.animations = [a for a in self.animations if a.active]
    
    def draw(self, screen, tile_size, font):
        """Draw all active animations."""
        for animation in self.animations:
            x, y = animation.get_current_pos()
            
            # Draw tile
            pygame.draw.rect(
                screen,
                (237, 224, 200),  # Default color for simplicity
                (x, y, tile_size, tile_size),
                border_radius=8
            )
            
            # Draw value
            text = font.render(str(animation.value), True, (119, 110, 101))
            text_rect = text.get_rect(center=(x + tile_size // 2, y + tile_size // 2))
            screen.blit(text, text_rect)
    
    def is_animating(self):
        """Check if any animations are currently active."""
        return len(self.animations) > 0
