import pygame
import src.Const as Const
import src.Support as Support
from src.Vector import Vector2
from src.Interactables.Interactable import Interactable
from src.Components.ComponentGraphics import ComponentGraphics,AnimData

class Chest(Interactable):
    SPRITEIMAGE = None

    def __init__(self, rect, direction=Vector2(1,0)):
        _rect = pygame.Rect((rect[0],rect[1]), (32,32)) #imagesize !
        super().__init__(_rect,direction)
        self.hitrect = _rect
        self.hitrect.center = self.rect.center
        self.acceptInteract = True
        pass

    def update(self,dt):
        pass

    def draw(self, surface):
        """draws the image"""
        if(self.image!=None):
            surface.blit(self.image,(0,0))

    def postInteraction(self):
        self.acceptInteract = False
        pass