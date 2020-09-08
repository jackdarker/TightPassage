import os
import pygame
import src.Const as Const
import src.Support as Support
import src.Interactables.Unit
from src.Interactables.Unit import Unit
import src.Interactables.Fireball
from src.Interactables.Fireball import Fireball
import src.Components.ComponentGraphics
from src.Components.ComponentGraphics import UnitGraphics
from src.Components.ComponentGraphics import AnimData

class Player(Unit):
    KEY_ATTACK = pygame.K_SPACE
    KEY_USE = pygame.K_e

    def __init__(self, rect, speed, direction=pygame.K_RIGHT):
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

        hit_size = int(0.4*self.rect.width), int(0.6*self.rect.height)
        self.hitrect = pygame.Rect((0,0), hit_size)
        self.hitrect.midbottom = self.rect.midbottom
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

    def make_frame_dict(self):
        """
        Create a dictionary of direction keys to frames. We can use
        transform functions to reduce the size of the sprite sheet we need.
        """
        indices = [[1,1],[2,1],[3,1],[4,1],[5,1],[6,1]]
        frames = Support.get_images(type(self).SPRITEIMAGE, indices, self.rect.size)
        self.walkframe_dict = { pygame.K_RIGHT : [frames[0],frames[1],frames[2],frames[3],frames[4],frames[5]],
            pygame.K_LEFT :[pygame.transform.flip(frames[0], True, False),
                            pygame.transform.flip(frames[1], True, False),
                            pygame.transform.flip(frames[2], True, False),
                            pygame.transform.flip(frames[3], True, False),
                            pygame.transform.flip(frames[4], True, False),
                            pygame.transform.flip(frames[5], True, False)],
            pygame.K_UP :   [frames[0],frames[1],frames[2],frames[3],frames[4],frames[5]],
            pygame.K_DOWN : [frames[0],frames[1],frames[2],frames[3],frames[4],frames[5]] }

        indices = [[0,6],[1,6],[2,6],[3,6],[4,6],[5,6],[6,6]]
        frames = Support.get_images(type(self).SPRITEIMAGE, indices, self.rect.size)
        self.attackframe_dict = { pygame.K_RIGHT : [frames[0],frames[1],frames[2],frames[3],frames[4],frames[5],frames[6]],
            pygame.K_LEFT :[pygame.transform.flip(frames[0], True, False),
                            pygame.transform.flip(frames[1], True, False),
                            pygame.transform.flip(frames[2], True, False),
                            pygame.transform.flip(frames[3], True, False),
                            pygame.transform.flip(frames[4], True, False),
                            pygame.transform.flip(frames[5], True, False),
                            pygame.transform.flip(frames[6], True, False)],
            pygame.K_UP :   [frames[0],frames[1],frames[2],frames[3],frames[4],frames[5],frames[6]],
            pygame.K_DOWN : [frames[0],frames[1],frames[2],frames[3],frames[4],frames[5],frames[6]]}

        indices = [[0,0],[1,0],[2,0],[3,0]]
        frames = Support.get_images(type(self).SPRITEIMAGE, indices, self.rect.size)
        self.idleframe_dict = { pygame.K_RIGHT : [frames[0],frames[1],frames[2],frames[3]],
            pygame.K_LEFT :[pygame.transform.flip(frames[0], True, False),
                            pygame.transform.flip(frames[1], True, False),
                            pygame.transform.flip(frames[2], True, False),
                            pygame.transform.flip(frames[3], True, False)],
            pygame.K_UP :   [frames[0],frames[1],frames[2],frames[3]],
            pygame.K_DOWN : [frames[0],frames[1],frames[2],frames[3]] }

        indices = [[0,1],[1,1],[2,1]]
        frames = Support.get_images(type(self).SPRITEIMAGE, indices, self.rect.size)
        self.dieframe_dict = { pygame.K_RIGHT : [frames[0],frames[1],frames[2]],
            pygame.K_LEFT :[frames[0],frames[1],frames[2]],
            pygame.K_UP :[frames[0],frames[1],frames[2]],
            pygame.K_DOWN : [frames[0],frames[1],frames[2]] }

    def attack(self):
        """attack in view direction"""
        if(self.cd_Atk<=0):
            self.cd_Atk = Const.FPS
            self.timer_Atk = Const.FPS // 2 #todo depends on attack
            self.attacking = True
            return Fireball(self, 10, self.direction)
        else:
            return None