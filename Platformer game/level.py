import pygame
from enemy import Enemy
from particles import ParticleEffect
from tiles import *
from settings import tile_size
from player import *
from settings import screen_width,screen_height
from support import import_csv_layout,import_cut_graphic
from decoration import cloud, sky,water
class Level:
    def __init__(self,level_data,surface):
        # level setup
        self.display_surface = surface
        # self.setup_level(level_data)
        self.world_shift = 0
        self.current_x = None

        # player
        player_layout = import_csv_layout(level_data['player'])
        self.player = pygame.sprite.GroupSingle()
        self.goal = pygame.sprite.GroupSingle()
        self.setup_player(player_layout)

        # dust
        self.dust_sprite = pygame.sprite.GroupSingle()
        self.player_on_ground = False

        # layout 
        # terrain setup
        terrain_layout =import_csv_layout(level_data['terrain'])
        # print(terrain_layout)
        self.terrain_sprites = self.create_tile_group(terrain_layout,'terrain')

        # grass layout
        grass_layout = import_csv_layout(level_data['grass'])
        self.grass_sprites = self.create_tile_group(grass_layout,'grass')

        # crates
        crate_layout = import_csv_layout(level_data['crates'])
        self.crates_sprites = self.create_tile_group(crate_layout,'crates')

        # coins
        coins_layout = import_csv_layout(level_data['coins'])
        self.coins_sprites = self.create_tile_group(coins_layout,'coins')

        # palms
        palms_layout = import_csv_layout(level_data['palms'])
        self.palms_sprites = self.create_tile_group(palms_layout,'palms')
        # bg_palms
        bg_palms_layout = import_csv_layout(level_data['bg_palms'])
        self.bg_palms_sprites = self.create_tile_group(bg_palms_layout,'bg_palms')
        # enemy
        enemy_layout = import_csv_layout(level_data['enemy'])
        self.enemy_sprites = self.create_tile_group(enemy_layout,'enemy')
        # enemy_restraints
        constraint_layout = import_csv_layout(level_data['enemy_constraints'])
        self.constraint_sprites = self.create_tile_group(constraint_layout,'enemy_constraints')

        # sky
        self.sky = sky(8)

        # Water
        level_width = len(terrain_layout[0]) * tile_size
        self.water = water(screen_height - 20,level_width)

        # clouds
        self.clouds = cloud(400,level_width,30)



        


    def setup_player(self,layout):
        for row_index,row in enumerate(layout):
            for col_index,val in enumerate(row):
                x = col_index*tile_size
                y  =row_index * tile_size

                if val == '0':
                    sprite = player((x,y),self.display_surface,self.create_jump_particles)
                    self.player.add(sprite)
                    # play = player((x,y),self.display_surface,self.create_jump_particles)
                    # self.player.add(play)

                if val == '1':
                    hat_surface = pygame.image.load('graphics/character/hat.png').convert_alpha()
                    sprtie = StaticTile(tile_size,x,y,hat_surface)
                    self.goal.add(sprtie)





    def create_tile_group(s,layout,type):
        sprite_group = pygame.sprite.Group()

        for row_index,row in enumerate(layout):
            for col_index,val in enumerate(row):
                # print(row)
                if val != '-1':
                    # print(val)
                    x = col_index*tile_size
                    y  =row_index * tile_size
                    if type == 'terrain':
                        terrain_tile_list = import_cut_graphic('graphics/terrain/terrain_tiles.png')
                        tile_surface = terrain_tile_list[int(val)]
                        sprite = StaticTile(tile_size,x,y,tile_surface)
                    if type == "grass":
                        grass_tile_list = import_cut_graphic('graphics/decoration/grass/grass.png')
                        tile_surface = grass_tile_list[int(val)]
                        sprite = StaticTile(tile_size,x,y,tile_surface)
                    if type == "crates":
                        sprite = Crate(tile_size,x,y)
                    if type == 'coins':
                        if val == '0':
                            sprite = Coin(tile_size,x,y,'graphics/coins/gold')
                        if val == '1':
                            sprite = Coin(tile_size,x,y,'graphics/coins/silver')
                    if type == 'palms':
                        if val == '0':
                            sprite = Palm(tile_size,x,y,'graphics/terrain/palm_small',36)
                        if val== '1':
                            sprite = Palm(tile_size,x,y,'graphics/terrain/palm_large',70)
                    if type == 'bg_palms':
                        sprite  = Palm(tile_size,x,y,'graphics/terrain/palm_bg',64)

                    if type == 'enemy':
                        sprite = Enemy(tile_size,x,y)
                    if type == 'enemy_constraints':
                        sprite = Tile(tile_size,x,y)



                        
                        
                    sprite_group.add(sprite)

        return sprite_group

    def enemy_collision_reverse(self):
        for enemy in self.enemy_sprites.sprites():
            if pygame.sprite.spritecollide(enemy,self.constraint_sprites,False):
                enemy.reverse()




    
    def create_jump_particles(s,pos):
        if s.player.sprite.facing_right:
            pos -= pygame.math.Vector2(10,5)
        else:
            pos += pygame.math.Vector2(10,-5)
        jump_paricle_sprite = ParticleEffect(pos,'jump')
        s.dust_sprite.add(jump_paricle_sprite)

    def get_player_onground(s):
        if s.player.sprite.on_ground:
            s.player_on_ground = True
        else:
            s.player_on_ground = False

    def create_landing_particles(s):
        if not s.player_on_ground and s.player.sprite.on_ground and not s.dust_sprite.sprites():
            if s.player.sprite.facing_right:
                offset = pygame.math.Vector2(10,15)
            else:
                offset = pygame.math.Vector2(-10,15)


            fall_dust_prticles = ParticleEffect(s.player.sprite.rect.midbottom - offset,'land')
            s.dust_sprite.add(fall_dust_prticles)

    # def setup_level(self,layout):
    #     self.tiles = pygame.sprite.Group()
    #     self.player = pygame.sprite.GroupSingle()
    #     for row_index,row in enumerate(layout): # enumerate gives the index or the postion and also the data
    #         # print(row)
    #         # print(row_index)
    #         for col_index,col in enumerate(row):
    #             # print(f'{row_index}{col_index}:{col}')
    #             x = col_index*tile_size
    #             y = row_index*tile_size
    #             if col == 'x':
    #                 tile = Tile((x,y),tile_size)
    #                 self.tiles.add(tile)
    #             if col == "P":
    #                 play = player((x,y),self.display_surface,self.create_jump_particles)
    #                 self.player.add(play)
    
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

        collidable_sprites = self.terrain_sprites.sprites() + self.crates_sprites.sprites() + self.palms_sprites.sprites()
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
        

        collidable_sprites = self.terrain_sprites.sprites() + self.crates_sprites.sprites() + self.palms_sprites.sprites()
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




            


    def run(self):
        # the higher the funtion the more in background


        
        # decorations
        self.sky.draw(self.display_surface)
        self.clouds.draw(self.display_surface,self.world_shift)
        # dust particle
        self.dust_sprite.update(self.world_shift)
        self.dust_sprite.draw(self.display_surface)

        # tiles or the background
        self.terrain_sprites.draw(self.display_surface)
        self.terrain_sprites.update(self.world_shift)
        # self.tiles.draw(self.display_surface)
        # self.tiles.update(self.world_shift)
        # bg palms
        self.bg_palms_sprites.update(self.world_shift)
        self.bg_palms_sprites.draw(self.display_surface)

        # grass
        self.grass_sprites.update(self.world_shift)
        self.grass_sprites.draw(self.display_surface)

        # crate
        self.crates_sprites.update(self.world_shift)
        self.crates_sprites.draw(self.display_surface)

        # coins
        self.coins_sprites.update(self.world_shift)
        self.coins_sprites.draw(self.display_surface)

        # palms
        self.palms_sprites.update(self.world_shift)
        self.palms_sprites.draw(self.display_surface)

        # enemy
        self.enemy_sprites.update(self.world_shift)
        self.enemy_sprites.draw(self.display_surface)

        # constraints
        self.constraint_sprites.update(self.world_shift)
        # self.constraints_sprites.draw(self.display_surface) not drawing but they do exist
        self.enemy_collision_reverse()

        # player sprites
        self.goal.update(self.world_shift)
        self.goal.draw(self.display_surface)

        # water 
        self.water.draw(self.display_surface,self.world_shift)




        # player
        self.player.update()
        self.horizontal_movement_collision()
        self.get_player_onground()
        self.vertical_movement_collision()
        self.create_landing_particles()
        self.player.draw(self.display_surface)
        # # camera operation on the player
        self.scroll_x()


        # # collision with objects
