import os
import pygame
import src.Const as Const
import src.Support as Support
import src.Interactables.Interactable
from src.Interactables.Interactable import Interactable
import src.Components.ComponentGraphics
from src.Components.ComponentGraphics import UnitGraphics
from src.GameState import GameState

class Warp(Interactable):
    """ a trigger to move the player to a different loaction f.e. a door or teleporter
    """
    def __init__(self,rect):
        self.map = None
        self.target = None
        super().__init__(rect,pygame.K_RIGHT)
        self.image = pygame.Surface((rect.width,rect.height),pygame.SRCALPHA)
        self.hitrect = rect
        self.hitrect.center = self.rect.center
        self.triggered=False
        self.firstPassDone = False

    def setTarget(self,map,target):
        self.map = map
        self.target = target

    def update(self):
        state=GameState()
        if(not state.inGame or self.triggered):
            return
        if(pygame.sprite.collide_rect(self,state.player)):
            #if teleporting from warpA to warpB this would trigger collision again immediatly
            #- have to wait until player moves away from trigger
            if(self.firstPassDone):
                self.notifyOnHit(state.player)
                self.triggered=True
        else:
            self.firstPassDone=True
