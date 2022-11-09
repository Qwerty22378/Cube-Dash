import pygame

from game_data import *
from import_assets import import_csv_layout, import_cut_graphics, import_folder, import_files_path
from player import Player
from settings import *
from tiles import StaticTile, AnimatedTile


class Level:
    def __init__(self, display, level_path):
        self.display = display
        self.state = ''
        self.level_path = level_path

        paths = import_files_path(level_path)

        # setup group sprites
        self.collision_tiles = pygame.sprite.Group()
        self.images_tiles = pygame.sprite.Group()
        self.scores_tiles = pygame.sprite.Group()
        self.kill_tiles = pygame.sprite.Group()
        self.change_direction = pygame.sprite.Group()
        self.teleport_list = []
        self.teleporting = False
        self.changed_dir = False
        self.changed_dir_tile = None

        self.create_tiles(paths)

        # player setup
        player_path = level_path + '/_player.csv'
        player_layout = import_csv_layout(player_path)
        self.player = self.create_player(player_layout)
        self.player_sprite = self.player.sprite

        # animation reset var
        self.current_x = 0
        self.current_y = 0

        # fps counter var
        self.font = pygame.font.SysFont("Arial", 18)

        # score
        self.score = 0

    def create_tiles(self, paths):
        for layer in paths:
            layer_path = self.level_path + '/' + layer
            layer_name = layer[:-4]
            layer_name = layer_name[5:]

            layer_img_list_path = self.level_path + '/graphics/' + layer_name
            if layer[3] == 't':
                layer_img_list = import_cut_graphics(layer_img_list_path + '.png')
            elif layer[3] == 'f':
                layer_img_list = import_folder(layer_img_list_path)

            layout = import_csv_layout(layer_path)

            teleport_group = pygame.sprite.Group()
            teleport = False

            for row_index, row in enumerate(layout):
                for col_index, val in enumerate(row):
                    if val != '-1':
                        x = col_index * tile_size
                        y = row_index * tile_size

                        if layer[2] == 's':
                            sprite = StaticTile((x, y), (tile_size, tile_size), layer_img_list[int(val)])
                        elif layer[2] == 'a':
                            sprite = AnimatedTile((x, y), (tile_size, tile_size), layer_img_list)

                        if layer[1] == 'c':
                            self.collision_tiles.add(sprite)
                        elif layer[1] == 's':
                            self.scores_tiles.add(sprite)
                        elif layer[1] == 't':
                            teleport_group.add(sprite)
                            teleport = True
                        elif layer[1] == 'k':
                            self.kill_tiles.add(sprite)
                        elif layer[1] == 'i':
                            self.images_tiles.add(sprite)
                        elif layer[1] == 'd':
                            self.change_direction.add(sprite)

            if teleport:
                self.teleport_list.append(teleport_group)

    def create_player(self, layout):
        sprite_group_single = pygame.sprite.GroupSingle()

        for row_index, row in enumerate(layout):
            for col_index, val in enumerate(row):
                if val == '0':
                    x = col_index * tile_size
                    y = row_index * tile_size

                    sprite = Player((x, y))
                    sprite_group_single.add(sprite)

        return sprite_group_single

    def update_fps_var(self, fps):
        self.player_sprite.speed = self.player_sprite.vel / fps
        self.player_sprite.animation_speed = self.player_sprite.animation_vel / fps

    def update_fps(self, fps_counter):
        fps_count = str(fps_counter)
        fps_text = self.font.render(fps_count, 1, pygame.Color("coral"))
        self.display.blit(fps_text, (10, 10))

    def movement_and_collision(self):
        # apply vel to the player
        self.player_sprite.rect.x += self.player_sprite.direction.x * self.player_sprite.speed
        self.player_sprite.rect.y += self.player_sprite.direction.y * self.player_sprite.speed

        # wall collision
        if self.player_sprite.rect.left < 0:
            self.player_sprite.rect.left = 0
            self.player_sprite.moving = False
            self.player_sprite.direction.x = 0

            self.player_sprite.on_left = True
            self.current_x = self.player_sprite.rect.left

        elif self.player_sprite.rect.right > screen_width:
            self.player_sprite.rect.right = screen_width
            self.player_sprite.moving = False
            self.player_sprite.direction.x = 0

            self.player_sprite.on_right = True
            self.current_x = self.player_sprite.rect.right

        elif self.player_sprite.rect.top < 0:
            self.player_sprite.rect.top = 0
            self.player_sprite.moving = False
            self.player_sprite.direction.y = 0

            self.player_sprite.on_ceiling = True
            self.current_y = self.player_sprite.rect.top

        elif self.player_sprite.rect.bottom > screen_height:
            self.player_sprite.rect.bottom = screen_height
            self.player_sprite.moving = False
            self.player_sprite.direction.y = 0

            self.player_sprite.on_ground = True
            self.current_y = self.player_sprite.rect.bottom

        # tiles collision
        for sprite in self.collision_tiles.sprites():
            if sprite.rect.colliderect(self.player_sprite.rect):
                if self.player_sprite.direction.x < 0:
                    self.player_sprite.rect.left = sprite.rect.right
                    self.player_sprite.moving = False
                    self.player_sprite.direction.x = 0

                    self.player_sprite.on_left = True
                    self.current_x = self.player_sprite.rect.left

                elif self.player_sprite.direction.x > 0:
                    self.player_sprite.rect.right = sprite.rect.left
                    self.player_sprite.moving = False
                    self.player_sprite.direction.x = 0

                    self.player_sprite.on_right = True
                    self.current_x = self.player_sprite.rect.right

                if self.player_sprite.direction.y < 0:
                    self.player_sprite.rect.top = sprite.rect.bottom
                    self.player_sprite.moving = False
                    self.player_sprite.direction.y = 0

                    self.player_sprite.on_ceiling = True
                    self.current_y = self.player_sprite.rect.top

                if self.player_sprite.direction.y > 0:
                    self.player_sprite.rect.bottom = sprite.rect.top
                    self.player_sprite.moving = False
                    self.player_sprite.direction.y = 0

                    self.player_sprite.on_ground = True
                    self.current_y = self.player_sprite.rect.bottom

        # reset animations
        if self.player_sprite.on_left and (
                self.player_sprite.rect.left < self.current_x or self.player_sprite.direction != (0, 0)):
            self.player_sprite.on_left = False

        if self.player_sprite.on_right and (
                self.player_sprite.rect.right < self.current_x or self.player_sprite.direction != (0, 0)):
            self.player_sprite.on_right = False

        if self.player_sprite.on_ground and (
                self.player_sprite.rect.bottom < self.current_y or self.player_sprite.direction != (0, 0)):
            self.player_sprite.on_ground = False

        if self.player_sprite.on_ceiling and (
                self.player_sprite.rect.top < self.current_y or self.player_sprite.direction != (0, 0)):
            self.player_sprite.on_ceiling = False

    def kill_collision(self):
        for sprite in self.kill_tiles.sprites():
            if sprite.rect.colliderect(self.player_sprite.rect):
                self.state = 'select_level'

    def scores_collision(self):

        for sprite in self.scores_tiles.sprites():
            if self.player_sprite.rect.collidepoint(sprite.rect.center):
                sprite.kill()
                self.score += 1

    def teleport_collision(self):
        if self.teleport_list:
            i = 0
            for group in self.teleport_list:
                sprites = group.sprites()
                for index, sprite in enumerate(sprites):
                    if self.player_sprite.rect.collidepoint(sprite.rect.center):
                        if not self.teleporting:
                            self.player_sprite.rect.center = sprites[1 - index].rect.center
                            self.teleporting = True
                    else:
                        i += 1

            if i == len(self.teleport_list) * 2:
                self.teleporting = False

    def change_direction_collision(self):
        for sprite in self.change_direction.sprites():
            if self.player_sprite.rect.collidepoint(sprite.rect.center) and not self.changed_dir:
                dir_x, dir_y = self.player_sprite.direction.x, self.player_sprite.direction.y
                self.player_sprite.direction.x, self.player_sprite.direction.y = 0, 0
                self.player_sprite.moving = False
                self.player_sprite.get_input()

                if self.player_sprite.direction.x == 0 and self.player_sprite.direction.y == 0:
                    self.player_sprite.direction.x, self.player_sprite.direction.y = dir_x, dir_y

                else:
                    self.player_sprite.rect.center = sprite.rect.center
                    self.changed_dir_tile = sprite
                    self.changed_dir = True

        if self.changed_dir_tile:
            if not self.changed_dir_tile.rect.collidepoint(self.player_sprite.rect.center):
                self.changed_dir = False
                self.changed_dir_tile = None

    def display_score(self):
        label = self.font.render(str(self.score), 1, 'white')
        self.display.blit(label, (((screen_width - 10) / 2), 15))

    def teleport_draw(self):
        for group in self.teleport_list:
            group.update()
            group.draw(self.display)

    def reset_level(self):
        if len(self.scores_tiles.sprites()) == 0:
            self.state = 'select_level'

    def run(self, fps):
        # fps counter
        self.update_fps(fps)

        # image tiles
        self.images_tiles.update()
        self.images_tiles.draw(self.display)

        # collision tiles
        self.collision_tiles.update()
        self.collision_tiles.draw(self.display)

        # spikes
        self.kill_collision()
        self.kill_tiles.update()
        self.kill_tiles.draw(self.display)

        # teleport_tiles
        self.teleport_collision()
        self.teleport_draw()

        # scores_tiles
        self.scores_tiles.update()
        self.scores_tiles.draw(self.display)

        # change direction tiles
        self.change_direction_collision()
        self.change_direction.draw(self.display)

        # score
        self.scores_collision()
        self.display_score()
        self.reset_level()

        # player
        self.player_sprite.update()
        self.movement_and_collision()
        self.player.draw(self.display)

        return self.state

    def dumb(self):
        print(self.player.direction.x)
