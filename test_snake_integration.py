"""
Additional Integration Tests for Snake Game
Tests for edge cases and integration scenarios
"""
import unittest
import random
from snake_game import SnakeGame, Direction, GameState


class TestSnakeGameIntegration(unittest.TestCase):
    """Integration tests for the complete snake game"""
    
    def setUp(self):
        """Set up test fixtures"""
        self.game = SnakeGame(width=100, height=100, block_size=10)
        random.seed(12345)  # Different seed for different test scenarios
    
    def test_complete_game_scenario(self):
        """Test a complete game scenario from start to finish"""
        # Initial state
        self.assertEqual(self.game.get_score(), 0)
        self.assertEqual(self.game.get_snake_length(), 1)
        
        # Move a few steps
        for _ in range(3):
            self.game.update()
        
        # Change direction and move
        self.game.change_direction(Direction.DOWN)
        self.game.update()
        
        # Should still be playing
        self.assertFalse(self.game.is_game_over())
        self.assertEqual(self.game.get_snake_length(), 1)  # No food eaten yet
    
    def test_food_placement_avoids_snake(self):
        """Test that food is never placed on the snake"""
        # Make a longer snake
        self.game.snake_positions = [(50, 50), (40, 50), (30, 50), (20, 50)]
        
        # Generate food multiple times
        for _ in range(10):
            food_pos = self.game._generate_food()
            self.assertNotIn(food_pos, self.game.snake_positions)
    
    def test_snake_growth_sequence(self):
        """Test sequence of snake growth when eating multiple foods"""
        initial_length = self.game.get_snake_length()
        
        # Simulate eating 3 foods in sequence
        for i in range(3):
            # Place food in snake's path
            head_x, head_y = self.game.get_snake_head()
            next_x = head_x + 10  # Snake moves right by default
            self.game.food_position = (next_x, head_y)
            
            # Update game - snake should eat food
            self.game.update()
            
            # Check growth
            expected_length = initial_length + i + 1
            self.assertEqual(self.game.get_snake_length(), expected_length)
            self.assertEqual(self.game.get_score(), i + 1)
    
    def test_rapid_direction_changes(self):
        """Test handling of rapid direction changes"""
        initial_direction = self.game.direction  # RIGHT
        
        # Try multiple rapid direction changes
        self.game.change_direction(Direction.DOWN)
        self.game.change_direction(Direction.LEFT)
        self.game.change_direction(Direction.RIGHT)  # Should be ignored (opposite to LEFT)
        
        # Should end up going LEFT (RIGHT was ignored)
        self.assertEqual(self.game.direction, Direction.LEFT)
        
        # One more valid change
        self.game.change_direction(Direction.UP)
        self.assertEqual(self.game.direction, Direction.UP)
    
    def test_minimum_board_size(self):
        """Test game with minimum board size"""
        # Create very small game
        small_game = SnakeGame(width=20, height=20, block_size=10)
        
        # Should work normally
        self.assertFalse(small_game.is_game_over())
        small_game.update()
        
        # Food should still be placeable
        food_pos = small_game.get_food_position()
        self.assertIsInstance(food_pos, tuple)
        self.assertEqual(len(food_pos), 2)
    
    def test_corner_collision_scenarios(self):
        """Test collision detection in corner scenarios"""
        # Test collision at exact corner
        self.game.snake_positions = [(0, 0)]
        self.game.direction = Direction.UP
        self.game.update()
        self.assertTrue(self.game.is_game_over())
        
        # Test collision at bottom-right corner
        self.game.reset_game()
        self.game.snake_positions = [(90, 90)]
        self.game.direction = Direction.RIGHT
        self.game.update()
        self.assertTrue(self.game.is_game_over())
    
    def test_long_snake_self_collision(self):
        """Test self-collision with a longer snake"""
        # Create a snake that forms a spiral
        spiral_positions = [
            (50, 50), (40, 50), (30, 50), (20, 50),  # horizontal line
            (20, 40), (20, 30), (20, 20),            # vertical line up
            (30, 20), (40, 20), (50, 20),            # horizontal line right
            (50, 30), (50, 40)                       # vertical line down
        ]
        
        self.game.snake_positions = spiral_positions
        self.game.direction = Direction.LEFT
        
        # Next move should cause collision with the horizontal line
        self.game.update()
        self.assertTrue(self.game.is_game_over())
    
    def test_game_reset_after_various_states(self):
        """Test game reset works correctly after different game states"""
        # Modify game to various states
        self.game.snake_positions = [(0, 10), (10, 10)]  # Head at edge
        self.game.direction = Direction.LEFT  # Will cause wall collision
        self.game.score = 5
        self.game.food_position = (80, 80)
        
        # Cause game over
        self.game.update()  # Should hit wall (move from x=0 to x=-10)
        self.assertTrue(self.game.is_game_over())
        
        # Reset and verify clean state
        self.game.reset_game()
        self.assertFalse(self.game.is_game_over())
        self.assertEqual(self.game.get_score(), 0)
        self.assertEqual(self.game.get_snake_length(), 1)
        self.assertEqual(self.game.direction, Direction.RIGHT)


class TestSnakeGameEdgeCases(unittest.TestCase):
    """Test edge cases and boundary conditions"""
    
    def test_food_generation_with_full_board(self):
        """Test food generation when board is nearly full"""
        game = SnakeGame(width=30, height=30, block_size=10)
        
        # Fill the board except for one spot
        all_positions = []
        for x in range(0, 30, 10):
            for y in range(0, 30, 10):
                all_positions.append((x, y))
        
        # Leave one position free
        free_position = all_positions.pop()
        game.snake_positions = all_positions
        
        # Food should be generated at the only free position
        food_pos = game._generate_food()
        self.assertEqual(food_pos, free_position)
    
    def test_direction_change_timing(self):
        """Test direction changes don't affect current move"""
        game = SnakeGame()
        initial_head = game.get_snake_head()
        
        # Change direction but don't update yet
        game.change_direction(Direction.DOWN)
        
        # Head shouldn't move until update is called
        self.assertEqual(game.get_snake_head(), initial_head)
        
        # After update, should move in new direction
        game.update()
        new_head = game.get_snake_head()
        expected_head = (initial_head[0], initial_head[1] + 10)
        self.assertEqual(new_head, expected_head)
    
    def test_multiple_food_consumption_in_sequence(self):
        """Test eating multiple foods placed in sequence"""
        game = SnakeGame(width=100, height=50, block_size=10)
        game.snake_positions = [(0, 20)]
        game.direction = Direction.RIGHT
        
        # Place food at regular intervals
        foods = [(10, 20), (20, 20), (30, 20)]
        score = 0
        
        for food_pos in foods:
            game.food_position = food_pos
            game.update()
            score += 1
            self.assertEqual(game.get_score(), score)
            self.assertEqual(game.get_snake_length(), score + 1)
    
    def test_invalid_board_dimensions(self):
        """Test game creation with various board dimensions"""
        # Very large board
        large_game = SnakeGame(width=1000, height=1000, block_size=10)
        self.assertIsNotNone(large_game)
        
        # Different block sizes
        small_block_game = SnakeGame(width=100, height=100, block_size=5)
        self.assertEqual(small_block_game.block_size, 5)
        
        large_block_game = SnakeGame(width=100, height=100, block_size=20)
        self.assertEqual(large_block_game.block_size, 20)


if __name__ == '__main__':
    unittest.main()