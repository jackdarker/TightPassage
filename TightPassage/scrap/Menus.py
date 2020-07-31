import pygame
import pygame_menu

class MenuManager():
    def __init__(self, screen, onStartGame):
        self.screen = screen
        #self.menu_screen = self.screen.copy()
        self.main_menu = None
        self.pause_menu = None
        self.start_the_game = onStartGame
        pass

    #@staticmethod
    def show_MainMenu(self):
        #if(self.main_menu == None):
        menu = pygame_menu.Menu(300, 400, 'Welcome',theme=pygame_menu.themes.THEME_BLUE)
        menu.add_text_input('Name :', default='John Doe')
        menu.add_selector('Difficulty :', [('Hard', 1), ('Easy', 2)], onchange=self.set_difficulty)
        menu.add_button('Play', self.new_game)
        menu.add_button('Quit', pygame_menu.events.EXIT)
        self.main_menu = menu
        self.main_menu.enable()
        return(self.main_menu)

    def show_PauseMenu(self):
        #if(self.pause_menu == None):
        menu = pygame_menu.Menu(300, 300, 'Pause',theme=pygame_menu.themes.THEME_GREEN)
        menu.add_button('Continue', self.resume_game)
        menu.add_button('Back to Start', self.main_menu)
        self.pause_menu = menu
        self.pause_menu.enable()
        return(self.pause_menu)

    def set_difficulty(self,value, difficulty):
        # Do the job here !
        pass 

    def new_game(self):
        self.main_menu.disable()
        self.main_menu.reset(1)
        self.start_the_game()

    def resume_game(self):
        self.pause_menu.disable()

    def updateMenu(self):
        if(self.main_menu!= None):
           if(self.main_menu.is_enabled()): 
               self.main_menu.mainloop(self.screen)
        if(self.pause_menu!= None):
            if(self.pause_menu.is_enabled()): 
                self.pause_menu.mainloop(self.screen)
