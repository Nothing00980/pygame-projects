import fractions
import imp
import pygame
from support import import_folder

class Tile(pygame.sprite.Sprite):
    def __init__(self,size,x,y):
        super().__init__()
        self.image = pygame.Surface((size,size))
        # self.image.fill('grey')
        self.rect = self.image.get_rect( topleft = (x,y))

    def update(self,x_shift): # scrolling in x direction
        self.rect.x += x_shift

class StaticTile(Tile):
    def __init__(s,size,x,y,surface):
        super().__init__(size,x,y)
        s.image = surface

# we did this because size of tile and crate are not same
class Crate(StaticTile):
    def __init__(self,size,x,y):
        super().__init__(size,x,y,pygame.image.load('graphics/terrain/crate.png').convert_alpha())
        offset_y = y + size
        self.rect = self.image.get_rect(bottomleft = (x,offset_y))

class animatedtile(Tile):
    def __init__(self,size,x,y,path):
        super().__init__(size,x,y)
        self.frames = import_folder(path)
        self.frame_index = 0
        self.image = self.frames[self.frame_index]


    def animate(s):
        s.frame_index +=0.15
        if s.frame_index >=len(s.frames):
            s.frame_index = 0
        s.image = s.frames[int(s.frame_index)]

    def update(s,shift):
        s.animate()
        s.rect.x += shift

class Coin(animatedtile):
    def __init__(self,size,x,y,path):
        super().__init__(size,x,y,path)
        center_x = x + int(size/2)
        cetner_y = y + int(size/2)
        self.rect = self.image.get_rect(center = (center_x,cetner_y))

class Palm(animatedtile):
    def __init__(self, size, x, y, path,offset):
        super().__init__(size, x, y, path)
        offset_y = y - offset
        self.rect.topleft = (x,offset_y)









