import os
import pygame
import src.Const as Const
import src.Support as Support
import src.Interactables.Unit
from src.Interactables.Unit import Unit
import src.Interactables.Fireball
from src.Interactables.Fireball import Fireball

class Player(Unit):
    KEY_ATTACK = pygame.K_SPACE
    KEY_USE = pygame.K_e
    SPRITEIMAGE = None


    def __init__(self, rect, speed, direction=pygame.K_RIGHT):
        """
        Arguments are a rect representing the Player's location and
        dimension, the speed(in pixels/frame) of the Player, and the Player's
        starting direction (given as a key-constant).
        """
        _rect = pygame.Rect((rect[0],rect[1]), (50,37)) #imagesize !
        if(type(self).SPRITEIMAGE == None):
            type(self).SPRITEIMAGE = pygame.image.load(Const.resource_path("assets/sprites/adventurer-v1.5-Sheet.png")).convert_alpha()
        super().__init__( _rect, speed, direction)
        hit_size = int(0.4*self.rect.width), int(0.6*self.rect.height)
        self.hitrect = pygame.Rect((0,0), hit_size)
        self.hitrect.midbottom = self.rect.midbottom

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
            self.attacking = True
            return Fireball(self, 10, self.direction)
        else:
            return None