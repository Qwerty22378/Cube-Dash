import pygame
from pygame.locals import *

from import_assets import import_folder
from settings import on_pc


class Player(pygame.sprite.Sprite):
    def __init__(self, pos):
        super().__init__()
        self.import_character_assets()
        self.frame_index = 0
        self.animation_vel = 9
        self.animation_speed = 0
        self.image = self.animations['idle'][self.frame_index]
        self.rect = self.image.get_rect(topleft=pos)

        # player movement
        self.moving = False
        self.speed = 0
        self.vel = 480
        self.direction = pygame.math.Vector2(0, 0)

        # player status
        self.status = 'idle'
        self.on_ground = True
        self.on_ceiling = False
        self.on_left = False
        self.on_right = False
        self.facing_right = True

    def import_character_assets(self):
        character_path = "..//graphics//character//"
        self.animations = {'idle': [], 'run': [], 'jump': [], 'fall': [], 'hanging_side': [], 'hanging_top': []}

        for animation in self.animations.keys():
            full_path = character_path + animation
            self.animations[animation] = import_folder(full_path)

    def animate(self):
        # set status
        if self.on_ceiling:
            self.status = 'hanging_top'
        elif self.on_right or self.on_left:
            self.status = 'hanging_side'
        elif self.direction.x:
            self.status = 'run'
        elif self.direction.y:
            if self.direction.y < 0:
                self.status = 'jump'
            else:
                self.status = 'fall'
        else:
            self.status = 'idle'

        animation = self.animations[self.status]

        # loop over frame index
        self.frame_index += self.animation_speed
        if self.frame_index >= len(animation):
            self.frame_index = 0

        image = animation[int(self.frame_index)]
        if self.facing_right:
            self.image = image
        else:
            flipped_image = pygame.transform.flip(image, True, False)
            self.image = flipped_image

        # set the rect
        if self.on_ground and self.on_right:
            self.rect = self.image.get_rect(bottomright=self.rect.bottomright)
        elif self.on_ground and self.on_left:
            self.rect = self.image.get_rect(bottomleft=self.rect.bottomleft)
        elif self.on_ground:
            self.rect = self.image.get_rect(midbottom=self.rect.midbottom)
        elif self.on_ceiling and self.on_right:
            self.rect = self.image.get_rect(topright=self.rect.topright)
        elif self.on_ceiling and self.on_left:
            self.rect = self.image.get_rect(topleft=self.rect.topleft)
        elif self.on_ceiling:
            self.rect = self.image.get_rect(midtop=self.rect.midtop)

    def get_input(self):
        if on_pc:
            keys = pygame.key.get_pressed()

            if keys[K_d] and not self.moving:
                self.direction.x = 1
                self.moving = True
                self.facing_right = True
            elif keys[K_a] and not self.moving:
                self.direction.x = -1
                self.moving = True
                self.facing_right = False
            elif keys[K_w] and not self.moving:
                self.direction.y = -1
                self.moving = True
            elif keys[K_s] and not self.moving:
                self.direction.y = 1
                self.moving = True
        else:
            keys = pygame.mouse.get_pressed()
            mouse_rel = pygame.mouse.get_rel()
            if keys[0]:
                if abs(mouse_rel[0]) > abs(mouse_rel[1]):
                    if mouse_rel[0] > 0 and not self.moving:
                        self.direction.x = 1
                        self.moving = True
                        self.facing_right = True
                    elif mouse_rel[0] < 0 and not self.moving:
                        self.direction.x = -1
                        self.moving = True
                        self.facing_right = False
                else:
                    if mouse_rel[1] < 0 and not self.moving:
                        self.direction.y = -1
                        self.moving = True
                    elif mouse_rel[1] > 0 and not self.moving:
                        self.direction.y = 1
                        self.moving = True

    def update(self):
        self.get_input()
        self.animate()
