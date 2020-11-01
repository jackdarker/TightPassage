import sys
import pygame
import time
import random
from pygame.locals import *
import src.Const as Const
#import pygame_menu
from src.FSM import FSM,State
from src.UI.Controls import *
from src.UI.pgu.pgu import gui

class BattleScreen():
    """implements the view for a battle"""

    @staticmethod
    def renderTextCenteredAt(text, font, colour, x, y, screen, allowed_width):
        # first, split the text into words
        words = text.split()

        # now, construct lines out of these words
        lines = []
        while len(words) > 0:
            # get as many words as will fit within allowed_width
            line_words = []
            while len(words) > 0:
                line_words.append(words.pop(0))
                fw, fh = font.size(' '.join(line_words + words[:1]))
                if fw > allowed_width:
                    break

            # add a line consisting of those words
            line = ' '.join(line_words)
            lines.append(line)

        # now we've split our text into lines that fit into the width, actually
        # render them

        # we'll render each line below the last, so we need to keep track of
        # the culmative height of the lines we've rendered so far
        y_offset = 0
        for line in lines:
            fw, fh = font.size(line)

            # (tx, ty) is the top-left of the font surface
            tx = x - fw / 2
            ty = y + y_offset

            font_surface = font.render(line, True, colour)
            screen.blit(font_surface, (tx, ty))

            y_offset += fh
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
        
        self._setupHud()
        

        self.font = pygame.font.Font(pygame.font.get_default_font(),36)

        self.message = ""
        self.delay = 0
        self.AnimID = ""
        self.fsm = FSM(model=self,
                               states=[self.StateBeforeInit(self),self.StateInit(self),
                                       self.StatePlayerSelectSkill(self),self.StatePlayerSelectTarget(self)],
                               initialState=self.StateBeforeInit.__name__)
    
    def _setupHud(self):
        self.form = gui.Form()
        themetouse = "default" #Const.resource_path("assets/pgu_themes/yellow")
        self.app = gui.App(theme=gui.Theme(themetouse))
        #the container for the widhgets
        c = gui.Table(align=-1,valign=1)
        tabsheetHeight =0   #240
        #grid with buttons
        tbSkills = gui.Table()
        tbSkills.style.width = Const.WINDOW_SIZE[0]-20
        tbSkills.style.height = tabsheetHeight
        #tbSkills.tr()
        #tbSkills.td(gui.Label("Skills",color=Const.YELLOW),colspan=2)

        tbSkills.tr()
        bt = IconButton("Clickdfsdgffdgdgf 1 Me!")
        #bt.connect(gui.KEYDOWN, resizeMe, bt)
        tbSkills.td(bt,align=-1)
        tbSkills.tr()
        bt = IconButton("Click  2 Me!")
        #bt.connect(gui.CLICK, resizeMe, bt)
        tbSkills.td(bt,align=-1)
        tbSkills.tr()
        bt = IconButton("Click      3 Me!")
        #bt.connect(gui.CLICK, resizeMe,bt)
        tbSkills.td(bt,align=-1)
        self.tbSkills =tbSkills

        #another grid with buttons
        tbItems = gui.Table()
        tbItems.style.width = Const.WINDOW_SIZE[0]-20
        tbItems.style.height = tabsheetHeight
        for i in range(0,5):
            tbItems.tr()
            for i in range(0,3):
                bt = IconButton("---")
                bt.disabled=True
                #bt.connect(gui.KEYDOWN, resizeMe, bt)
                tbItems.td(bt,align=-1)
        self.tbItems =tbItems
        if(True):
            tablabels = Tabsheet(tabContent = {'Skills': self.tbSkills,'Items':self.tbItems})
        else:
            #creates a tab; buttons are used to switch tabs
            self.tabs = gui.Group()
            self.tabs.connect(gui.CHANGE,tab)
            tablabels = gui.Table()
            tablabels.tr()
            #when the toolbutton is pressed it will call gui.CHANGE->tab() and this will switchout the boxwidget with c,t or d
            b = gui.Tool(self.tabs,gui.Label("Skills"),self.tbSkills)    
            tablabels.td(b)
            tablabels.tr()
            b = gui.Tool(self.tabs,gui.Label("Items"),self.tbItems)
            tablabels.td(b)
            tablabels.tr()
            b = gui.Tool(self.tabs,gui.Label("Magic"),self.tbSkills)
            tablabels.td(b)
            #the following widget will be switched out when pressing on the tablabels
            #tablabels.tr()
            spacer = gui.Spacer(Const.WINDOW_SIZE[0]-20,240)
            self.box = gui.ScrollArea(spacer,height=spacer.rect[1])
            tablabels.td(self.box,row=0,col=1,style={'border':1},rowspan=3)
            tablabels.tr()

        self.Log = Textlog(width=Const.WINDOW_SIZE[0],height=300)
        c.tr()
        c.add(self.Log)#,20,0)
        c.tr()
        c.add(tablabels)#,0,200)

        self.app.init(c)
        pass

    def scrap_pgutest():
        #font = pygame_menu.font.FONT_OPEN_SANS
        #my_theme = pygame_menu.themes.THEME_SOLARIZED.copy()
        #my_theme.widget_font=font
        #menu = pygame_menu.Menu(300, 400, 'Battle',theme=my_theme,columns=2,rows=4)
        #menu.enable()
        #id = 0
        #id = menu.add_button('Continue', self.setTitle,id).get_id()
        #id = menu.add_button('Continue2', self.setTitle,id).get_id()
        #id = menu.add_button('Continue3', self.setTitle,id).get_id()
        #id = menu.add_button('Continue4', self.setTitle,id).get_id()
        #id = menu.add_button('Continue5', self.setTitle,id).get_id()
        #id = menu.add_button('Continue6', self.setTitle,id).get_id()#
        #self.menu = menu
        #def setTitle(self,id):
        #   self.menu.get_widget(id).set_title('sdf')
        #pass
        #tbSkills.resize()
        #tbSkills.repaint()
        #tbSkills.add("item ",value=0)
        #tbSkills.add("item2 ",value=1)
        #tbSkills.add("item3 ",value=2)
        #tbSkills.add("item2 ",value=1)
        #tbSkills.add("item3 ",value=2)
        #tbSkills.add("item2 ",value=1)
        #tbSkills.add("item3 ",value=2)
        pass

    #methods called by model observer
    def OnInitBattle(self,ID):
        self.message = ("Starting Battle between")
        first =True
        for team in self.battleData.teams:
            if(not first):
                self.message +=('   and   ')
            first=False
            for char in team.chars:
                self.message +=(team.get_char(char).name+(', '))
        self.message = self.message #__class__.wrap_words_to_fit(self.message,1.0,300)
        self.Log.set_text(self.message)
        self.delay=1000
        self.AnimID = ID #sys._getframe().f_code.co_name
        pass

    def OnNewTurn(self,ID):
        self.Log.set_text("Starting Next Turn")
        chars = self.battleData.getAllChars()
        for char in chars:
            self.Log.set_text(char.name+ ' has HP='+str(char.stats.HP))
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
            self.Log.set_text(self.battleData.currCharacter +
                  " causes " + effect.getDescription() +
                  " on " + effect.owner.name)
        
        self.delay=100
        self.AnimID = ID 
        pass

    def OnVictory(self,ID):
        self.Log.set_text("Congrats. You defeated all opponents.")
        self.delay=1000
        self.AnimID = ID 
        pass

    def OnDefeat(self,ID):
        self.Log.set_text("You failed.")
        self.delay=1000
        self.AnimID = ID 
        pass

    def OnFleeing(self,ID):
        self.Log.set_text("You retreat hastily.")
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
                self.battleScreen.Log.set_text(self.battleData.currCharacter +" cannot do anything")
                self.forceSkip=True #skip skill and targetselection
                self.battleScreen.delay=500
            else:
                self.battleScreen.Log.set_text("select move for "+self.battleData.currCharacter)
                return
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
            self.battleScreen.Log.set_text("select target for "+self.battleScreen.selectedSkill)
            self.battleScreen.selectedTarget =  None
            skill=self.battleData.getCharacterByID(self.battleData.currCharacter).getSkillForID(self.battleScreen.selectedSkill)
            postargets = skill.targetFilter()(self.battleData.getAllChars())
            i=1
            targets =[]
            for target in postargets:
                print(str(i)+': '+target.name + ' HP=' + str(target.stats.HP)  )
                targets.append(target)
                i+=1
            self.battleScreen.Log.set_text('0: back')
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
        #if(self.menu.is_enabled()):
        #    self.menu.update(events)
        #else:
        for e in events:   #pgu gui update
            self.app.event(e)

    def update(self,dt):
        if(self.delay>0): 
            self.delay = self.delay -dt
            self.notifyAnimationDone(self.AnimID)
        self.fsm.checkTransition() 
        pass
        
    def render(self, window):
        #fill with black
        self.screen = window.copy()
        self.screen.fill((0, 0, 0, 200))
        self.screen.set_alpha(100) #why does fill with RGB+alpha not work?
        #render background
        window.blit(self.screen,(0,0))
        #window.blit(self.battleData.arena.bgImage)

        #if(self.message != ''):
        x = (window.get_width()) // 2
        y = (window.get_height()) // 2
        __class__.renderTextCenteredAt(self.message, self.font, Const.WHITE, x, y, window, 200)

        #render teams

        #render menu
        #if (self.menu.is_enabled()):
        #    self.menu.draw(window)
        self.app.paint(window) #pgu gui update

    def showSkillMenu(self):
        self.menu.add_button('Attack', self._skillSelected)

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
