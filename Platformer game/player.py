import pygame
from support import import_folder

class player(pygame.sprite.Sprite):
    def __init__(s,pos,surface,create_jump_particles):
        super().__init__()
        s.import_character_assets()
        s.frame_index = 0
        s.animation_speed = 0.15
        # the real animations
        s.image = s.animations['idle'][s.frame_index]
        s.rect = s.image.get_rect(topleft = pos)


        # these are just a square block animations
        # s.image = pygame.Surface((32,64))
        # s.image.fill('red')


        # dust particles
        s.import_dust_run_particles()
        s.dustframe_index = 0
        s.dustanimation_speed = 0.15
        s.display_surface = surface
        s.create_jump_particles = create_jump_particles


        # player movement
        s.direction = pygame.math.Vector2(0,0)  #we can make the player move in both the direction simulatenously
        s.gravity = 0.8
        s.jump_speed = -16
        s.speed = 8
        # player status
        s.status = 'idle'
        s.facing_right = True
        
        # to place the rect properly
        s.on_ground = False
        s.on_ceiling  = False
        s.on_left = False
        s.on_right = False
    def import_character_assets(self):
        character_path = 'graphics/character/'
        # creating a dictionary
        self.animations = { 'idle':[],'run':[],'jump':[],'fall':[]}

        for animations in self.animations.keys():
            full_path = character_path + animations
            self.animations[animations] = import_folder(full_path)


    def import_dust_run_particles(self):
        self.dust_run_particles = import_folder('graphics/character/dust_particles/run')
    def animate(self):
        animation = self.animations[self.status]
        # loop over the frame index
        self.frame_index += self.animation_speed
        if self.frame_index >= len(animation):
            self.frame_index = 0
        self.image = animation[int(self.frame_index)] 
        image  = animation[int(self.frame_index)]
        # right and left facing of the character
        if self.facing_right:
            self.image  = image
        else:
            flipped_image = pygame.transform.flip(image,True,False)
            self.image = flipped_image

        # setting the rect
        if self.on_ground and self.on_right:
            self.rect = self.image.get_rect(bottomright = self.rect.bottomright)
        elif self.on_ground and self.on_left:
            self.rect = self.image.get_rect(bottomleft = self.rect.bottomleft)
        elif self.on_ground:
            self.rect = self.image.get_rect(midbottom = self.rect.midbottom)
        elif self.on_ceiling and self.on_right:
            self.rect = self.image.get_rect(topright = self.rect.topright)
        elif self.on_ceiling and self.on_left:
            self.rect = self.image.get_rect(topleft = self.rect.topleft)
        elif self.on_ceiling:
            self.rect = self.image.get_rect(midtop = self.rect.midtop)


    def run_dust_animation(self):
        if self.status == 'run' and self.on_ground:
            self.dustframe_index += self.dustanimation_speed
            if self.dustframe_index >= len(self.dust_run_particles):
                self.dustframe_index = 0
            
            dust_particle = self.dust_run_particles[int(self.dustframe_index)]
            # running particle
            if self.facing_right:
                pos = self.rect.bottomleft - pygame.math.Vector2(6,10)
                self.display_surface.blit(dust_particle,pos)
            else:
                pos = self.rect.bottomright - pygame.math.Vector2(6,10)
                flipped_dust_particle = pygame.transform.flip(dust_particle,True,False)
                self.display_surface.blit(flipped_dust_particle,pos)

      






    def get_input(self):
        keys = pygame.key.get_pressed()

        if keys[pygame.K_RIGHT]:
            self.direction.x = 1
            self.facing_right = True
        elif keys[pygame.K_LEFT]:
            self.direction.x = -1
            self.facing_right = False
            
        else:
            self.direction.x = 0
        
        if keys[pygame.K_SPACE] and self.on_ground:
            self.jump()
            self.create_jump_particles(self.rect.midbottom)
                

    def get_status(self):
        if self.direction.y <0:
            self.status = 'jump'
        elif self.direction.y >1 :
            self.status = 'fall'
        else:
            if self.direction.x !=0:
                self.status = 'run'
            else:
                self.status = 'idle'

    def apply_gravity(self):
        self.direction.y += self.gravity
        self.rect.y += self.direction.y

    def jump(slef):
        slef.direction.y =slef.jump_speed
        



    def update(self):
        self.get_input()
        self.get_status()
        self.animate()
        self.run_dust_animation()
        