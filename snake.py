import pygame
import snake_objects as obj
import random

class Snake_Game:
    GAME_SPEED = 10
    width = 600
    height = 600
    running: bool

    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((self.width, self.height))

        self.font = pygame.font.SysFont(None, 36)
        self.cube_array = obj.create_map(int(self.width / obj.Settings.CUBE_TEXTURE_WIDTH), int(self.height / obj.Settings.CUBE_TEXTURE_HEIGHT))
        self.snake_spawn_point_x = obj.Settings.CUBE_TEXTURE_WIDTH * 15
        self.snake_spawn_point_y = obj.Settings.CUBE_TEXTURE_HEIGHT * 15
        self.snake = obj.Snake(self.snake_spawn_point_x, self.snake_spawn_point_y)
        free_cubes = obj.get_free_cells(self.cube_array, self.snake)
        random_cube = free_cubes[random.randint(0, len(free_cubes) - 1)]
        self.apple = obj.Apple(1, random_cube.x, random_cube.y)

        self.current_snake_direction = obj.Snake_Direction.RIGHT
        self.score_tracker = self.font.render(f"Score: {self.snake.score}", True, (255, 255, 255))
        self.screen.blit(self.score_tracker, (10, 10))

        self.win = False
        self.death = False
        self.apple_pickup = False

    def shutdown(self):
        pygame.quit()
    
    def reset(self):
        for part in self.snake.body:
            del part
        self.snake.body.clear()
        del self.snake
        del self.apple

        self.current_snake_direction = obj.Snake_Direction.RIGHT

        self.snake = obj.Snake(self.snake_spawn_point_x, self.snake_spawn_point_y)
        free_cubes = obj.get_free_cells(self.cube_array, self.snake)
        random_cube = free_cubes[random.randint(0, len(free_cubes) - 1)]
        self.apple = obj.Apple(1, random_cube.x, random_cube.y)
        self.score_tracker = self.font.render(f"Score: {self.snake.score}", True, (255, 255, 255))
        self.screen.blit(self.score_tracker, (10, 10))

        self.win = False
        self.death = False
        self.apple_pickup = False

        obj.refresh_screen(self.screen, self.cube_array, self.apple, self.snake, self.score_tracker)

    def get_direction_by_key(self, keys):
        if keys[pygame.K_w] and not self.current_snake_direction == obj.Snake_Direction.UP and not self.current_snake_direction == obj.Snake_Direction.DOWN:
            self.current_snake_direction = obj.Snake_Direction.UP
        elif keys[pygame.K_s] and not self.current_snake_direction == obj.Snake_Direction.DOWN and not self.current_snake_direction == obj.Snake_Direction.UP:
            self.current_snake_direction = obj.Snake_Direction.DOWN
        elif keys[pygame.K_d] and not self.current_snake_direction == obj.Snake_Direction.RIGHT and not self.current_snake_direction == obj.Snake_Direction.LEFT:
            self.current_snake_direction = obj.Snake_Direction.RIGHT
        elif keys[pygame.K_a] and not self.current_snake_direction == obj.Snake_Direction.LEFT and not self.current_snake_direction == obj.Snake_Direction.RIGHT:
            self.current_snake_direction = obj.Snake_Direction.LEFT


    def get_direction_by_action(self, action):
        if action == obj.Snake_Direction.UP and not self.current_snake_direction == obj.Snake_Direction.UP and not self.current_snake_direction == obj.Snake_Direction.DOWN:
            self.current_snake_direction = obj.Snake_Direction.UP
        elif action == obj.Snake_Direction.DOWN and not self.current_snake_direction == obj.Snake_Direction.DOWN and not self.current_snake_direction == obj.Snake_Direction.UP:
            self.current_snake_direction = obj.Snake_Direction.DOWN
        elif action == obj.Snake_Direction.RIGHT and not self.current_snake_direction == obj.Snake_Direction.RIGHT and not self.current_snake_direction == obj.Snake_Direction.LEFT:
            self.current_snake_direction = obj.Snake_Direction.RIGHT
        elif action == obj.Snake_Direction.LEFT and not self.current_snake_direction == obj.Snake_Direction.LEFT and not self.current_snake_direction == obj.Snake_Direction.RIGHT:
            self.current_snake_direction = obj.Snake_Direction.LEFT


    def run(self):
        self.running = True
        self.clock = pygame.time.Clock()

        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
            
            self.get_direction_by_key(pygame.key.get_pressed())

            if self.current_snake_direction:
                self.snake.move(self.current_snake_direction)

            if obj.check_apple_eat(self.snake, self.apple):
                self.snake.score += self.apple.value
                self.snake.body.append(obj.Object("snake", self.snake.body[-1].x, self.snake.body[-1].y))
                self.score_tracker = self.font.render(f"Score: {self.snake.score}", True, (255, 255, 255))
                self.win = self.apple.move(self.cube_array, self.snake, self.screen)

            if self.win:
                self.running = False
                break

            if obj.check_game_over(self.snake, self.width, self.height):
                self.death = True
                self.running = False

            obj.refresh_screen(self.screen, self.cube_array, self.apple, self.snake, self.score_tracker)

            self.clock.tick(self.GAME_SPEED)
        pygame.quit()


    def convert_number_into_action(self, num) -> obj.Snake_Direction:
        if type(num) == obj.Snake_Direction:
            return num

        if num == 0:
            return obj.Snake_Direction.UP
        elif num == 1:
            return obj.Snake_Direction.RIGHT
        elif num == 2:
            return obj.Snake_Direction.DOWN
        else:
            return obj.Snake_Direction.LEFT


    def render(self, action):
        self.apple_pickup = False
        self.get_direction_by_action(self.convert_number_into_action(action))

        if self.current_snake_direction:
            self.snake.move(self.current_snake_direction)
        
        if obj.check_apple_eat(self.snake, self.apple):
            self.snake.score += self.apple.value
            self.snake.body.append(obj.Object("snake", self.snake.body[-1].x, self.snake.body[-1].y))
            self.score_tracker = self.font.render(f"Score: {self.snake.score}", True, (255, 255, 255))
            self.win = self.apple.move(self.cube_array, self.snake, self.screen)
            self.apple_pickup = True

        if self.win:
            return

        if obj.check_game_over(self.snake, self.width, self.height):
            self.death = True

        obj.refresh_screen(self.screen, self.cube_array, self.apple, self.snake, self.score_tracker)

    def get_features(self):
        """
        - return: 
        - [0] - apple_dx
        - [1] - apple_dy

        - [2] - current_dx
        - [3] - current_dy

        - [4] - is_forward_blocked:bool
        - [5] - is_behind_blocked:bool
        - [6] - is_left_blocked:bool
        - [7] - is_right_blocked:bool

        - [8] - top_wall_distance

        - [9] - bot_wall_distance

        - [10] - left_wall_distance

        - [11] - right_wall_distance

        """

        game_state = self.get_game_state()
        apple_pos = game_state[1]
        head_pos = game_state[0][0]

        apple_dx = apple_pos[0] - head_pos[0]
        apple_dy = apple_pos[1] - head_pos[1]

        # normalize the dx, dy to only be -1, 0 or 1
        if not apple_dx == 0:
            apple_dx /= abs(apple_dx)

        if not apple_dy == 0:
            apple_dy /= abs(apple_dy)


        forward_cell = obj.is_cell_occupied(self.snake, obj.get_cube_by_pos(self.cube_array, head_pos[0], head_pos[1] - obj.Settings.CUBE_TEXTURE_HEIGHT))
        behind_cell = obj.is_cell_occupied(self.snake, obj.get_cube_by_pos(self.cube_array, head_pos[0], head_pos[1] + obj.Settings.CUBE_TEXTURE_HEIGHT))
        left_cell = obj.is_cell_occupied(self.snake, obj.get_cube_by_pos(self.cube_array, head_pos[0] - obj.Settings.CUBE_TEXTURE_WIDTH, head_pos[1]))
        right_cell = obj.is_cell_occupied(self.snake, obj.get_cube_by_pos(self.cube_array, head_pos[0] + obj.Settings.CUBE_TEXTURE_WIDTH, head_pos[1]))


        top_wall_distance = head_pos[1]
        bottom_wall_distance = self.height - head_pos[1]
        left_wall_distance = head_pos[0]
        right_wall_distance = self.width - head_pos[0]

        return (apple_dx, apple_dy, self.current_snake_direction.value[0], self.current_snake_direction.value[1], forward_cell, behind_cell, left_cell, right_cell,
        top_wall_distance, bottom_wall_distance, left_wall_distance, right_wall_distance)


    def get_game_state(self):
        """
        - return: [0] - every part's pos from snake's body, [1] - apple's pos, [2] - isWin, [3] - isDeath, [4] - isApplePickUp
        """

        snake_pos = []
        for part in self.snake.body:
            snake_pos.append([part.x, part.y])

        return snake_pos, [self.apple.x, self.apple.y], self.win, self.death, self.apple_pickup


    def get_actions(self):
        """
        - returns all the possible directions
        """
        
        return 0, 1, 2, 3
        

    def evaluate_state(self):
        """
        - returns: [0] - reward, [1] - isDone
        """
        
        state = self.get_game_state()

        head_pos = state[0][0]
        apple_pos = state[1]

        if state[2]:
            return 200, (state[2] or state[3])
        elif state[3]:
            return 0, (state[2] or state[3])
        elif state[4]:
            return 20, (state[2] or state[3])
        else:
            prev_pos_x = head_pos[0] - self.current_snake_direction.value[0]
            prev_pos_y = head_pos[1] - self.current_snake_direction.value[1]
            
            # previous frame's distance between the apple and the snake's head
            prev_distance_x = abs(apple_pos[0] - prev_pos_x)
            prev_distance_y = abs(apple_pos[1] - prev_pos_y)

            # current frame's distance between the apple and the snake's head
            current_distance_x = abs(apple_pos[0] - head_pos[0])
            current_distance_y = abs(apple_pos[1] - head_pos[1])

            if self.current_snake_direction == obj.Snake_Direction.UP or self.current_snake_direction == obj.Snake_Direction.DOWN:
                if current_distance_y < prev_distance_y:
                    return 1, (state[2] or state[3])
                elif current_distance_y > prev_distance_y:
                    return 0, (state[2] or state[3])
                else:
                    return 0, (state[2] or state[3])
            else:
                if current_distance_x < prev_distance_x:
                    return 1, (state[2] or state[3])
                elif current_distance_x > prev_distance_x:
                    return 0, (state[2] or state[3])
                else:
                    return 0, (state[2] or state[3])

