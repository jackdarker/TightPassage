import os
import pygame
import src.Const as Const
import src.Interactables.Unit as Unit

class Player(Unit.Unit):
    KEY_ATTACK = pygame.K_SPACE
    KEY_USE = pygame.K_e
    def __init__(self, rect, speed, direction=pygame.K_RIGHT):
        """
        Arguments are a rect representing the Player's location and
        dimension, the speed(in pixels/frame) of the Player, and the Player's
        starting direction (given as a key-constant).
        """
        super().__init__( rect, speed, direction)