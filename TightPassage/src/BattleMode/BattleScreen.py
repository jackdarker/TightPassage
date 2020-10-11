import sys
import pygame
import pygame_menu
from src.FSM import FSM,State
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
        self.fsm = FSM(model=self,
                       states=[self.StateBeforeInit(self),self.StateInit(self),
                               self.StatePlayerSelectSkill(self),self.StatePlayerSelectTarget(self)],
                       initialState=self.StateBeforeInit.__name__)
        self.delay = 0
        self.AnimID = ""
    
    def update(self,dt):
        if(self.delay>0): 
            self.delay = self.delay -dt
            self.notifyAnimationDone(self.AnimID)
        self.fsm.checkTransition() 
        pass

    #methods called by model observer
    def OnInitBattle(self,ID):
        print("Starting Battle between")
        first =True
        for team in self.battleData.teams:
            if(first):
                print('   and   ')
                first=False
            for char in team.chars:
                print(team.get_char(char).name)
            
        self.delay=1000
        self.AnimID = ID #sys._getframe().f_code.co_name
        pass

    def OnNewTurn(self,ID):
        print("Starting Next Turn")
        chars = self.battleData.getAllChars()
        for char in chars:
            print(char.name+ ' has HP='+str(char.stats.HP))
        self.delay=1000
        self.AnimID = ID 
        pass

    def OnNextPlayerChar(self,ID):
        self.delay=-10
        self.AnimID = ID
        self.fsm.forceState(self.StatePlayerSelectSkill.__name__)
        pass

    def OnCombatAction(self,ID,actionResult):
        for effect in actionResult.effects:
            print(self.battleData.currCharacter +
                  " causes " + effect.getDescription() +
                  " on " + effect.owner.name)
        
        self.delay=100
        self.AnimID = ID 
        pass

    def OnVictory(self,ID):
        print("Congrats. You defeated all opponents.")
        self.delay=1000
        self.AnimID = ID 
        pass

    def OnDefeat(self,ID):
        print("You failed.")
        self.delay=1000
        self.AnimID = ID 
        pass

    def OnFleeing(self,ID):
        print("You retreat hastily.")
        self.delay=1000
        self.AnimID = ID 
        pass

    class StateInit(State):
        def __init__(self,battleScreen):
            super().__init__(__class__.__name__)
            self.battleScreen = battleScreen
    
        def onEnter(self):
            pass

        def checkTransition(self):
            return None

    class StateBeforeInit(State):
        def __init__(self,battleScreen):
            super().__init__(__class__.__name__)
            self.battleScreen = battleScreen
    
        def onEnter(self):
            pass

        def checkTransition(self):
            return BattleScreenConsole.StateInit.__name__

    class StatePlayerSelectSkill(State):
        """display which actor to use and let the player select a skill"""
        def __init__(self,battleScreen):
            super().__init__(__class__.__name__)
            self.battleScreen = battleScreen
            self.battleData = battleScreen.battleData
    
        def onEnter(self):
            self.battleScreen.selectedSkill = None
            self.battleScreen.selectedTarget =  None
            self.forceSkip=False
            char = self.battleData.getCharacterByID(self.battleData.currCharacter)
            if(char.isInhibited()):
                print(self.battleData.currCharacter +" cannot do anything")
                self.forceSkip=True #skip skill and targetselection
                self.battleScreen.delay=500
            else:
                print("select move for "+self.battleData.currCharacter)
                i=1
                skills =[]
                for skill in char.skills:
                    print(str(i)+': '+skill.name)
                    skills.append(skill.name)
                    i+=1
                skill= input("-->")
                if(skill.isdigit()):
                    x = int(skill)
                    skill = skills[x-1]
                self.battleScreen.selectedSkill = skill
            pass

        def checkTransition(self):
            if(self.forceSkip==True):
                return BattleScreenConsole.StateInit.__name__
            elif(self.battleScreen.selectedSkill != None):
                return BattleScreenConsole.StatePlayerSelectTarget.__name__
            return None

    class StatePlayerSelectTarget(State):
        def __init__(self,battleScreen):
            super().__init__(__class__.__name__)
            self.battleScreen = battleScreen
            self.battleData = battleScreen.battleData
    
        def onEnter(self):
            print("select target for "+self.battleScreen.selectedSkill)
            self.battleScreen.selectedTarget =  None
            skill=self.battleData.getCharacterByID(self.battleData.currCharacter).getSkillForID(self.battleScreen.selectedSkill)
            postargets = skill.targetFilter()(self.battleData.getAllChars())
            i=1
            targets =[]
            for target in postargets:
                print(str(i)+': '+target.name + ' HP=' + str(target.stats.HP)  )
                targets.append(target)
                i+=1
            print('0: back')
            target= input("-->")
            if(target.isdigit()):
                x = int(target)
                if(x==0):
                    self.battleScreen.selectedSkill =None #force return to prev state
                else:
                    x = int(target)
                    target = targets[x-1]
            self.battleScreen.selectedTarget=[target]
            pass

        def checkTransition(self):
            if(self.battleScreen.selectedSkill ==None):
                return BattleScreenConsole.StatePlayerSelectSkill.__name__
            elif(self.battleScreen.selectedTarget != None):
                self.battleScreen.battleController.selectSkillForCharacter(self.battleData.currCharacter,self.battleScreen.selectedSkill,self.battleScreen.selectedTarget)
                self.battleScreen.notifyAnimationDone(self.battleScreen.AnimID)
                return BattleScreenConsole.StateInit.__name__
            return None

class SkillRenderData():
    """a data container to transfer data from controller to the view
    contains a collection: damage dealt, applied effect, used skill
    the view is responsible to display the information in a proper way, f.e. updating healthbars, skillanimation
    """
    def __init__(self,skillResult):
        self.data = skillResult
        pass
