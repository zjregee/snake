
import pygame
import sys
from snake_game import SnakeGame, Direction, GameState

# 初始化 Pygame
pygame.init()

# 屏幕尺寸
screen_width = 600
screen_height = 400
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption('贪吃蛇')

# 颜色
white = (255, 255, 255)
black = (0, 0, 0)
red = (213, 50, 80)
green = (0, 255, 0)

# 蛇和食物的尺寸
snake_block = 10
snake_speed = 15

# 字体
font_style = pygame.font.SysFont(None, 50)

def draw_snake(snake_block, snake_positions):
    """Draw the snake on the screen"""
    for pos in snake_positions:
        pygame.draw.rect(screen, black, [pos[0], pos[1], snake_block, snake_block])

def show_message(msg, color):
    """Display a message on the screen"""
    mesg = font_style.render(msg, True, color)
    screen.blit(mesg, [screen_width / 6, screen_height / 3])

def game_loop():
    """Main game loop using the refactored SnakeGame class"""
    # Create game instance
    game = SnakeGame(width=screen_width, height=screen_height, block_size=snake_block)
    clock = pygame.time.Clock()

    while True:
        # Handle game over state
        while game.is_game_over():
            screen.fill(white)
            show_message("你输了! 按 Q 退出或 C 重新开始", red)
            pygame.display.update()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_q:
                        pygame.quit()
                        sys.exit()
                    if event.key == pygame.K_c:
                        return  # 返回到 main() 函数来重启

        # Handle events during gameplay
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    game.change_direction(Direction.LEFT)
                elif event.key == pygame.K_RIGHT:
                    game.change_direction(Direction.RIGHT)
                elif event.key == pygame.K_UP:
                    game.change_direction(Direction.UP)
                elif event.key == pygame.K_DOWN:
                    game.change_direction(Direction.DOWN)

        # Update game state
        game.update()
        
        # Draw everything
        screen.fill(white)
        
        # Draw food
        food_pos = game.get_food_position()
        pygame.draw.rect(screen, green, [food_pos[0], food_pos[1], snake_block, snake_block])
        
        # Draw snake
        draw_snake(snake_block, game.get_snake_body())

        pygame.display.update()
        clock.tick(snake_speed)

def main():
    """Main function"""
    while True:
        game_loop()

if __name__ == "__main__":
    main()
