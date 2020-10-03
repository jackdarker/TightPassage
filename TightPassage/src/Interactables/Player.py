import os
import pygame
import src.Const as Const
import src.Support as Support
from src.Vector import Vector2
import src.Interactables.Unit
from src.Interactables.Unit import Unit
from src.Interactables.Fireball import Fireball
from src.Interactables.Damager import Damager
from src.Interactables.Damager import DamagerInfo
import src.Components.ComponentGraphics
from src.Components.ComponentGraphics import UnitGraphics
from src.Components.ComponentGraphics import AnimData

class Player(Unit):
    KEY_ATTACK = pygame.K_SPACE
    KEY_USE = pygame.K_e

    def __init__(self, rect, speed, direction=Vector2(1,0)):
        """
        Arguments are a rect representing the Player's location and
        dimension, the speed(in pixels/frame) of the Player, and the Player's
        starting direction (given as a key-constant).
        """
        _rect = pygame.Rect((rect[0],rect[1]), (64,64)) #imagesize !
        #load spritesheet
        SPRITEIMAGE = pygame.image.load(Const.resource_path("assets/sprites/clotharmor.png")).convert_alpha()
        SWORDIMAGE = pygame.image.load(Const.resource_path("assets/sprites/sword1.png")).convert_alpha()
        SPRITEIMAGE.blit(SWORDIMAGE,(0,0))
        super().__init__( _rect, speed, direction)

        hit_size = int(self.rect.width//2), int(self.rect.height//2)
        self.hitrect = pygame.Rect((0,0), hit_size)
        self.hitrect.center = self.rect.center
        
        if(Const.DRAW_COLLIDERS):   #just for visualisation:
            self.hitboximage = pygame.Surface(self.rect.size).convert_alpha()   #todo image size from leveldata
            self.hitboximage.fill((0,255,0,0),self.rect)
            self.hitboximage.fill((0,255,0,60),self.hitrect)

        self.canUseDoors =True

        #build animations
        anim = AnimData()
        name="idleright"
        anim.fps=2
        indices = [[0,2],[1,2]]
        anim.frames = Support.get_images(SPRITEIMAGE, indices, self.rect.size)
        self.cGraphic.addAnimation(name,anim)
        anim = AnimData()
        name="idleleft"
        anim.frames = [pygame.transform.flip(frame, True, False) 
                       for frame in Support.get_images(SPRITEIMAGE, indices, self.rect.size)]
        self.cGraphic.addAnimation(name,anim)
        anim = AnimData()
        name="idleup"
        anim.fps=2
        indices = [[0,5],[1,5]]
        anim.frames = Support.get_images(SPRITEIMAGE, indices, self.rect.size)
        self.cGraphic.addAnimation(name,anim)
        anim = AnimData()
        name="idledown"
        anim.fps=2
        indices = [[0,8],[1,8]]
        anim.frames = Support.get_images(SPRITEIMAGE, indices, self.rect.size)
        self.cGraphic.addAnimation(name,anim)
        #
        anim = AnimData()
        name="walkright"
        anim.fps=2
        indices = [[0,1],[1,1],[2,1],[3,1]]
        anim.frames = Support.get_images(SPRITEIMAGE, indices, self.rect.size)
        self.cGraphic.addAnimation(name,anim)
        anim = AnimData()
        name="walkleft"
        anim.frames = [pygame.transform.flip(frame, True, False) 
                       for frame in Support.get_images(SPRITEIMAGE, indices, self.rect.size)]
        self.cGraphic.addAnimation(name,anim)
        anim = AnimData()
        name="walkup"
        indices = [[0,4],[1,4],[2,4],[3,4]]
        anim.frames = Support.get_images(SPRITEIMAGE, indices, self.rect.size)
        self.cGraphic.addAnimation(name,anim)
        anim = AnimData()
        name="walkdown"
        indices = [[0,7],[1,7],[2,7],[3,7]]
        anim.frames = Support.get_images(SPRITEIMAGE, indices, self.rect.size)
        self.cGraphic.addAnimation(name,anim)
        #
        anim = AnimData()
        name="attackright"
        indices = [[0,0],[1,0],[2,0],[3,0]]
        anim.frames = Support.get_images(SPRITEIMAGE, indices, self.rect.size)
        self.cGraphic.addAnimation(name,anim)
        anim = AnimData()
        name="attackleft"
        anim.frames = [pygame.transform.flip(frame, True, False) 
                       for frame in Support.get_images(SPRITEIMAGE, indices, self.rect.size)]
        self.cGraphic.addAnimation(name,anim)
        anim = AnimData()
        name="attackup"
        indices = [[0,3],[1,3],[1,3],[1,3]]
        anim.frames = Support.get_images(SPRITEIMAGE, indices, self.rect.size)
        self.cGraphic.addAnimation(name,anim)
        anim = AnimData()
        name="attackdown"
        indices = [[0,6],[1,6],[1,6],[1,6]]
        anim.frames = Support.get_images(SPRITEIMAGE, indices, self.rect.size)
        self.cGraphic.addAnimation(name,anim)
        #
        SPRITEIMAGE = pygame.image.load(Const.resource_path("assets/sprites/death.png")).convert_alpha()
        anim = AnimData()
        name="die"
        anim.fps=4
        indices = [[0,0],[1,0],[2,0],[3,0],[4,0]]
        anim.frames = Support.get_images(SPRITEIMAGE, indices, (48,48))
        self.cGraphic.addAnimation(name,anim)
        SPRITEIMAGE = None

    def draw(self, surface):
        """draws the image"""
        super().draw(surface)
        if(Const.DRAW_COLLIDERS):   #just for visualisation:
            self.image.blit(self.hitboximage,(0,0))

    def attack(self):
        """attack in view direction"""
        if(self.coolDown_Attack<=0):
            self.coolDown_Attack = Const.FPS
            self.timer_Atk = Const.FPS // 2 #todo depends on attack
            self.attacking = True

            return Damager(self,DamagerInfo(self.direction, Const.FPS//2,1,(16,32),(28,0)))
            #return Fireball(self, 10, self.direction)
        else:
            return None

    def interact(self):
        """check if there is anything nearby to interact with"""
        _rect = self.hitrect.copy()
        _rect.move_ip(self.direction*5) #todo in front of the own hitrect
        callback = self.collide_other(_rect)  #Collidable callback created.
        collisions = pygame.sprite.spritecollide(self, self.levelData.units, False, callback)
        while collisions:
            collision = collisions.pop()
            self.notifyOnInteract(collision)
            return
        pass