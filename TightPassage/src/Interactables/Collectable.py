import os
import random
import pygame

class Collectable(pygame.sprite.Sprite):
    """Something to run head-first into."""
    #Alpha-Image for sprite
    SHADE_MASK = None