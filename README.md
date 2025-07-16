# Snake Game 贪吃蛇

A classic Snake game implemented in Python using pygame, with comprehensive unit testing.

## Project Structure

```
snake/
├── main.py                    # Main game application with pygame interface
├── snake_game.py             # Core game logic (testable without pygame)
├── test_snake_game.py        # Unit tests for core game logic
├── test_snake_integration.py # Integration tests and edge cases
├── run_tests.py              # Test runner script
└── README.md                 # This file
```

## Features

- Classic Snake gameplay with arrow key controls
- Collision detection (walls and self-collision)
- Food generation and consumption
- Score tracking
- Game reset functionality
- Comprehensive test coverage

## Game Controls

- **Arrow Keys**: Control snake direction
- **Q**: Quit game (when game over)
- **C**: Continue/restart game (when game over)

## Running the Game

```bash
python3 main.py
```

**Note**: Requires pygame. Install with:
```bash
pip install pygame
```

## Running Tests

### Run all tests:
```bash
python3 run_tests.py
```

### Run specific test files:
```bash
# Core game logic tests
python3 -m unittest test_snake_game.py -v

# Integration and edge case tests  
python3 -m unittest test_snake_integration.py -v
```

### Run tests with unittest discovery:
```bash
python3 -m unittest discover -s . -p "test_*.py" -v
```

## Test Coverage

The test suite includes **25 comprehensive tests** covering:

### Core Game Logic (`test_snake_game.py`)
- ✅ Initial game state validation
- ✅ Snake movement in all directions
- ✅ Direction change prevention (can't reverse into self)
- ✅ Wall collision detection
- ✅ Self-collision detection
- ✅ Food consumption and snake growth
- ✅ Food generation algorithms
- ✅ Game reset functionality
- ✅ Game state management
- ✅ Enum value validation

### Integration & Edge Cases (`test_snake_integration.py`)
- ✅ Complete game scenarios
- ✅ Food placement collision avoidance
- ✅ Sequential snake growth
- ✅ Rapid direction changes
- ✅ Minimum board size handling
- ✅ Corner collision scenarios
- ✅ Long snake self-collision
- ✅ Game reset after various states
- ✅ Direction change timing
- ✅ Food generation on nearly full board
- ✅ Multiple food consumption sequences
- ✅ Various board dimensions

## Architecture

The game is designed with separation of concerns:

- **`snake_game.py`**: Contains pure game logic independent of pygame
- **`main.py`**: Handles pygame rendering and user interface
- **Test files**: Comprehensive test coverage without requiring pygame display

This architecture allows:
- Unit testing without GUI dependencies
- Easy logic modifications
- Better code maintainability
- Clear separation between game rules and presentation

## Development

The refactored code maintains 100% compatibility with the original game while adding:
- Type hints for better code clarity
- Enum-based direction and state management
- Comprehensive error handling
- Full test coverage
- Modular design for easier maintenance

## Test Results

```
Tests run: 25
Failures: 0
Errors: 0
✅ All tests passed!
```