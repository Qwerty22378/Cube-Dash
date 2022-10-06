import sys

import pygame
from pygame.locals import *

from game_data import levels
from import_assets import import_folder
from menu_data import *
from settings import *
from tiles import StaticTile, ButtonTile, AnimatedTile, LevelButtonTile, Tile


class MenuManager:
    def __init__(self, display, clock):
        # setup
        self.display = display
        self.clock = clock
        self.state = 'main_menu'

        # main menu setup
        self.main_menu = MainMenu(self.display, self.clock)

        # select_menu setup
        self.select_menu = SelectLevel(self.display, self.clock)

    def run(self):
        while self.state:
            if self.state == 'main_menu':
                self.main_menu.state = 'main_menu'
                self.state = self.main_menu.show()

            if self.state == 'select_level':
                self.select_menu.setup_level_buttons(levels[self.main_menu.difficulty_menu.difficulty])
                self.state = self.select_menu.show()


class MainMenu:
    def __init__(self, display, clock):
        # setup
        self.display = display
        self.clock = clock
        self.showing = True
        self.state = 'main_menu'

        # setup popups
        self.difficulty = 0
        self.difficulty_menu = DifficultyMenu(self.display, self.clock, self.difficulty)

        # setup main_menu sprites
        self.setup_sprites()

    def setup_sprites(self):
        # non interactive images
        self.images = pygame.sprite.Group()

        bg_img_path = resources_path['bg']
        bg_img = pygame.image.load(bg_img_path)
        bg_sprite = StaticTile((0, 0), (screen_width, screen_height), bg_img)
        self.images.add(bg_sprite)

        title_path = resources_path['title']
        title_img = pygame.image.load(title_path).convert_alpha()
        title_size = title_img.get_size()
        title_pos = ((screen_width - title_size[0]) / 2, (screen_height - title_size[1]) / 2)
        title_sprite = StaticTile(title_pos, title_size, title_img)
        self.images.add(title_sprite)

        player_path = resources_path['player']
        player_img_list = import_folder(player_path)
        player_size = player_img_list[0].get_size()
        player_pos = ((screen_width - player_size[0]) / 2, (screen_height - player_size[1]) / 3)
        player_sprite = AnimatedTile(player_pos, player_size, player_img_list)
        player_sprite.animation_speed = 0.3
        self.images.add(player_sprite)

        # difficulty_label
        self.difficulty_font0 = pygame.font.SysFont('Arial', 18)
        self.update_difficulty_label()

        # buttons
        self.buttons = pygame.sprite.Group()

        play_button_path = resources_path['play']
        play_img_list = import_folder(play_button_path)
        play_size = play_img_list[0].get_size()
        play_pos = ((screen_width - play_size[0]) / 2, (screen_height * 2 - play_size[1]) / 3)
        play_sprite = ButtonTile(play_pos, play_size, play_img_list, 'play')
        self.buttons.add(play_sprite)

        difficulty_button_path = resources_path['difficulty_button']
        difficulty_button_img_list = import_folder(difficulty_button_path)
        difficulty_button_size = difficulty_button_img_list[0].get_size()
        difficulty_button_pos = ((screen_width - difficulty_button_size[0]) / 2, screen_height * 3 / 4)
        difficulty_button_sprite = ButtonTile(difficulty_button_pos, difficulty_button_size, difficulty_button_img_list,
                                              'difficulty')
        self.buttons.add(difficulty_button_sprite)

    def update_difficulty_label(self):
        if self.difficulty == 0:
            text = 'Easy'
        elif self.difficulty == 1:
            text = 'Normal'
        elif self.difficulty == 2:
            text = 'Hard'

        label0 = self.difficulty_font0.render(text, 1, 'white')
        label0_size = label0.get_size()
        label0_pos = ((screen_width - label0_size[0]) / 2, screen_height * 4 / 5)
        self.display.blit(label0, label0_pos)

    def event_handler(self):
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()

            if event.type == MOUSEBUTTONUP:
                mouse_pos = pygame.mouse.get_pos()
                for sprite in self.buttons.sprites():
                    if sprite.rect.collidepoint(mouse_pos):
                        self.button_click(sprite.type)

    def set_button_state(self):
        mouse_pos = pygame.mouse.get_pos()
        for sprite in self.buttons.sprites():
            if sprite.rect.collidepoint(mouse_pos):
                sprite.image = sprite.img_list[1]
            else:
                sprite.image = sprite.img_list[0]

    def button_click(self, type):
        if type == 'play':
            self.showing = False
            self.state = 'select_level'

        elif type == 'difficulty':
            self.difficulty = self.difficulty_menu.show()

    def show(self):
        self.showing = True

        while self.showing:
            self.event_handler()

            # draw non interactive images
            self.images.update()
            self.images.draw(self.display)

            # draw buttons
            self.set_button_state()
            self.buttons.draw(self.display)

            # draw difficulty label
            self.update_difficulty_label()

            # update display
            pygame.display.update()
            self.clock.tick(30)

        return self.state


