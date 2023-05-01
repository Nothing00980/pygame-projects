from os import walk #system funcctionality
import pygame
# for layouts
from csv import reader
from settings import tile_size


def import_csv_layout(path):
    terrain_map  = []
    with open(path) as map:
        level = reader(map,delimiter=',')
        for row in level:
            # print(row)
            terrain_map.append(list(row))
        return terrain_map

def import_cut_graphic(path):
    surface = pygame.image.load(path).convert_alpha()
    tile_num_x = int(surface.get_size()[0] / tile_size)
    tile_num_y = int(surface.get_size()[1] / tile_size)

    cut_tiles = []
    for row in range(tile_num_y):
        for col in range(tile_num_x):
            x = col * tile_size
            y = row * tile_size
            new_surface = pygame.Surface((tile_size,tile_size),flags=pygame.SRCALPHA)
            new_surface.blit(surface,(0,0),pygame.Rect(x,y,tile_size,tile_size))
            cut_tiles.append(new_surface)

    return cut_tiles

            






def import_folder(path):
    surface_list = []

    for _,__,img_files in walk(path):  #putting all the animations in a surface of list
        for image in img_files:
            full_path = path + "/"+ image
            image_surface = pygame.image.load(full_path).convert_alpha()
            surface_list.append(image_surface)

    return surface_list
        # print(information)





# import_folder('graphics/character/run')
    