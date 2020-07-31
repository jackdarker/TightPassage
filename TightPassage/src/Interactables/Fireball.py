import os
import pygame
import src.Const as Const
import src.Interactables.Interactable as Interactable

class Fireball(Interactable.Interactable):
    #spritemap of the unit
    SPRITEIMAGE = None
    def __init__(self, creator, speed, direction=pygame.K_RIGHT):
        """
        Arguments are a rect representing the Player's location and
        dimension, the speed(in pixels/frame) of the Player, and the Player's
        starting direction (given as a key-constant).
        """
        rect = creator.rect
        super().__init__(rect,direction)
        
        hit_size = int(0.6*self.rect.width), int(0.4*self.rect.height)
        self.hitrect = pygame.Rect((0,0), hit_size)
        self.hitrect.midbottom = self.rect.midbottom
        self.speed = speed
        self.parent = creator

        if(type(self).SPRITEIMAGE == None):
            type(self).SPRITEIMAGE = pygame.Surface((30,30)).convert_alpha()
            type(self).SPRITEIMAGE.fill((100,0,0))
        self.redraw = False  #Force redraw if needed.
        self.image = type(self).SPRITEIMAGE

    def draw(self, surface):
        """Draw method seperated out from update."""
        surface.blit(self.image, self.rect)

    def update(self, obstacles):
        """Adjust the image and move as needed."""

        self.movement(obstacles, 0)
        self.movement(obstacles, 1)

    def movement(self, obstacles, i):
        """Move player and then check for collisions; adjust as necessary.
        i =0 is x; i=1 is y 
        """
        direction_vector = Interactable.Interactable.DIRECT_DICT[self.direction]
        self.hitrect[i] += self.speed*direction_vector[i]
        callback = self.collide_other(self.hitrect)  #Collidable callback created.
        collisions = pygame.sprite.spritecollide(self, obstacles, False, callback)
        while collisions:
            collision = collisions.pop()
            self.notifyOnHit(collision)
        self.rect.midbottom = self.hitrect.midbottom