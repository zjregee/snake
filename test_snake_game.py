"""
Unit Tests for Snake Game Logic
"""
import unittest
import random
from snake_game import SnakeGame, Direction, GameState


class TestSnakeGame(unittest.TestCase):
    
    def setUp(self):
        """Set up test fixtures before each test method"""
        self.game = SnakeGame(width=200, height=200, block_size=10)
        # Set random seed for reproducible tests
        random.seed(42)
    
    def test_initial_game_state(self):
        """Test initial game state is correct"""
        self.assertEqual(self.game.state, GameState.PLAYING)
        self.assertEqual(self.game.score, 0)
        self.assertEqual(self.game.get_snake_length(), 1)
        self.assertEqual(self.game.direction, Direction.RIGHT)
        
        # Snake should start at center
        expected_center = (100, 100)
        self.assertEqual(self.game.get_snake_head(), expected_center)
    
    def test_snake_movement(self):
        """Test snake moves correctly in each direction"""
        # Test moving right (default)
        initial_head = self.game.get_snake_head()
        self.game.update()
        new_head = self.game.get_snake_head()
        self.assertEqual(new_head, (initial_head[0] + 10, initial_head[1]))
        
        # Test moving down
        self.game.change_direction(Direction.DOWN)
        self.game.update()
        head_after_down = self.game.get_snake_head()
        self.assertEqual(head_after_down, (new_head[0], new_head[1] + 10))
        
        # Test moving left
        self.game.change_direction(Direction.LEFT)
        self.game.update()
        head_after_left = self.game.get_snake_head()
        self.assertEqual(head_after_left, (head_after_down[0] - 10, head_after_down[1]))
        
        # Test moving up
        self.game.change_direction(Direction.UP)
        self.game.update()
        head_after_up = self.game.get_snake_head()
        self.assertEqual(head_after_up, (head_after_left[0], head_after_left[1] - 10))
    
    def test_direction_change_prevention(self):
        """Test that snake cannot reverse direction into itself"""
        # Initially moving right
        self.assertEqual(self.game.direction, Direction.RIGHT)
        
        # Try to reverse to left - should be ignored
        self.game.change_direction(Direction.LEFT)
        self.assertEqual(self.game.direction, Direction.RIGHT)
        
        # Change to down - should work
        self.game.change_direction(Direction.DOWN)
        self.assertEqual(self.game.direction, Direction.DOWN)
        
        # Try to reverse to up - should be ignored
        self.game.change_direction(Direction.UP)
        self.assertEqual(self.game.direction, Direction.DOWN)
    
    def test_wall_collision(self):
        """Test collision detection with walls"""
        # Test left wall - snake at x=0 moving left
        self.game.snake_positions = [(0, 100)]
        self.game.direction = Direction.LEFT
        self.game.update()
        self.assertTrue(self.game.is_game_over())
        
        # Reset and test right wall - snake at x=190 moving right
        self.game.reset_game()
        self.game.snake_positions = [(190, 100)]
        self.game.direction = Direction.RIGHT
        self.game.update()
        self.assertTrue(self.game.is_game_over())
        
        # Reset and test top wall - snake at y=0 moving up
        self.game.reset_game()
        self.game.snake_positions = [(100, 0)]
        self.game.direction = Direction.UP
        self.game.update()
        self.assertTrue(self.game.is_game_over())
        
        # Reset and test bottom wall - snake at y=190 moving down
        self.game.reset_game()
        self.game.snake_positions = [(100, 190)]
        self.game.direction = Direction.DOWN
        self.game.update()
        self.assertTrue(self.game.is_game_over())
    
    def test_self_collision(self):
        """Test collision detection when snake hits itself"""
        # Create a snake that will collide with itself
        self.game.snake_positions = [(100, 100), (90, 100), (80, 100), (80, 110)]
        self.game.direction = Direction.LEFT
        self.game.update()  # Move head to (90, 100) which collides with body
        self.assertTrue(self.game.is_game_over())
    
    def test_food_consumption(self):
        """Test food consumption and snake growth"""
        # Place food at a known position
        self.game.food_position = (110, 100)
        initial_length = self.game.get_snake_length()
        initial_score = self.game.get_score()
        
        # Move snake to eat food
        self.game.update()  # Snake moves right to (110, 100)
        
        # Check snake grew and score increased
        self.assertEqual(self.game.get_snake_length(), initial_length + 1)
        self.assertEqual(self.game.get_score(), initial_score + 1)
        
        # Food should be repositioned
        self.assertNotEqual(self.game.get_food_position(), (110, 100))
    
    def test_food_generation(self):
        """Test food is generated in valid positions"""
        # Fill most of the board with snake to test food generation
        positions = []
        for x in range(0, 200, 10):
            for y in range(0, 190, 10):  # Leave last row empty
                positions.append((x, y))
        
        self.game.snake_positions = positions
        food_pos = self.game._generate_food()
        
        # Food should be in the empty row
        self.assertEqual(food_pos[1], 190)
        self.assertNotIn(food_pos, positions)
    
    def test_reset_game(self):
        """Test game reset functionality"""
        # Modify game state
        self.game.snake_positions = [(50, 50), (40, 50), (30, 50)]
        self.game.direction = Direction.LEFT
        self.game.state = GameState.GAME_OVER
        self.game.score = 5
        
        # Reset game
        self.game.reset_game()
        
        # Check all values are reset
        self.assertEqual(self.game.state, GameState.PLAYING)
        self.assertEqual(self.game.score, 0)
        self.assertEqual(self.game.get_snake_length(), 1)
        self.assertEqual(self.game.direction, Direction.RIGHT)
        self.assertEqual(self.game.get_snake_head(), (100, 100))
    
    def test_game_state_methods(self):
        """Test various getter methods"""
        # Test initial state
        self.assertFalse(self.game.is_game_over())
        self.assertIsInstance(self.game.get_snake_body(), list)
        self.assertIsInstance(self.game.get_food_position(), tuple)
        
        # Test after game over
        self.game.state = GameState.GAME_OVER
        self.assertTrue(self.game.is_game_over())
    
    def test_no_movement_when_game_over(self):
        """Test snake doesn't move when game is over"""
        self.game.state = GameState.GAME_OVER
        initial_head = self.game.get_snake_head()
        
        self.game.update()
        
        # Head should not have moved
        self.assertEqual(self.game.get_snake_head(), initial_head)
    
    def test_no_direction_change_when_game_over(self):
        """Test direction cannot be changed when game is over"""
        self.game.state = GameState.GAME_OVER
        initial_direction = self.game.direction
        
        self.game.change_direction(Direction.UP)
        
        # Direction should not have changed
        self.assertEqual(self.game.direction, initial_direction)


class TestDirection(unittest.TestCase):
    """Test Direction enum"""
    
    def test_direction_values(self):
        """Test direction enum values are correct"""
        self.assertEqual(Direction.UP.value, (0, -1))
        self.assertEqual(Direction.DOWN.value, (0, 1))
        self.assertEqual(Direction.LEFT.value, (-1, 0))
        self.assertEqual(Direction.RIGHT.value, (1, 0))


class TestGameState(unittest.TestCase):
    """Test GameState enum"""
    
    def test_game_state_values(self):
        """Test game state enum values"""
        self.assertEqual(GameState.PLAYING.value, "playing")
        self.assertEqual(GameState.GAME_OVER.value, "game_over")


if __name__ == '__main__':
    unittest.main()