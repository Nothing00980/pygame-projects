# basic libararies

import pygame,sys
from settings import * 
from level import *
from tiles import Tile
from settings import level_0




pygame.init()

screen = pygame.display.set_mode((screen_width,screen_height))
clock = pygame.time.Clock()
level = Level(level_0,screen)



# working

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:

            pygame.quit()
            sys.exit()
        screen.fill('lightblue')
        level.run()



    pygame.display.update()
    clock.tick(60)