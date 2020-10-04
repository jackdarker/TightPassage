import sys
import pygame
import pygame_menu
import src.Const as Const

class BattleScreen():
    """implements the view for a battle"""

    def __init__(self,screen,state,battleController):
        self.__observers = []
        self.battleController = battleController
        self.battleData = battleController.battleData
        self.battleData.addObserver(self)   #recevie notification on modelchange
        if(screen==None): return 
        self.menu_screen = screen.copy()
        self.menu_screen.fill((0, 0, 0, 200))
        self.menu_screen.set_alpha(100) #why does fill with RGB+alpha not work?
        self.menu = None
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

    def _skillSelected(self):
        pass
    
    

    #using observer to send data to the controller
    def addObserver(self, observer):
        self.__observers.append(observer)

    def removeObserver(self, observer):
        if(self.__observers.count(observer)):
            self.__observers.remove(observer)

    def notifyAnimationDone(self,ID):
        for observer in self.__observers:
            observer.OnAnimationDone(ID)

class BattleScreenConsole(BattleScreen):
    """using text console for testing purpose
    """
    def __init__(self,screen,state,battleController):
        super().__init__(screen,state,battleController)
        self.delay = 0
        self.AnimID = ""
    
    def update(self,dt):
        if(self.delay>0): 
            self.delay = self.delay -dt
            self.notifyAnimationDone(self.AnimID)
        pass

    #methods called by model observer
    def OnInitBattle(self,ID):
        print("Starting Battle")
        
        for team in self.battleData.teams:
            for char in team.chars:
                print(team.get_char(char).name)
            print('   against   ')
        
        self.delay=1000
        self.AnimID = ID #sys._getframe().f_code.co_name
        pass

    def OnNewTurn(self,ID):
        print("Starting Next Turn")        
        self.delay=1000
        self.AnimID = ID 
        pass

    def OnNextPlayerChar(self,ID):
        print("select move for "+self.battleData.currCharacter)
        i=1
        skills =[]
        for skill in self.battleData.getCharacterByID(self.battleData.currCharacter).skills:
            print(str(i)+': '+skill.name)
            skills.append(skill.name)
        skill= input("-->")
        if(skill.isdigit()):
            x = int(skill)
            skill = skills[x-1]
        print("select target for "+skill)

        self.battleController.selectSkillForCharacter(self.battleData.currCharacter,skill)
        self.delay=10
        self.AnimID = ID 
        pass

    def OnCombatAction(self,ID):
        print("move for "+self.battleData.currCharacter)
        
        self.delay=100
        self.AnimID = ID 
        pass