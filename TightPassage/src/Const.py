import sys, os
import pygame

#some global constants

FPS = 60.0
WINDOW_SIZE = (640, 640)
BACKGROUND_COLOR = (40, 40, 40)

#colors for debug draw
BLACK =  (  0,   0,   0)
WHITE =  (255, 255, 255)
BLUE =   (  0,   0, 255)
GREEN =  (  0, 255,   0)
RED =    (255,   0,   0)
PURPLE = (155,   0, 155)

COLOR_KEY = (255, 0, 255) #transparency color of sprites without alpha
CAPTION = "dungeon"

#debug-tools
DEBUG = True    #enables some stuff that should only be available in dev-mode
DRAW_COLLIDERS = True  # hitrects and colliders are drawn on screen

def resource_path(relative_path):
    """ Get the absolute path to the resource, works for dev and for PyInstaller 
    resource_path("assets/sprites/shader.png")
    """
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)