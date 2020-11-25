import pygame
import src.Const as Const
import src.Support as Support
from src.GameState import GameState
from src.Components.Party import Character,Party,CharacterReserve
from src.Components.SkillDB import *
from src.DialogMode.DialogScene import DialogScene
from Tutorial.Tutorial1 import *
import src.Components.ResourceManager as RM
from src.Components.ComponentGraphics import ComponentGraphics,AnimData

if __name__ == "__main__" :
    pygame.mixer.pre_init(44100, -16, 2, 512) #if this line is not placed before pygame.init there might be delay on sound, also buffersize should be small
    pygame.init()
    screen = pygame.display.set_mode(Const.WINDOW_SIZE, pygame.HWSURFACE | pygame.DOUBLEBUF  ) 
    pygame.mixer.init()
    clock = pygame.time.Clock()

    game = GameState()
    game.reset()

    Done = False
    def on_done():
        global Done 
        Done = True

    dialog = DialogScene(game,on_done=on_done)
    dialog.startScene(Tutorial1())

    
    while(not Done):
        dt = clock.tick(Const.FPS)
        dialog.processInput()
        dialog.update(10)
        dialog.render(screen)
        pygame.display.flip()
