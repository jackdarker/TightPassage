import os
import pygame
import pygame_menu
import random
import src.Const as Const
import src.GameModeObserver as GameModeObserver
import src.GameModes.PlayMode as PlayMode
import src.GameModes.BattleMode as BattleMode
import src.GameModes.MessageMode as MessageMode
import src.GameModes.MenuMode as MenuMode
import src.GameModes.MovieMode as MovieMode
import src.GameState as GameState

import testGame.battleTest as battleTest #todo remove this

class App(GameModeObserver.GameModeObserver):
    """main-application containing the main loop
    receives notifiactions from gamemodes
    """
    def __init__(self):
        self._running = True
        self.screen = None  #surface to paint on
        self.playmode = None    #statemachine of the game
        self.menumode = None    #menu overlay logic
        self.interactmode = None    #actual interaction like dialogs,...
        self.state = GameState.GameState()  #game data
 
    def on_init(self):
        pygame.mixer.pre_init(44100, -16, 2, 512) #if this line is not placed before pygame.init there might be delay on sound, also buffersize should be small
        pygame.init()
        self.screen = pygame.display.set_mode(Const.WINDOW_SIZE, pygame.HWSURFACE | pygame.DOUBLEBUF  ) #| pygame.SCALED??
        pygame.mixer.init()
        self.clock = pygame.time.Clock()
        self.menumode = MenuMode.MenuMode(self.screen,self.state)
        self.menumode.addObserver(self)
        intro = MovieMode.SceneData()
        intro.loadImageStrip(Const.resource_path("assets\sprites\Movie"),24)
        self.moviemode = MovieMode.MovieMode(intro)
        self.moviemode.addObserver(self)
        #self.moviemode.show()  #show the intro
        self.menumode.show_MainMenu()

    def on_loop(self,dt):
        """update all modes"""
        #processInput will consume all events, so only one mode should be called
        if(self.menumode.inMenu()):
            self.menumode.processInput()
            self.menumode.update(dt)
        elif(self.moviemode.enabled):
            self.moviemode.processInput()
            self.moviemode.update(dt)
        elif(self.interactmode!=None and self.interactmode.enabled):
            self.interactmode.processInput()
            self.interactmode.update(dt)
        elif(self.playmode!=None):
            self.playmode.processInput()
            self.playmode.update(dt)

    def on_render(self):
        """render all modes"""
        if(self.playmode!=None):
            self.playmode.render(self.screen)
            self.playmode.drawdebug(self.screen)
        if(self.interactmode!=None and self.interactmode.enabled):
            self.interactmode.render(self.screen)
        elif(self.moviemode.enabled):
            self.moviemode.render(self.screen)
        self.menumode.render(self.screen)
        self.display_fps()
        pygame.display.flip()

 
    def on_execute(self):
        """main execution loop"""
        if self.on_init() == False:
            self._running = False
        while( self._running ):
            dt = self.clock.tick(Const.FPS)
            self.on_loop(dt)
            self.on_render() 
        self.on_cleanup()

    def on_cleanup(self):
        pygame.quit()

    def quitRequested(self):
        """notification"""
        self._running = False
    
    def newGameRequested(self,MazeGenerator):
        """notification from menumode"""
        if(self.playmode!= None):
            self.playmode.removeObserver(self)
            self.playmode = None
        self.state.reset()
        self.state.mazeGenerator= MazeGenerator
        self.playmode = PlayMode.PlayMode(self.state)
        self.playmode.addObserver(self)
        pass

    def newBattleRequested(self,Battle):
        """starts a battle"""
        if(self.playmode!= None):
            self.playmode.removeObserver(self)
            self.playmode = None
        self.state.reset()
        self.state.battleData = battleTest.battleTest()
        self.playmode = BattleMode.BattleMode(self.state,self.state.battleData)
        self.playmode.addObserver(self)
        pass

    def showMenuRequested(self):
        """notification from gamemode"""
        self.menumode.show_MainMenu()

    def showPopupRequested(self,Message):
        """notification from gamemode"""
        self.interactmode = MessageMode.MessageMode(self.state,Message)
        #self.interactmode.show()

    def display_fps(self):
        """Show the program's FPS in the window handle."""
        caption = "{} - FPS: {:.2f}".format(Const.CAPTION, self.clock.get_fps())
        pygame.display.set_caption(caption)

if __name__ == "__main__" :
    """if this script was the start script- run the App"""
    theApp = App()
    theApp.on_execute()