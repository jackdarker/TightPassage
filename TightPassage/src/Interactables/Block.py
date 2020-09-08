import os
import random
import pygame
import src.Const as Const
import src.Support as Support
import src.Interactables.Interactable
from src.Interactables.Interactable import Interactable

class Block(Interactable):
    """Something to run head-first into."""
    #Alpha-Image for sprite
    SHADE_MASK = None

    def __init__(self,rect):
        
        if(type(self).SHADE_MASK == None):
            #convert_alpha since since the block will be shaded with color later
            type(self).SHADE_MASK = pygame.image.load(Const.resource_path("assets/sprites/shader.png")).convert_alpha()
        image = self.make_image(rect)
        rect = image.get_rect(topleft=rect.topleft)
        rect.move(rect.topleft)
        super().__init__(rect,pygame.K_RIGHT)
        self.image = image

    def make_image(self,rect):
        """create random colored block"""
        image = pygame.Surface(rect.size).convert_alpha()   #todo image size from leveldata
        image.fill([random.randint(0, 255) for _ in range(3)])
        image.blit(type(self).SHADE_MASK, (0,0))
        return image