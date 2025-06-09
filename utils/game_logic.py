"""
Game logic for the 2048 game.
"""
import random

class GameBoard:
    def __init__(self, size):
        """Initialize a new game board with the given size."""
        self.size = size
        self.grid = [[0 for _ in range(size)] for _ in range(size)]
        self.score_increment = 0
        
        # Add initial tiles
        self.add_random_tile()
        self.add_random_tile()
    
    def add_random_tile(self):
        """Add a random tile (2 or 4) to an empty cell."""
        empty_cells = []
        for row in range(self.size):
            for col in range(self.size):
                if self.grid[row][col] == 0:
                    empty_cells.append((row, col))
        
        if empty_cells:
            row, col = random.choice(empty_cells)
            self.grid[row][col] = 2 if random.random() < 0.9 else 4
            return True
        return False
    
    def contains_tile(self, value):
        """Check if the board contains a tile with the given value."""
        for row in range(self.size):
            for col in range(self.size):
                if self.grid[row][col] == value:
                    return True
        return False
    
    def moves_available(self):
        """Check if any moves are available."""
        # Check for empty cells
        for row in range(self.size):
            for col in range(self.size):
                if self.grid[row][col] == 0:
                    return True
        
        # Check for adjacent cells with the same value
        for row in range(self.size):
            for col in range(self.size):
                value = self.grid[row][col]
                
                # Check right
                if col < self.size - 1 and self.grid[row][col + 1] == value:
                    return True
                
                # Check down
                if row < self.size - 1 and self.grid[row + 1][col] == value:
                    return True
        
        return False
    
    def move_left(self):
        """Move all tiles to the left and merge if possible."""
        moved = False
        self.score_increment = 0
        
        for row in range(self.size):
            # Compact non-zero tiles to the left
            new_row = [tile for tile in self.grid[row] if tile != 0]
            new_row += [0] * (self.size - len(new_row))
            
            # Merge adjacent tiles with the same value
            for i in range(self.size - 1):
                if new_row[i] != 0 and new_row[i] == new_row[i + 1]:
                    new_row[i] *= 2
                    self.score_increment += new_row[i]
                    new_row[i + 1] = 0
            
            # Compact again after merging
            new_row = [tile for tile in new_row if tile != 0]
            new_row += [0] * (self.size - len(new_row))
            
            # Check if the row changed
            if new_row != self.grid[row]:
                moved = True
                self.grid[row] = new_row
        
        return moved
    
    def move_right(self):
        """Move all tiles to the right and merge if possible."""
        moved = False
        self.score_increment = 0
        
        for row in range(self.size):
            # Compact non-zero tiles to the right
            new_row = [tile for tile in self.grid[row] if tile != 0]
            new_row = [0] * (self.size - len(new_row)) + new_row
            
            # Merge adjacent tiles with the same value (from right to left)
            for i in range(self.size - 1, 0, -1):
                if new_row[i] != 0 and new_row[i] == new_row[i - 1]:
                    new_row[i] *= 2
                    self.score_increment += new_row[i]
                    new_row[i - 1] = 0
            
            # Compact again after merging
            new_row = [tile for tile in new_row if tile != 0]
            new_row = [0] * (self.size - len(new_row)) + new_row
            
            # Check if the row changed
            if new_row != self.grid[row]:
                moved = True
                self.grid[row] = new_row
        
        return moved
    
    def move_up(self):
        """Move all tiles up and merge if possible."""
        moved = False
        self.score_increment = 0
        
        for col in range(self.size):
            # Extract column
            column = [self.grid[row][col] for row in range(self.size)]
            
            # Compact non-zero tiles to the top
            new_column = [tile for tile in column if tile != 0]
            new_column += [0] * (self.size - len(new_column))
            
            # Merge adjacent tiles with the same value
            for i in range(self.size - 1):
                if new_column[i] != 0 and new_column[i] == new_column[i + 1]:
                    new_column[i] *= 2
                    self.score_increment += new_column[i]
                    new_column[i + 1] = 0
            
            # Compact again after merging
            new_column = [tile for tile in new_column if tile != 0]
            new_column += [0] * (self.size - len(new_column))
            
            # Check if the column changed
            if new_column != column:
                moved = True
                for row in range(self.size):
                    self.grid[row][col] = new_column[row]
        
        return moved
    
    def move_down(self):
        """Move all tiles down and merge if possible."""
        moved = False
        self.score_increment = 0
        
        for col in range(self.size):
            # Extract column
            column = [self.grid[row][col] for row in range(self.size)]
            
            # Compact non-zero tiles to the bottom
            new_column = [tile for tile in column if tile != 0]
            new_column = [0] * (self.size - len(new_column)) + new_column
            
            # Merge adjacent tiles with the same value (from bottom to top)
            for i in range(self.size - 1, 0, -1):
                if new_column[i] != 0 and new_column[i] == new_column[i - 1]:
                    new_column[i] *= 2
                    self.score_increment += new_column[i]
                    new_column[i - 1] = 0
            
            # Compact again after merging
            new_column = [tile for tile in new_column if tile != 0]
            new_column = [0] * (self.size - len(new_column)) + new_column
            
            # Check if the column changed
            if new_column != column:
                moved = True
                for row in range(self.size):
                    self.grid[row][col] = new_column[row]
        
        return moved