class PopupMenu:
    def __init__(self, display, clock):
        self.display = display
        self.clock = clock
        self.showing = False

        self.set_default_sprites()

    def set_default_sprites(self):
        self.window = pygame.sprite.GroupSingle()

        # bg_window
        bg_window_path = resources_path['popup_bg']
        bg_window_img = pygame.image.load(bg_window_path)
        bg_window_size = bg_window_img.get_size()
        bg_window_pos = ((screen_width - bg_window_size[0]) / 2, (screen_height - bg_window_size[1]) / 2)
        self.width, self.height = bg_window_size
        bg_sprite = StaticTile((0, 0), (screen_width, screen_height), bg_window_img)
        self.window.add(bg_sprite)

        # set surface
        self.surface = pygame.sprite.GroupSingle()
        self.surface_sprite = Tile(bg_window_pos, bg_window_size)
        self.surface.add(self.surface_sprite)

        self.images = pygame.sprite.Group()
        self.buttons = pygame.sprite.Group()

    def get_mouse_pos(self):
        pos = pygame.mouse.get_pos()
        pos = (pos[0] - self.surface_sprite.rect.x, pos[1] - self.surface_sprite.rect.y)
        return pos

    def event_handler(self):
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()

            if event.type == MOUSEBUTTONUP:
                mouse_pos = pygame.mouse.get_pos()
                if self.surface_sprite.rect.collidepoint(mouse_pos):
                    mouse_pos = self.get_mouse_pos()
                    for sprite in self.buttons.sprites():
                        if sprite.rect.collidepoint(mouse_pos):
                            self.button_click(sprite.type)
                else:
                    self.showing = False

    def set_button_state(self):
        mouse_pos = self.get_mouse_pos()
        for sprite in self.buttons.sprites():
            if sprite.rect.collidepoint(mouse_pos):
                sprite.image = sprite.img_list[1]
            else:
                sprite.image = sprite.img_list[0]

    def button_click(self, type):
        pass


class DifficultyMenu(PopupMenu):
    def __init__(self, display, clock, difficulty):
        super().__init__(display, clock)
        self.difficulty = difficulty

        self.setup_buttons_sprites()

    def setup_buttons_sprites(self):
        easy_button_path = resources_path['easy_button']
        easy_button_img_list = import_folder(easy_button_path)
        easy_button_size = easy_button_img_list[0].get_size()
        easy_button_pos = ((self.width - easy_button_size[0]) / 2, 10)
        easy_button_sprite = ButtonTile(easy_button_pos, easy_button_size, easy_button_img_list, 'easy')
        self.buttons.add(easy_button_sprite)

        normal_button_path = resources_path['normal_button']
        normal_button_img_list = import_folder(normal_button_path)
        normal_button_size = normal_button_img_list[0].get_size()
        normal_button_pos = ((self.width - normal_button_size[0]) / 2, (self.height - normal_button_size[1]) / 2)
        normal_button_sprite = ButtonTile(normal_button_pos, normal_button_size, normal_button_img_list, 'normal')
        self.buttons.add(normal_button_sprite)

        hard_button_path = resources_path['hard_button']
        hard_button_img_list = import_folder(hard_button_path)
        hard_button_size = hard_button_img_list[0].get_size()
        hard_button_pos = ((self.width - hard_button_size[0]) / 2, (self.height * 2) / 3)
        hard_button_sprite = ButtonTile(hard_button_pos, hard_button_size, hard_button_img_list, 'hard')
        self.buttons.add(hard_button_sprite)

    def button_click(self, type):
        if type == 'easy':
            self.difficulty = 0
        elif type == 'normal':
            self.difficulty = 1
        elif type == 'hard':
            self.difficulty = 2
        self.showing = False

    def show(self):
        self.showing = True

        while self.showing:
            self.event_handler()

            # window
            self.window.draw(self.surface_sprite.image)

            # draw non interactive images
            self.images.update()
            self.images.draw(self.surface_sprite.image)

            # draw buttons
            self.set_button_state()
            self.buttons.draw(self.surface_sprite.image)

            # draw surface on main display
            self.surface.draw(self.display)

            # update display
            pygame.display.update()
            self.clock.tick(30)

        return self.difficulty


