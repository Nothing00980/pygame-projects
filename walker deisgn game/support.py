from os import walk
import pygame
from csv import reader
from settings import tilesize

# converting the csv layout format to a list.
def import_csv_layout(path):
    terrain_map = []
    with open(path) as map:
        level = reader(map,delimiter=",")
        for row in level:
            terrain_map.append(list(row))
        return terrain_map


def import_cut_graphic(path):
    surface = pygame.image.load(path).convert_alpha()
    tile_num_x = int(surface.get_size()[0]/tilesize)
    tile_num_y = int(surface.get_size()[1]/tilesize)

    cuttiles = []
    for row in range(tile_num_y):
        for col in range(tile_num_x):
            x = col * tilesize
            y = row*tilesize
            new_surface = pygame.Surface((tilesize,tilesize),flags=pygame.SRCALPHA)
            new_surface.blit(surface,(0,0),pygame.Rect(x,y,tilesize,tilesize))
            cuttiles.append(new_surface)

    return cuttiles

def import_folder(path):
    surfacelist =[]

    for _,__,img_files in walk(path):
        for image in img_files:
            full_path = path + "/" + image
            image_surface = pygame.image.load(full_path).convert_alpha()
            surfacelist.append(image_surface)

    return surfacelist
