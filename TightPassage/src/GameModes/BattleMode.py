import pygame
import pygame_menu
import src.Const as Const
import src.GameMode as GameMode
from src.GameState import GameState,GameStateObserver
from src.BattleMode.BattleController import BattleData,BattleController
from src.BattleMode.BattleScreen import *

class BattleMode(GameMode.GameMode, GameStateObserver):
    """turnbased battlescreen
    """
    def __init__(self,state,battleData, on_done = None):
        super().__init__(state)
        self.on_done = on_done
        self.battleCtrl = BattleController(state,battleData)
        self.view = BattleScreen(state,self.battleCtrl)
        self.view.addObserver(self.battleCtrl)
        state.addObserver(self)
        self.paused = False
        self.done = False
        self.state.inGame = True

    def processInput(self):
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                self.notifyQuitRequested()
                break
        self.view.processInput(events)

    def update(self,dt):
        if(not self.done):
            self.battleCtrl.update(dt)
            self.view.update(dt)
            self.done = self.battleCtrl.battleData.battleDone
            if(self.done and self.on_done): 
                self.on_done()
        pass
        
    def render(self, window):
        self.view.render(window)

    def drawdebug(self,window):
        pass


    def is_paused(self):
        return self.paused

    def pause(self,pause=True):
        self.paused = pause