import pygame
from tiles import *
from settings import *
from support import *
from player import *

class Level:
    def __init__(self,leveldata,surface):
        self.display_surface = surface
        self.world_shift = 0
        self.current_x = None

# player layout
        player_layout  = import_csv_layout(leveldata['player'])
        self.player = pygame.sprite.GroupSingle()
        self.goal = pygame.sprite.GroupSingle()
        self.setup_player(player_layout)


        # terrain layout
        terrain_layout = import_csv_layout(leveldata['terrain'])
        self.terrain_sprites = self.create_tile_group(terrain_layout,'terrain')

    def setup_player(s,layout):
        for row_index,row in enumerate(layout):
            for col_index,val in enumerate(row):
                x = col_index * tilesize
                y = row_index * tilesize

                if val =='0':
                    sprite  = Player((x,y),s.display_surface)
                    s.player.add(sprite)

                if val == '1':
                    hat_surface = pygame.image.load('resources/character/hat.png').convert_alpha()
                    sprtie = StaticTile(tilesize,x,y,hat_surface)
                    s.goal.add(sprtie)



    def create_tile_group(s,layout,type):
        sp_group = pygame.sprite.Group()

        for r_i,row in enumerate(layout):
            for c_i,val in enumerate(row):
                if val!= '-1':
                    x = c_i * tilesize
                    y = r_i * tilesize

                    if type == "terrain":
                        terrain_tile_list = import_cut_graphic('resources/terrain/terrain_tiles.png')
                        tile_surface = terrain_tile_list[int(val)]
                        sprite = StaticTile(tilesize,x,y,tile_surface)
                    
                    sp_group.add(sprite)

        return sp_group

    def get_player_onground(s):
        if s.player.sprite.on_ground:
            s.player_on_ground = True
        else:
            s.player_on_ground = False

    def scroll_x(self):  #camera moving function
        player = self.player.sprite
        player_x = player.rect.centerx
        direction_x = player.direction.x

        if player_x < screen_width/4 and direction_x<0:
            self.world_shift = 8
            player.speed = 0
        elif player_x >screen_width - (screen_width/4) and direction_x>0:
            self.world_shift = -8
            player.speed = 0
        else:
            self.world_shift = 0
            player.speed = 8
    


    def horizontal_movement_collision(self):
        player = self.player.sprite
        player.rect.x += player.direction.x *player.speed

        collidable_sprites = self.terrain_sprites.sprites() 
        for sprite in collidable_sprites:
            if sprite.rect.colliderect(player.rect):
                if player.direction.x <0:
                    player.rect.left = sprite.rect.right
                    player.on_left = True
                    # storing position of the collision
                    self.current_x = player.rect.left
                elif player.direction.x>0:
                    player.rect.right = sprite.rect.left
                    player.on_right = True
                    self.current_x = player.rect.right

        if player.on_left and (player.rect.left < self.current_x or player.direction.x>=0):
            player.on_left = False
            
        if player.on_right and (player.rect.right > self.current_x or player.direction.x<=0):
            player.on_right = False
        

    def vertical_movement_collision(self):
        player = self.player.sprite
        player.apply_gravity()
        

        collidable_sprites = self.terrain_sprites.sprites() 
        for sprite in collidable_sprites:
            if sprite.rect.colliderect(player.rect):
                if player.direction.y >0:
                    player.rect.bottom = sprite.rect.top
                    player.direction.y = 0
                    player.on_ground = True
                elif player.direction.y<0:
                    player.rect.top = sprite.rect.bottom
                    player.direction.y = 0
                    player.on_ceiling = True

# if player is jumping or falling then it is not on the ground
        if player.on_ground and player.direction.y < 0 or player.direction.y >1:
            player.on_ground = False
        if player.on_ceiling and player.direction.y>0:
            player.on_ceiling = False


    def run(s):
    # tiles or the background
        s.terrain_sprites.draw(s.display_surface)
        s.terrain_sprites.update(s.world_shift)

    # player sprites
        s.goal.update(s.world_shift)
        s.goal.draw(s.display_surface)
     # player
        s.player.update()
        s.horizontal_movement_collision()
        s.get_player_onground()
        s.vertical_movement_collision()
        # s.create_landing_particles()
        s.player.draw(s.display_surface)
        # # camera operation on the player
        s.scroll_x()
