import pygame
import pygame_menu
import src.Const as Const
import src.GameMode as GameMode

class MenuMode(GameMode.GameMode):
    def __init__(self,screen,state):
        super().__init__(state)
        self.menu_screen = screen.copy()
        self.menu_screen.fill((0, 0, 0, 200))
        self.menu_screen.set_alpha(100) #why does fill with RGB+alpha not work?
        self.menu = None
        font = pygame_menu.font.FONT_OPEN_SANS
        my_theme = pygame_menu.themes.THEME_BLUE.copy()
        my_theme.widget_font=font
        #mainmenu
        menu = pygame_menu.Menu(500, 400, 'Welcome',theme=my_theme)
        menu.add_text_input('Name :', default='John Doe')
        menu.add_selector('Difficulty :', [('Hard', 1), ('Easy', 2)], onchange=self.set_difficulty)
        menu.add_button('Play', self.new_game)
        if(Const.DEBUG==True):
            menu.add_button('Play Testmaze', self.test_game)
        if(Const.DEBUG==True):
            menu.add_button('Play Testbattle', self.test_battle)
        menu.add_button('Quit', self.notifyQuitRequested)
        self.main_menu = menu
        #pausemenu
        menu2 = pygame_menu.Menu(300, 300, 'Pause',theme=pygame_menu.themes.THEME_GREEN)
        menu2.add_button('Continue', self.resume_game)
        menu2.add_button('Back to Start', self.main_menu)
        self.pause_menu = menu2
        self.menu = self.main_menu
        self.menu.disable()
        #self.show_MainMenu()

    def inMenu(self):
        return(self.menu.is_enabled())

    def processInput(self):
        events = pygame.event.get()
        self.menu.update(events)

    def update(self,dt):
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
        self.notifyNewGameRequested()

    def test_game(self):
        self.menu.disable()
        self.menu.reset(1)
        self.notifyNewGameRequested(MazeGenerator="TestMazeGenerator")

    def test_battle(self):
        self.menu.disable()
        self.menu.reset(1)
        self.notifyNewBattleRequested(Battle="Test")

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

