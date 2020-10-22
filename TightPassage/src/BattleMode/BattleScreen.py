import sys
import pygame
import pygame_menu
from src.FSM import FSM,State
import src.Const as Const

class BattleScreen():
    """implements the view for a battle"""

    @staticmethod
    def wrap_words_to_fit(text, scale, width, x_kerning=0):
        split_on_newlines = text.split("\n")
        if len(split_on_newlines) > 1:
            """if it's got newlines, split it, call this method again, and re-combine"""
            wrapped_substrings = []
            for line in split_on_newlines:
                wrapped_substrings.append(TextImage.wrap_words_to_fit(line, scale, width, x_kerning=x_kerning))

            return "\n".join(wrapped_substrings)

        text = text.replace("\n", " ")  # shouldn't be any at this point, but just to be safe~
        words = text.split(" ")
        lines = []
        cur_line = []

        while len(words) > 0:
            if len(cur_line) == 0:
                cur_line.append(words[0])
                words = words[1:]

            if len(words) == 0:
                lines.append(" ".join(cur_line))
                cur_line.clear()

            elif TextImage.calc_width(" ".join(cur_line + [words[0]]), scale, x_kerning=x_kerning) > width:
                lines.append(" ".join(cur_line))
                cur_line.clear()

            elif len(words) > 0:
                cur_line.append(words[0])
                words = words[1:]
                if len(words) == 0:
                    lines.append(" ".join(cur_line))

        return "\n".join(lines)

    def __init__(self,state,battleController):
        self.__observers = []
        
        self.battleController = battleController
        self.battleData = battleController.battleData
        self.battleData.addObserver(self)   #recevie notification on modelchange
        
        font = pygame_menu.font.FONT_OPEN_SANS
        my_theme = pygame_menu.themes.THEME_SOLARIZED.copy()
        my_theme.widget_font=font
        menu = pygame_menu.Menu(500, 400, 'Battle',theme=my_theme)
        menu.enabled = False
        self.font = pygame.font.Font(pygame.font.get_default_font(),36)
        self.message = ""
        self.menu = menu
        self.delay = 0
        self.AnimID = ""
        self.fsm = FSM(model=self,
                               states=[self.StateBeforeInit(self),self.StateInit(self),
                                       self.StatePlayerSelectSkill(self),self.StatePlayerSelectTarget(self)],
                               initialState=self.StateBeforeInit.__name__)

    

    #methods called by model observer
    def OnInitBattle(self,ID):
        self.message = ("Starting Battle between")
        first =True
        for team in self.battleData.teams:
            if(first):
                self.message +=('   and   ')
                first=False
            for char in team.chars:
                self.message +=(team.get_char(char).name)
        self.message = __class__.wrap_words_to_fit(self.message,1.0,300)
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

    class StateBeforeInit(State):
        def __init__(self,battleScreen):
            super().__init__(__class__.__name__)
            self.battleScreen = battleScreen
    
        def onEnter(self):
            pass

        def checkTransition(self):
            return BattleScreenConsole.StateInit.__name__
    
    class StateInit(State):
        def __init__(self,battleScreen):
            super().__init__(__class__.__name__)
            self.battleScreen = battleScreen
    
        def onEnter(self):
            pass

        def checkTransition(self):
            return None
    
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

    def processInput(self,events):
        self.menu.update(events)

    def update(self,dt):
        if(self.delay>0): 
            self.delay = self.delay -dt
            self.notifyAnimationDone(self.AnimID)
        self.fsm.checkTransition() 
        pass
        
    def render(self, window):
        if(self.message != ''):
            surface = self.font.render(self.message, True, (200, 0, 0))
            x = (window.get_width() - surface.get_width()) // 2
            y = (window.get_height() - surface.get_height()) // 2
            window.blit(surface, (x, y))
        if(self.menu.is_enabled()):
            self.menu_screen = window.copy()
            self.menu_screen.fill((0, 0, 0, 200))
            self.menu_screen.set_alpha(100) #why does fill with RGB+alpha not work?
        
        #render background
        #window.blit(self.battleData.arena.bgImage)
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
    def __init__(self,state,battleController):
        super().__init__(state,battleController)
        self.fsm = FSM(model=self,
                       states=[self.StateBeforeInit(self),self.StateInit(self),
                               self.StatePlayerSelectSkill(self),self.StatePlayerSelectTarget(self)],
                       initialState=self.StateBeforeInit.__name__)

    

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



    class StateBeforeInit(State):
        def __init__(self,battleScreen):
            super().__init__(__class__.__name__)
            self.battleScreen = battleScreen
    
        def onEnter(self):
            pass

        def checkTransition(self):
            return BattleScreenConsole.StateInit.__name__
    
    class StateInit(State):
        def __init__(self,battleScreen):
            super().__init__(__class__.__name__)
            self.battleScreen = battleScreen
    
        def onEnter(self):
            pass

        def checkTransition(self):
            return None
    
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
