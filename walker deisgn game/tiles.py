import pygame
from support import *


class Tile(pygame.sprite.Sprite):
    def __init__(self,size,x,y):
        super().__init__()
        self.image = pygame.Surface((size,size))
        self.rect = self.image.get_rect( topleft = (x,y))


    def update(self,x_shift):
        self.rect.x += x_shift

class StaticTile(Tile):
    def __init__(self, size, x, y,surface):
        super().__init__(size, x, y)
        self.image = surface


class animatedtile(Tile):
    def __init__(self, size, x, y,path):
        super().__init__(size, x, y)
        self.frames = import_folder(path)
        self.frame_index = 0
        self.image = self.frames[self.frame_index]



    def animate(s):
        s.frame_index +=0.15
        if s.frame_index >=len(s.frames):
            s.frame_index = 0
        s.image = s.frames[int(s.frame_index)]
    def update(self, shift):
        self.animate()
        self.rect.x += shift