class SelectLevel:
    def __init__(self, display, clock):
        # setup
        self.display = display
        self.clock = clock
        self.shift = 0
        self.showing = False
        self.state = 'select_level'
        self.selecting = True
        self.dir = levels[0]['tutorial']

        self.setup_sprites()

    def setup_sprites(self):
        # setup static images
        self.images = pygame.sprite.Group()

        bg_img_path = resources_path['bg']
        bg_img = pygame.image.load(bg_img_path)
        bg_sprite = StaticTile((0, 0), (screen_width, screen_height), bg_img)
        self.images.add(bg_sprite)

        # setup static buttons
        self.static_buttons = pygame.sprite.Group()

        exit_path = resources_path['exit']
        exit_img_list = import_folder(exit_path)
        exit_sprite = ButtonTile((0, 0), exit_img_list[0].get_size(), exit_img_list, 'exit')
        self.static_buttons.add(exit_sprite)

    def setup_level_buttons(self, level_list):
        self.level_buttons = pygame.sprite.Group()

        for keys_index, key in enumerate(level_list.keys()):
            img_list = import_folder(resources_path['level_button'])
            img_size = img_list[0].get_size()
            img_pos_x = (screen_width - img_size[0]) / 2

            sprite = LevelButtonTile((img_pos_x, (keys_index * (img_size[1] + 5) + 20)),
                                     img_size,
                                     img_list,
                                     key,
                                     level_list[key]
                                     )
            self.level_buttons.add(sprite)

    def event_handler(self):
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()

            elif event.type == MOUSEBUTTONDOWN:
                mouse_rel = pygame.mouse.get_rel()
                if abs(mouse_rel[1]) > 30:
                    self.scroll()

            elif event.type == MOUSEBUTTONUP:
                mouse_rel = pygame.mouse.get_rel()
                mouse_pos = pygame.mouse.get_pos()
                for sprite in self.level_buttons.sprites():
                    if sprite.rect.collidepoint(mouse_pos):
                        self.level_button_click(sprite.type)
                for sprite in self.static_buttons.sprites():
                    if sprite.rect.collidepoint(mouse_pos):
                        self.static_button_click(sprite.type)


    def scroll(self):
        while pygame.mouse.get_pressed()[0]:
            for event in pygame.event.get():
                if event.type == QUIT:
                    pygame.quit()
                    sys.exit()
            mouse_rel = pygame.mouse.get_rel()
            self.shift = mouse_rel[1]

            self.draw()

        self.scroll_limit()

    def level_button_click(self, type):
        self.showing = False
        self.state = ''
        self.level_path = type

    def static_button_click(self, type):
        if type == 'exit':
            self.showing = False
            self.state = 'main_menu'

    def set_button_state(self):
        # on mouse over
        mouse_pos = pygame.mouse.get_pos()
        for sprite in self.static_buttons.sprites():
            if sprite.rect.collidepoint(mouse_pos):
                sprite.image = sprite.img_list[1]
            else:
                sprite.image = sprite.img_list[0]

        for sprite in self.level_buttons.sprites():
            if sprite.rect.collidepoint(mouse_pos):
                sprite.image = sprite.img_list[1]
            else:
                sprite.image = sprite.img_list[0]

    def scroll_limit(self):
        buttons = self.level_buttons.sprites()

        bottom = screen_height - buttons[0].rect.height * 2
        top = buttons[0].rect.height

        while buttons[-1].rect.y < bottom and buttons[0].rect.y <= top:
            self.shift = 30

            self.draw()

        while buttons[0].rect.y > top:
            self.shift = -30

            self.draw()

        self.shift = 0

    def draw(self):
        self.event_handler()

        # draw non interactive images
        self.images.update()
        self.images.draw(self.display)

        # draw buttons
        self.set_button_state()
        self.static_buttons.draw(self.display)

        # draw level buttons
        self.level_buttons.update(self.shift)
        self.level_buttons.draw(self.display)

        # update display
        pygame.display.update()
        self.clock.tick(30)

    def show(self):
        self.showing = True

        while self.showing:
            self.draw()

        return self.state
