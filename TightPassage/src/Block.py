import os
import random
import pygame
import src.Const as Const
import src.Interactables.Interactable as Interactable

class Block(Interactable.Interactable):
    """Something to run head-first into."""
    #Alpha-Image for sprite
    SHADE_MASK = None

    def __init__(self,location):
        
        if(type(self).SHADE_MASK == None):
            #convert_alpha since since the block will be shaded with color later
            type(self).SHADE_MASK = pygame.image.load(os.path.join("assets","sprites","shader.png")).convert_alpha()
        self.image = self.make_image()
        rect = self.image.get_rect(topleft=location)
        rect.move(location)
        super().__init__(rect,pygame.K_RIGHT)

    def make_image(self):
        """create random colored block"""
        image = pygame.Surface((50,50)).convert_alpha()
        image.fill([random.randint(0, 255) for _ in range(3)])
        image.blit(type(self).SHADE_MASK, (0,0))
        return image