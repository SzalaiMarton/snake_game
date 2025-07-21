import pygame
import objects as obj

class Snake_Game:
    GAME_SPEED = 10
    TEXTURE_SIZE = 10
    width = 400
    height = 400
    running: bool

    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((self.width, self.height))

        self.font = pygame.font.SysFont(None, 36)
        self.cube_array = obj.create_map(int(self.width / obj.CUBE_TEXTURE_WIDTH), int(self.height / obj.CUBE_TEXTURE_HEIGHT))
        self.snake_spawn_point_x = obj.CUBE_TEXTURE_WIDTH * 15
        self.snake_spawn_point_y = obj.CUBE_TEXTURE_HEIGHT * 15
        self.snake = obj.Snake(self.snake_spawn_point_x, self.snake_spawn_point_y)
        self.apple = obj.Apple(1, 150, 150)

        self.current_snake_direction = obj.Snake_Direction.RIGHT
        self.score_tracker = self.font.render(f"Score: {self.snake.score}", True, (255, 255, 255))
        self.screen.blit(self.score_tracker, (10, 10))

        self.win = False
        self.death = False
        self.apple_pickup = False

    
    def reset(self):
        del self.snake
        del self.apple

        self.current_snake_direction = obj.Snake_Direction.RIGHT

        self.snake = obj.Snake(self.snake_spawn_point_x, self.snake_spawn_point_y)
        self.apple = obj.Apple(1, 150, 150)

        self.win = False
        self.death = False
        self.apple_pickup = False


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


    def render(self, action):
        self.apple_pickup = False
        self.get_direction_by_action(action)

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


    def get_state(self):
        """
        - returns: [0] - every part's pos from snake's body, [1] - apple's pos, [2] - isWin, [3] - isDeath, [4] - isApplePickup
        """

        snake_pos = []
        for part in self.snake.body:
            snake_pos.append([part.x, part.y])

        return snake_pos, [self.apple.x, self.apple.y], self.win, self.death, self.apple_pickup


    def get_actions(self):
        """
        - according to the current_snake_direction it returns the available actions
        - the ammount of actions is always 3
        """
        
        if self.current_snake_direction == obj.Snake_Direction.UP:
            return obj.Snake_Direction.UP, obj.Snake_Direction.RIGHT, obj.Snake_Direction.LEFT
        elif self.current_snake_direction == obj.Snake_Direction.DOWN:
            return obj.Snake_Direction.DOWN, obj.Snake_Direction.RIGHT, obj.Snake_Direction.LEFT
        elif self.current_snake_direction == obj.Snake_Direction.RIGHT:
            return obj.Snake_Direction.DOWN, obj.Snake_Direction.RIGHT, obj.Snake_Direction.UP
        else:
            return obj.Snake_Direction.DOWN, obj.Snake_Direction.LEFT, obj.Snake_Direction.UP
        

    def evaluate_state(self):
        """
        - returns: reward:[int]
        """
        
        state = self.get_state()

        head_pos = state[0][0]
        apple_pos = state[1]

        if state[2]:
            return 200
        elif state[3]:
            return -200
        elif state[4]:
            return 20
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
                    return 1
                elif current_distance_y > prev_distance_y:
                    return -1
                else:
                    return 0
            else:
                if current_distance_x < prev_distance_x:
                    return 1
                elif current_distance_x > prev_distance_x:
                    return -1
                else:
                    return 0

