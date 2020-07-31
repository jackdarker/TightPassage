import pygame

#some global constants

FPS = 60.0
WINDOW_SIZE = (640, 480)
BACKGROUND_COLOR = (40, 40, 40)
#transparency color of sprites
COLOR_KEY = (255, 0, 255)
CAPTION = "dungeon"

DIRECT_DICT = {pygame.K_LEFT  : (-1, 0),
               pygame.K_RIGHT : ( 1, 0),
               pygame.K_UP    : ( 0,-1),
               pygame.K_DOWN  : ( 0, 1)}
