import sys, os
import pygame

#some global constants

FPS = 60.0
WINDOW_SIZE = (640, 480)
BACKGROUND_COLOR = (40, 40, 40)
#transparency color of sprites
COLOR_KEY = (255, 0, 255)
CAPTION = "dungeon"


def resource_path(relative_path):
    """ Get the absolute path to the resource, works for dev and for PyInstaller """
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)