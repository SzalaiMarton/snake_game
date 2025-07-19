import pygame
import random
from typing import Optional
from enum import Enum

APPLE_VALUE = 1
CUBE_TEXTURE_WIDTH = 10
CUBE_TEXTURE_HEIGHT = 10

MAP_OFFSET = 0

class Snake_Direction(Enum):
    UP = [0, -1]
    DOWN = [0, 1]
    RIGHT = [1, 0]
    LEFT = [-1, 0]


class Object:
    x: int
    y: int
    texture: pygame.Surface

    def __init__(self, tex_name: str, x: int = 0, y: int = 0) -> None:
        self.texture = pygame.image.load("tex/" + tex_name + ".png")
        self.set_pos(x, y)

    def draw_self(self, screen: pygame.Surface) -> None:
        screen.blit(self.texture, (self.x, self.y))

    def set_pos(self, x: int, y: int) -> None:
        self.x = x
        self.y = y


class Snake:
    x: int
    y: int
    body: list[Object] = []
    score: int

    def __init__(self, x: int, y: int):
        self.x = x
        self.y = y
        self.score = 0
        for i in range(1, 4):
            self.body.append(Object("snake", self.x, (self.y - CUBE_TEXTURE_HEIGHT * i)))

    def draw_self(self, screen: pygame.Surface):
        for part in self.body:
            part.draw_self(screen)

    def move_snake(self, direction: Snake_Direction):
        self.x += CUBE_TEXTURE_WIDTH * direction.value[0]
        self.y += CUBE_TEXTURE_HEIGHT * direction.value[1]

        self.body.insert(0, Object("snake", self.x, self.y))
        self.body.pop()

class Cube(Object):
    has_apple: bool

    def __init__(self, x: int = 0, y: int = 0) -> None:
        super().__init__("cube", x, y)
        self.has_apple = False


class Apple(Object):
    value: int

    def __init__(self, custom_value: int, x: int = 0, y: int = 0) -> None:
        self.value = custom_value
        super().__init__("apple", x, y)

    def move_apple(self, cubes_array: list[Cube], snake: Snake, screen: pygame.Surface) -> None:
        free_cells = get_free_cells(cubes_array, snake)

        if len(free_cells) == 0:
            print("Out of free cells.")
            return None

        random_cell = free_cells[random.randrange(0, len(free_cells))]

        self.x = random_cell.x
        self.y = random_cell.y
        self.draw_self(screen)

def create_map(width: int, height: int) -> list[Cube]:
    cubes: list[Cube] = []
    for y_index in range(MAP_OFFSET, height + MAP_OFFSET):
        for x_index in range(MAP_OFFSET ,width + MAP_OFFSET):
            cubes.append(Cube((CUBE_TEXTURE_WIDTH * x_index), (CUBE_TEXTURE_HEIGHT * y_index)))

    return cubes

def get_free_cells(cubes_array: list[Cube], snake: Snake) -> list[Cube]:
    free_cells: list[Cube] = []
    for cube in cubes_array:
        if not is_cell_occupied(snake, cube):
            free_cells.append(cube)

    return free_cells


def is_cell_occupied(snake: Snake, cube: Cube) -> bool:
    for snake_part in snake.body:
        if (cube.x == snake_part.x and cube.y == snake_part.y) or cube.has_apple:
            return True
    return False


def refresh_screen(screen: pygame.Surface, cubes_array: list[Cube], apple: Apple, snake: Snake) -> None:
    screen.fill((0,0,0))

    for cube in cubes_array:
        cube.draw_self(screen)

    apple.draw_self(screen)

    snake.draw_self(screen)

    pygame.display.flip()

def check_game_over(snake: Snake, screen_width: int, screen_height: int) -> bool:
    return ((snake.x < 0 or snake.x > screen_width) or (snake.y < 0 or snake.y > screen_height))

def check_apple_eat(snake: Snake, apple: Apple) -> bool:
    return (snake.x == apple.x and snake.y == apple.y)