from turtle import update
import pygame
from settings import *
from support import import_folder
from tiles import StaticTile, animatedtile
from random import choice, randint
class sky:
    def __init__(self,horizon):
        self.verticle_tile_number = 11
        self.top = pygame.image.load('graphics/decoration/sky/sky_top.png').convert()
        self.middle = pygame.image.load('graphics/decoration/sky/sky_middle.png').convert()
        self.bottom = pygame.image.load('graphics/decoration/sky/sky_bottom.png').convert()
        self.horion = horizon

        # strech
        self.top = pygame.transform.scale(self.top,(screen_width,tile_size))
        self.middle = pygame.transform.scale(self.middle,(screen_width,tile_size))
        self.bottom = pygame.transform.scale(self.bottom,(screen_width,tile_size))
        

    def draw(self,surface):
        for row  in range(self.verticle_tile_number):
            y = row * tile_size
            if row < self.horion:
                surface.blit(self.top,(0,y))
            elif row == self.horion:
                surface.blit(self.middle,(0,y))
            else:
                surface.blit(self.bottom,(0,y))


class water:
    def __init__(self,top,level_width):
        water_start = -screen_width
        water_tile_width = 192
        tile_x_amount = int((level_width + screen_width * 2) / water_tile_width)
        self.water_sprites = pygame.sprite.Group()

        for tile  in range(tile_x_amount):
            x = tile * water_tile_width + water_start
            y = top
            sprtie = animatedtile(192,x,y,'graphics/decoration/water')
            self.water_sprites.add(sprtie)

    def draw(slef,surface,shift):
        slef.water_sprites.update(shift)
        slef.water_sprites.draw(surface)

class cloud:
    def __init__(self,horizon,level_width,cloud_number):
        cloud_surf_list = import_folder('graphics/decoration/clouds')
        min_x = -screen_width
        max_x = level_width + screen_width
        min_y = 0
        max_y = horizon
        self.cloud_sprites = pygame.sprite.Group()

        for cloud in range(cloud_number):
            cloud = choice(cloud_surf_list)
            x = randint(min_x,max_x)
            y = randint(min_y,max_y)
            sprite = StaticTile(0,x,y,cloud)
            self.cloud_sprites.add(sprite)

    def draw(self,surface,shift):
        self.cloud_sprites.update(shift)
        self.cloud_sprites.draw(surface)


        


        