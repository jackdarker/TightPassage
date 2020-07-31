import os
import pygame
import pygame_menu
import random
import src.Const as Const
import src.GameModeObserver as GameModeObserver
import src.GameModes.PlayMode as PlayMode
import src.GameModes.MessageMode as MessageMode
import src.GameModes.MenuMode as MenuMode
import src.GameState as GameState

class App(GameModeObserver.GameModeObserver):
    def __init__(self):
        self._running = True
        self.screen = None
        self.playmode = None
        self.menumode = None
        self.state = GameState.GameState()
 
    def on_init(self):
        pygame.init()
        self.screen = pygame.display.set_mode(Const.WINDOW_SIZE, pygame.HWSURFACE | pygame.DOUBLEBUF )
        self.clock = pygame.time.Clock()
        #self.menus = Menus.MenuManager(self.screen,self.start_the_game)
        #self.menus.show_MainMenu()
        self.menumode = MenuMode.MenuMode(self.screen,self.state)
        self.menumode.addObserver(self)

    def loadLevelRequested(self,filename):
        if(self.playmode!= None):
            self.playmode.removeObserver(self)
            self.playmode = None
        self.playmode = PlayMode.PlayMode(self.state)
        self.playmode.addObserver(self)
        pass

    def showMenuRequested(self):
        self.menumode.show_MainMenu()

    def on_loop(self):
        if(self.menumode.inMenu()):
            self.menumode.processInput()
            self.menumode.update()
            
        elif(self.playmode!=None):
            self.playmode.processInput()
            self.playmode.update()
        else:
            #self.menus.updateMenu()
            pass

    def on_render(self):
        
        if(self.playmode!=None):
            self.playmode.render(self.screen)
        self.menumode.render(self.screen)
        self.display_fps()
        pygame.display.flip()

 
    def on_execute(self):
        """main execution loop"""
        if self.on_init() == False:
            self._running = False
        while( self._running ):
            #for event in pygame.event.get():
            #    self.on_event(event)
            self.on_loop()
            self.on_render()
            self.clock.tick(Const.FPS)
        self.on_cleanup()

    def on_cleanup(self):
        pygame.quit()

    def quitRequested(self):
        self._running = False

    def display_fps(self):
        """Show the program's FPS in the window handle."""
        caption = "{} - FPS: {:.2f}".format(Const.CAPTION, self.clock.get_fps())
        pygame.display.set_caption(caption)



if __name__ == "__main__" :
    theApp = App()
    theApp.on_execute()