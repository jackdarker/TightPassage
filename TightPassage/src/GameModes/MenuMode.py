import pygame
import pygame_menu
import src.Const as Const
import src.GameMode as GameMode

class MenuMode(GameMode.GameMode):
    def __init__(self,screen,state):     
        super().__init__(state)
        self.screen = screen
        self.menu_screen = self.screen.copy()
        self.menu_screen.fill((0, 0, 0, 200))
        self.menu_screen.set_alpha(100) #why does fill with RGB+alpha not work?
        self.menu = None
        menu = pygame_menu.Menu(300, 400, 'Welcome',theme=pygame_menu.themes.THEME_BLUE)
        menu.add_text_input('Name :', default='John Doe')
        menu.add_selector('Difficulty :', [('Hard', 1), ('Easy', 2)], onchange=self.set_difficulty)
        menu.add_button('Play', self.new_game)
        menu.add_button('Quit', pygame_menu.events.EXIT)
        self.main_menu = menu
        menu2 = pygame_menu.Menu(300, 300, 'Pause',theme=pygame_menu.themes.THEME_GREEN)
        menu2.add_button('Continue', self.resume_game)
        menu2.add_button('Back to Start', self.main_menu)
        self.pause_menu = menu2
        self.show_MainMenu()

    def inMenu(self):
        return(self.menu.is_enabled())

    def processInput(self):
        events = pygame.event.get()
        self.menu.update(events)

    def update(self):
        pass
        
    def render(self, window):
        if (self.menu.is_enabled()):
            window.blit(self.menu_screen,(0,0))
            self.menu.draw(window)

    def set_difficulty(self,value, difficulty):
        # Do the job here !
        pass 

    def new_game(self):
        self.menu.disable()
        self.menu.reset(1)
        self.notifyLoadLevelRequested("Level1")
        #self.start_the_game()

    def show_MainMenu(self):
        if(self.state.inGame):
            self.show_PauseMenu()
            return
        #if(self.main_menu == None):
        #menu = pygame_menu.Menu(300, 400, 'Welcome',theme=pygame_menu.themes.THEME_BLUE)
        #menu.add_text_input('Name :', default='John Doe')
        #menu.add_selector('Difficulty :', [('Hard', 1), ('Easy', 2)], onchange=self.set_difficulty)
        #menu.add_button('Play', self.new_game)
        #menu.add_button('Quit', pygame_menu.events.EXIT)
        self.menu = self.main_menu
        self.menu.enable()

    def show_PauseMenu(self):
        #if(self.pause_menu == None):
        #menu = pygame_menu.Menu(300, 300, 'Pause',theme=pygame_menu.themes.THEME_GREEN)
        #menu.add_button('Continue', self.resume_game)
        #menu.add_button('Back to Start', self.main_menu)
        self.menu = self.pause_menu
        self.menu.enable()

    def resume_game(self):
        self.menu.disable()

