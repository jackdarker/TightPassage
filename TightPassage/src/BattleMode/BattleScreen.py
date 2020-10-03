import pygame
import pygame_menu
import src.Const as Const

class BattleScreen():
    """implements the view for a battle"""

    def __init__(self,screen,state,battleData):
        super().__init__(state)
        self.menu_screen = screen.copy()
        self.menu_screen.fill((0, 0, 0, 200))
        self.menu_screen.set_alpha(100) #why does fill with RGB+alpha not work?
        self.menu = None
        self.battleData = battleData
        font = pygame_menu.font.FONT_OPEN_SANS
        my_theme = pygame_menu.themes.THEME_SOLARIZED.copy()
        my_theme.widget_font=font
        menu = pygame_menu.Menu(500, 400, 'Battle',theme=my_theme)

    def processInput(self,events):
        self.menu.update(events)

    def update(self,dt):
        pass
        
    def render(self, window):
        #render background
        window.blit(self.battleData.arena.bgImage)
        #render teams

        #render menu
        if (self.menu.is_enabled()):
            window.blit(self.menu_screen,(0,0))
            self.menu.draw(window)

    def showSkillMenu(self):
        menu.add_button('Attack', self._skillSelected)

    def _skillSelected(self)