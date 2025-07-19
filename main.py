import pygame
import objects as obj

GAME_SPEED = 10
TEXTURE_SIZE = 10

pygame.init()
width = 720
height = 720
screen = pygame.display.set_mode((width, height))
clock = pygame.time.Clock()
running = True

cube_array = obj.create_map(int(width / TEXTURE_SIZE), int(height / TEXTURE_SIZE))
snake_spawn_point_x = TEXTURE_SIZE * 15
snake_spawn_point_y = TEXTURE_SIZE * 15
snake = obj.Snake(snake_spawn_point_x, snake_spawn_point_y)
apple: obj.Apple = obj.Apple(1, 150, 150)

current_snake_direction = obj.Snake_Direction.RIGHT

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    keys = pygame.key.get_pressed()
    if keys[pygame.K_w] and not current_snake_direction == obj.Snake_Direction.UP and not current_snake_direction == obj.Snake_Direction.DOWN:
        current_snake_direction = obj.Snake_Direction.UP
    elif keys[pygame.K_s] and not current_snake_direction == obj.Snake_Direction.DOWN and not current_snake_direction == obj.Snake_Direction.UP:
        current_snake_direction = obj.Snake_Direction.DOWN
    elif keys[pygame.K_d] and not current_snake_direction == obj.Snake_Direction.RIGHT and not current_snake_direction == obj.Snake_Direction.LEFT:
        current_snake_direction = obj.Snake_Direction.RIGHT
    elif keys[pygame.K_a] and not current_snake_direction == obj.Snake_Direction.LEFT and not current_snake_direction == obj.Snake_Direction.RIGHT:
        current_snake_direction = obj.Snake_Direction.LEFT

    if current_snake_direction:
        snake.move_snake(current_snake_direction)

    if obj.check_apple_eat(snake, apple):
        snake.score += apple.value
        print("score: ", snake.score)
        apple.move_apple(cube_array, snake, screen)

    if obj.check_game_over(snake, width, height):
        running = False

    obj.refresh_screen(screen, cube_array, apple, snake)

    clock.tick(GAME_SPEED)

pygame.quit()