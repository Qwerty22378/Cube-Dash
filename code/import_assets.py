from csv import reader
from os import walk

import pygame

from settings import tile_size


def import_folder(path):
    surface_list = []

    for _, __, img_files in walk(path):
        for image in img_files:
            full_path = path + '/' + image
            image_surf = pygame.image.load(full_path).convert_alpha()
            surface_list.append(image_surf)

    return surface_list


def import_csv_layout(path):
    map_list = []
    with open(path) as map_layout:
        level = reader(map_layout, delimiter=',')
        for row in level:
            map_list.append(list(row))

    return map_list


def import_cut_graphics(path):
    full_img = pygame.image.load(path).convert_alpha()

    tile_num_x = int(full_img.get_width() / tile_size)
    tile_num_y = int(full_img.get_height() / tile_size)

    img_list = []
    for row in range(tile_num_y):
        for col in range(tile_num_x):
            x = col * tile_size
            y = row * tile_size
            img_cut = pygame.Surface((tile_size, tile_size))
            img_cut.fill('cyan')
            img_cut.blit(full_img, (0, 0), pygame.Rect(x, y, tile_size, tile_size))
            img_list.append(img_cut)

    return img_list


def import_files_path(path):
    for _, __, files in walk(path):
        return files


#this is a test of the level_data git branch
