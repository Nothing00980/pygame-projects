# basic pygame setup
import pygame,sys
from settings import *
from tiles import Tile
from level import Level
from settings import level_0


pygame.init()

screen = pygame.display.set_mode((screen_width,screen_height))
clock = pygame.time.Clock()
# test_tile = pygame.sprite.Group(Tile((100,100),200)) -- to make a tile and giving diemnsion and position
level = Level(level_0,screen)




while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            
            pygame.quit()
            sys.exit()
    screen.fill('lightblue')  #we can give color like this also
    # test_tile.draw(screen) -- putting on the screen
    level.run()

    pygame.display.update()
    clock.tick(60)
