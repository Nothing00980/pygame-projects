import pygame
from support import import_folder

class ParticleEffect(pygame.sprite.Sprite):
    def __init__(self,pos,type):
        super().__init__()
        self.frame_index = 0
        self.animation_speed  = 0.5
        if type == 'jump':
            self.frames = import_folder('graphics/character/dust_particles/jump')
        if type == 'land':
            self.frames = import_folder('graphics/character/dust_particles/land')
        self.image  = self.frames[self.frame_index]
        self.rect = self.image.get_rect(center = pos)

    def animate(s):
        s.frame_index += s.animation_speed
        if s.frame_index >= len(s.frames):
            s.kill()  #we are disposing off the particle as long as the animation end
        else:
            s.image = s.frames[int(s.frame_index)]


    def update(s,x_shift):
        s.animate()
        s.rect.x += x_shift



