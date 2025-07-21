import pygame
import snake
import random
from time import sleep

def main():
    game = snake.Snake_Game()
    for i in range(1, 6):
        actions = []
        score = 0
        while game.death == False and game.win == False:
            actions = game.get_actions()
            game.render(actions[random.randint(0, len(actions) - 1)])
            score += game.evaluate_state()

        print("Game: {} Score: {}".format(i, score))
        game.reset()
        sleep(1)
    pygame.quit()

if __name__ == "__main__":
    main()