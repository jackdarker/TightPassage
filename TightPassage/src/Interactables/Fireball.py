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

#import src.Interactables.Interactable
#from src.Interactables.Interactable import Interactable

class Fireball(Unit):
    SPRITEIMAGE = None

    def __init__(self, creator, speed, direction=pygame.K_RIGHT):
        """
        Arguments are a rect representing the Player's location and
        dimension, the speed(in pixels/frame) of the Player, and the Player's
        starting direction (given as a key-constant).
        """
        rect = pygame.Rect((0,0), (32,32))  #imagesize
        rect.center = creator.rect.center
        if(type(self).SPRITEIMAGE == None):
            type(self).SPRITEIMAGE = pygame.image.load(Const.resource_path("assets/sprites/fireball1.png")).convert_alpha()
        super().__init__( rect, speed, direction)
        hit_size = int(0.8*self.rect.width), int(0.8*self.rect.height)
        self.hitrect = pygame.Rect((0,0), hit_size)
        self.hitrect.midbottom = self.rect.midbottom
        self.speed = speed
        self.parent = creator
        self.direction_offset = Interactable.DIRECT_DICT[direction]

        anim = AnimData()
        name="walkright"
        anim.fps=7
        indices = [[0,0],[1,0],[2,0],[3,0],[4,0]]
        anim.frames = Support.get_images(type(self).SPRITEIMAGE, indices, self.rect.size)
        self.cGraphic.addAnimation(name,anim)
        #
        name="walkleft"
        #anim.frames = [pygame.transform.flip(frame, True, False) 
        #               for frame in Support.get_images(type(self).SPRITEIMAGE, indices, self.rect.size)]
        self.cGraphic.addAnimation(name,anim)
        name="walkup"
        self.cGraphic.addAnimation(name,anim)
        name="walkdown"
        self.cGraphic.addAnimation(name,anim)
        name="idle"
        self.cGraphic.addAnimation(name,anim)
        #
        anim = AnimData()
        name="dieright"
        anim.fps=7
        indices = [[0,1],[1,1],[2,1]]
        anim.frames = Support.get_images(type(self).SPRITEIMAGE, indices, self.rect.size)
        self.cGraphic.addAnimation(name,anim)
        #
        anim = AnimData()
        name="dieleft"
        anim.fps=7
        indices = [[0,1],[1,1],[2,1]]
        anim.frames = [pygame.transform.flip(frame, True, False) 
                       for frame in Support.get_images(type(self).SPRITEIMAGE, indices, self.rect.size)]
        self.cGraphic.addAnimation(name,anim)
        #
        anim = AnimData()
        name="dieup"
        anim.fps=7
        indices = [[0,1],[1,1],[2,1]]
        anim.frames = [pygame.transform.rotate(frame, 90) 
                       for frame in Support.get_images(type(self).SPRITEIMAGE, indices, self.rect.size)]
        self.cGraphic.addAnimation(name,anim)
        #
        anim = AnimData()
        name="diedown"
        anim.fps=7
        indices = [[0,1],[1,1],[2,1]]
        anim.frames = [pygame.transform.rotate(frame, -90) 
                       for frame in Support.get_images(type(self).SPRITEIMAGE, indices, self.rect.size)]
        self.cGraphic.addAnimation(name,anim)
            #type(self).SPRITEIMAGE.set_colorkey(Const.COLOR_KEY)
            #type(self).SPRITEIMAGE = pygame.Surface((30,30)).convert_alpha()
            #type(self).SPRITEIMAGE.fill((100,0,0))

    def make_frame_dict(self):
        """
        Create a dictionary of direction keys to frames. We can use
        transform functions to reduce the size of the sprite sheet we need.
        """
        indices = [[0,0],[1,0],[2,0],[3,0],[4,0]]
        frames = Support.get_images(type(self).SPRITEIMAGE, indices, self.rect.size)
        self.walkframe_dict = { pygame.K_RIGHT : [frames[0],frames[1],frames[2],frames[3],frames[4]],
            pygame.K_LEFT :[frames[0],frames[1],frames[2],frames[3],frames[4]],
            pygame.K_UP :[frames[0],frames[1],frames[2],frames[3],frames[4]],
            pygame.K_DOWN : [frames[0],frames[1],frames[2],frames[3],frames[4]] }
        indices = [[0,1],[1,1],[2,1]]
        frames = Support.get_images(type(self).SPRITEIMAGE, indices, self.rect.size)
        self.dieframe_dict = { pygame.K_RIGHT : [frames[0],frames[1],frames[2]],
            pygame.K_LEFT :[frames[0],frames[1],frames[2]],
            pygame.K_UP :[frames[0],frames[1],frames[2]],
            pygame.K_DOWN : [frames[0],frames[1],frames[2]] }

        self.idleframe_dict = self.walkframe_dict

    def movement(self, obstacles, i):
        """
        i =0 is x; i=1 is y 
        """
        direction_vector = Interactable.DIRECT_DICT[self.direction]
        self.hitrect[i] += self.speed*direction_vector[i]
        callback = self.collide_other(self.hitrect)  #Collidable callback created.
        collisions = pygame.sprite.spritecollide(self, obstacles, False, callback)
        while collisions:
            collision = collisions.pop()
            self.notifyOnHit(collision)
        self.rect.midbottom = self.hitrect.midbottom

    def OnHit(self,otherSprite):
        """hit someone and cause damage"""
        if(self.start_dieing()):
            _func = getattr(otherSprite,"damage",None)
            if(_func!=None):
                _func(1,self.direction)
            self.direction_offset = pygame.Vector2(0,0)
        