import os
import pygame
import src.Const as Const
import src.Support as Support
import src.Interactables.Interactable
from src.Interactables.Interactable import Interactable
import src.Components.ComponentGraphics
from src.Components.ComponentGraphics import UnitGraphics
from src.GameState import GameState


class Trigger(Interactable):
    """ a trigger to start something
    CB_onEnter is a function func(triggerSource) called when triggersource enters the hitrect
    """
    def __init__(self,rect, #triggerSource, 
                 CB_onEnter = None, CB_onExit = None, **params):
        #self.triggerSource = triggerSource
        self.CB_onEnter = CB_onEnter
        self.CB_onExit = CB_onExit
        self.params = params

        super().__init__(rect,pygame.K_RIGHT)
        self.image = pygame.Surface((rect.width,rect.height),pygame.SRCALPHA)
        self.hitrect = rect
        self.hitrect.center = self.rect.center
        self.enterTriggered= self.exitWait = False
        self.firstPassDone = False

    def draw(self, surface):
        pass

    def update(self,dt):
        state=GameState()
        if(not state.inGame):
            return
        self.triggerSource = state.player   # todo at construction of trigger player doesnt yet exist and triggersource is invalid

        _inside = pygame.sprite.collide_rect(self,self.triggerSource)
        if(_inside and not self.enterTriggered):
            if(self.firstPassDone):
                #if teleporting from warpA to warpB this would trigger collision again immediatly
                #- have to wait until player moves away from trigger
                if(self.CB_onEnter!= None): self.CB_onEnter(self.triggerSource,self.params)
            self.enterTriggered  = True
            return
        if(not _inside and self.enterTriggered): 
            if(self.firstPassDone):
                if(self.CB_onExit!= None):self.CB_onExit(self.triggerSource,self.params)
            self.enterTriggered=False
            return

        self.firstPassDone=True



class Warp(Trigger):
    """ a trigger to move the player to a different loaction f.e. a door or teleporter
    make sure that their is enough space or the sprite might gat stuck in an obstacle or is pushed away
    """
    def __init__(self,rect):
        self.map = self.world = None
        self.target = None
        state=GameState() 
        super().__init__(rect,#state.player,
                         CB_onEnter = self.onEnter)


    def setTarget(self,map,target,world):
        """
        map = filename of the roomlayout
        target = spawnposition (Rect or textlabel of an object)
        world = "" if this is a teleport to a room inside this world or a name of a world
        """
        self.map = map
        self.target = target
        self.world = world

    def onEnter(self,triggerSource,params):
        self.notifyOnHit(triggerSource)

    def OBSOLETE_update(self,dt):
        state=GameState()
        if(not state.inGame or self.triggered):
            return
        if(pygame.sprite.collide_rect(self,state.player)):
            #if teleporting from warpA to warpB this would trigger collision again immediatly
            #- have to wait until player moves away from trigger
            if(self.firstPassDone):
            #    self.notifyOnHit(state.player)
                self.triggered=True
        else:
            self.firstPassDone=True
