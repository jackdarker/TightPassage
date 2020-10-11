import pygame
import pygame_menu
import src.Const as Const
import src.GameMode as GameMode
from src.BattleMode.BattleController import BattleData,BattleController
from src.BattleMode.BattleScreen import BattleScreen

class BattleMode(GameMode.GameMode):
    """turnbased battlescreen
    """
    def __init__(self,screen,state,battleData):
        super().__init__(state)
        
        self.menu_screen = screen.copy()
        self.menu_screen.fill((0, 0, 0, 200))
        self.menu_screen.set_alpha(100) #why does fill with RGB+alpha not work?
        self.menu = None
        self.battleCtrl = BattleController(state,battleData)
        self.view = BattleScreen(screen,state,self.battleCtrl)

    def processInput(self):
        events = pygame.event.get()
        self.view.processInput(events)

    def update(self,dt):
        self.view.update(dt)
        self.battleCtrl.update(dt)
        pass
        
    def render(self, window):
        self.view.render(window)


