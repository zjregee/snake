"""
Snake Game Logic Module
Separated game logic from pygame rendering for unit testing
"""
import random
from enum import Enum
from typing import List, Tuple, Optional


class Direction(Enum):
    UP = (0, -1)
    DOWN = (0, 1)
    LEFT = (-1, 0)
    RIGHT = (1, 0)


class GameState(Enum):
    PLAYING = "playing"
    GAME_OVER = "game_over"


class SnakeGame:
    """Core Snake Game Logic"""
    
    def __init__(self, width: int = 600, height: int = 400, block_size: int = 10):
        self.width = width
        self.height = height
        self.block_size = block_size
        self.reset_game()
    
    def reset_game(self):
        """Reset the game to initial state"""
        self.snake_positions = [(self.width // 2, self.height // 2)]
        self.direction = Direction.RIGHT
        self.food_position = self._generate_food()
        self.state = GameState.PLAYING
        self.score = 0
    
    def _generate_food(self) -> Tuple[int, int]:
        """Generate food at a random position not occupied by snake"""
        while True:
            x = random.randrange(0, self.width // self.block_size) * self.block_size
            y = random.randrange(0, self.height // self.block_size) * self.block_size
            food_pos = (x, y)
            if food_pos not in self.snake_positions:
                return food_pos
    
    def change_direction(self, new_direction: Direction):
        """Change snake direction if valid (not opposite to current direction)"""
        if self.state != GameState.PLAYING:
            return
            
        # Prevent reversing into self
        current_dir = self.direction
        if (current_dir == Direction.UP and new_direction == Direction.DOWN or
            current_dir == Direction.DOWN and new_direction == Direction.UP or
            current_dir == Direction.LEFT and new_direction == Direction.RIGHT or
            current_dir == Direction.RIGHT and new_direction == Direction.LEFT):
            return
        
        self.direction = new_direction
    
    def update(self):
        """Update game state by one step"""
        if self.state != GameState.PLAYING:
            return
        
        # Calculate new head position
        head_x, head_y = self.snake_positions[0]
        dx, dy = self.direction.value
        new_head = (head_x + dx * self.block_size, head_y + dy * self.block_size)
        
        # Check wall collision
        if (new_head[0] < 0 or new_head[0] >= self.width or
            new_head[1] < 0 or new_head[1] >= self.height):
            self.state = GameState.GAME_OVER
            return
        
        # Check self collision
        if new_head in self.snake_positions:
            self.state = GameState.GAME_OVER
            return
        
        # Move snake
        self.snake_positions.insert(0, new_head)
        
        # Check food consumption
        if new_head == self.food_position:
            self.score += 1
            self.food_position = self._generate_food()
        else:
            # Remove tail if no food eaten
            self.snake_positions.pop()
    
    def get_snake_head(self) -> Tuple[int, int]:
        """Get current snake head position"""
        return self.snake_positions[0]
    
    def get_snake_body(self) -> List[Tuple[int, int]]:
        """Get all snake positions"""
        return self.snake_positions.copy()
    
    def get_food_position(self) -> Tuple[int, int]:
        """Get current food position"""
        return self.food_position
    
    def is_game_over(self) -> bool:
        """Check if game is over"""
        return self.state == GameState.GAME_OVER
    
    def get_score(self) -> int:
        """Get current score"""
        return self.score
    
    def get_snake_length(self) -> int:
        """Get current snake length"""
        return len(self.snake_positions)