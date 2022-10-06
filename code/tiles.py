import pygame


class Tile(pygame.sprite.Sprite):
    def __init__(self, pos, size):
        super().__init__()
        self.image = pygame.Surface(size)
        self.rect = self.image.get_rect(topleft=pos)


class StaticTile(Tile):
    def __init__(self, pos, size, img):
        super().__init__(pos, size)
        self.image = img


class AnimatedTile(Tile):
    def __init__(self, pos, size, img_list):
        super().__init__(pos, size)
        self.img_list = img_list
        self.frame_index = 0
        self.animation_speed = 0.05
        self.image = self.img_list[self.frame_index]

    def animate(self):
        self.frame_index += self.animation_speed

        if self.frame_index >= len(self.img_list):
            self.frame_index = 0

        self.image = self.img_list[int(self.frame_index)]

    def update(self):
        self.animate()


class ButtonTile(Tile):
    def __init__(self, pos, size, img_list, type):
        super().__init__(pos, size)
        self.img_list = img_list
        self.image = self.img_list[0]
        self.type= type


class LevelButtonTile(Tile):
    def __init__(self, pos, size, img_list, label_text, type):
        super().__init__(pos, size)
        self.img_list = img_list
        self.image = self.img_list[0]
        self.type = type
        self.add_label(label_text)

    def add_label(self, label_text):
        font = pygame.font.SysFont('Arial', int(self.rect.size[1] / 2))
        label = font.render(label_text, 1, 'black')

        for img in self.img_list:
            img.blit(label, (0, 0))

    def update(self, shift):
        self.rect.y += shift

