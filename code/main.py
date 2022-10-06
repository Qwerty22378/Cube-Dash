import pygame
import sys
from pygame.locals import *

from level import Level
from menus import MenuManager
from settings import screen_width, screen_height, fps


class Game:
    def __init__(self):
        # setup
        self.menu_manager = MenuManager(screen, clock)

    def setup_level(self):
        self.level = Level(screen, self.menu_manager.select_menu.level_path)
        self.level.update_fps_var(fps)

    def run(self, fps):
        if self.menu_manager.state:
            self.menu_manager.run()
            self.setup_level()
        else:
            self.menu_manager.state = self.level.run(fps)


pygame.init()

screen = pygame.display.set_mode((screen_width, screen_height))
clock = pygame.time.Clock()
game = Game()


if __name__ == '__main__':
    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()

        screen.fill('cyan')
        fps_counter = int(clock.get_fps())
        game.run(fps_counter)

        pygame.display.update()
        clock.tick(fps)


