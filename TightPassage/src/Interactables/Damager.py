import os
import pygame
import src.Const as Const
import src.Support as Support
import src.Interactables.Interactable
from src.Interactables.Interactable import Interactable
import src.Interactables.Unit as Unit
from src.Interactables.Unit import Unit
import src.Components.ComponentGraphics
from src.Components.ComponentGraphics import UnitGraphics
from src.Components.ComponentGraphics import AnimData

class DamagerInfo:
    def __init__(self, direction,duration,damage,size,offset):
        self.size = size    # size of the damager hitrect
        self.direction = direction  #in which direction the damager is executed
        self.duration = duration    #how long the damager is active
        self.damage = damage    #amount of damage

        # positionoffset to sprite-center when facing to right
        #the offset&size of the hitrect needs to be adjusted depending on the direction
        if(direction==pygame.K_LEFT):
            self.offset = (offset[0]*-1, offset[1])
        elif(direction==pygame.K_UP):
            self.offset = (offset[1], offset[0]*-1)
            self.size = (size[1],size[0])
        elif(direction==pygame.K_DOWN):
            self.offset = (offset[1], offset[0])
            self.size = (size[1],size[0])
        else: self.offset = offset   
        pass

class Damager(Unit):
    __SPRITEIMAGE = None

    def __init__(self, creator, damagerInfo):
        self.damagerInfo = damagerInfo
        rect = pygame.Rect((0,0), damagerInfo.size)  #todo
        rect.center = creator.rect.center
        rect.move_ip(self.damagerInfo.offset)
        super().__init__( rect, 0, damagerInfo.direction)
        self.hitrect = pygame.Rect(rect)
        self.hitrect.center = self.rect.center
        self.parent = creator
        self.duration = self.damagerInfo.duration
        self.direction_offset = Interactable.DIRECT_DICT[self.damagerInfo.direction]
        #just for visualisation:
        image = pygame.Surface(rect.size).convert_alpha()   #todo image size from leveldata
        image.fill((255,0,0,60))
        anim = AnimData()
        anim.frames = [image]
        self.cGraphic.addAnimation("idle",anim)

    def draw(self, surface):
        """draws the image"""
        self.cGraphic.update()
        self.cGraphic.draw(self.image)   #self.cGraphic.draw(surface)

    def update(self):
        super().update()
        self.duration-=1
        if(self.duration<0): self.kill()

    def movement(self, i):
        """i =0 is x; i=1 is y """
        #direction_vector = Interactable.DIRECT_DICT[self.direction]
        #self.hitrect[i] += self.speed*direction_vector[i]
        #self.rect.midbottom = self.hitrect.midbottom

        callback = self.collide_other(self.hitrect)  #Collidable callback created.
        collisions = pygame.sprite.spritecollide(self, self.levelData.units, False, callback)
        while collisions:
            collision = collisions.pop()
            self.notifyOnHit(collision)
            return        

    def OnHit(self,otherSprite):
        """hit someone and cause damage"""
        if(self.start_dieing()): #only react on the first hit
            _func = getattr(otherSprite,"damage",None)
            if(_func!=None):
                _func(self.damagerInfo.damage,self.direction)
            self.direction_offset = pygame.Vector2(0,0)
        else:
            pass