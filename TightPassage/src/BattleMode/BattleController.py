import pygame
from src.FSM import FSM,State
import src.Const as Const

class BattleController():
    """contains the logic of the battlesystem
    executes commands on the data
    triggers updates of view
    receives commands from view
    """
    def __init__(self,gameState,battleData):
        self.battleData = battleData
        self.AnimationDone = {}
        self.fsm = FSM(model=self,
                       states=[StateBeforeInit(self),StateInit(self),StateCheckDefeat(self),StateNewTurn(self),
                          StateCombatantSelection(self),StateCombatantAction(self),
                          StateTurnEnd(self),StatePlayerLoss(self),StatePlayerVictory(self),
                          StateDeinit(self)],
                       initialState=StateBeforeInit.__name__)
        pass

    def update(self,dt):
        self.fsm.checkTransition()  #todo we dont need to poll this on every cycle

    def selectSkillForCharacter(self,charname,skillname):
        self.battleData.getCharacterByID(charname).skillInNextTurn = skillname

    def isPlayerDefeated(self):
        #is playerteam defeated?
        return False

    def isOpponentDefeated(self):
        #is other team defeated?
        return False

    #methods called by view via observer
    def OnAnimationDone(self,ID):
        self.AnimationDone[ID]=True


class StateBeforeInit(State):
    def __init__(self,battleController):
        super().__init__(__class__.__name__)
        self.controller = battleController
    
    def onEnter(self):
        pass

    def checkTransition(self):
        return StateInit.__name__

class StateInit(State):
    AnimID = hash('OnInitBattle')

    def __init__(self,battleController):
        super().__init__(__class__.__name__)
        self.controller = battleController
    
    def onEnter(self):
        self.controller.AnimationDone[StateInit.AnimID]=False
        self.controller.battleData.notifyOnInitBattle(StateInit.AnimID)
        pass

    def checkTransition(self):
        if(self.controller.AnimationDone[StateInit.AnimID]==True):
            return StateCheckDefeat.__name__
        return None

class StateCheckDefeat(State):
    def __init__(self,battleController):
        super().__init__(__class__.__name__)
        self.controller = battleController

    def onEnter(self):
        pass

    def checkTransition(self):
        #evaluate if team is defeated and switch to postBattleScene
        if(self.controller.isPlayerDefeated()):
            return StatePlayerLoss.__name__
        elif(self.controller.isOpponentDefeated()):
            return StatePlayerVictory.__name__
        else:   return StateNewTurn.__name__

class StateNewTurn(State):
    AnimID = hash('OnNewTurn')
    def __init__(self,battleController):
        super().__init__(__class__.__name__)
        self.controller = battleController

    def onEnter(self):
        #notify that new turn starts
        self.controller.battleData.nextTurn()
        self.controller.AnimationDone[__class__.AnimID]=False
        self.controller.battleData.notifyOnNewTurn(__class__.AnimID)
        #trigger preTurn-Handling of teams to apply statuseffect

        #determine turn-order
        self.controller.battleData.nextCharacter()
        pass

    def checkTransition(self):
        if(self.controller.AnimationDone[__class__.AnimID]==True):
            return StateCombatantSelection.__name__
        return None

class StateCombatantSelection(State):
    AnimID = hash('OnNextPlayerChar')
    def __init__(self,battleController):
        super().__init__(__class__.__name__)
        self.controller = battleController

    def onEnter(self):
        #notify about combatant change
        char = self.controller.battleData.getCharacterByID(self.controller.battleData.currCharacter)
        #if playercontrolled selectSkillAndTarget by View
        if(char.AI==None):
            self.controller.AnimationDone[__class__.AnimID]=False
            self.controller.battleData.notifyOnNextPlayerChar(__class__.AnimID)
        else:#if AIcontrolled selectSkillAndTarget by AI
            pass
        
        pass

    def checkTransition(self):
        #wait until combatant selected his move
        if(self.controller.AnimationDone[__class__.AnimID]==True):
            self.controller.battleData.nextCharacter()
            #if there are more combatants switch to the next one
            if(not self.controller.battleData.finishTurn ):
                return StateCombatantSelection.__name__
            else:
                #otherwise execute move
                return StateCombatantAction.__name__

class StateCombatantAction(State):
    AnimID = hash('OnCombatAction')

    def __init__(self,battleController):
        super().__init__(__class__.__name__)
        self.controller = battleController

    def onEnter(self):
        #execute skill
        self.controller.AnimationDone[__class__.AnimID]=False
        self.controller.battleData.notifyOnCombatAction(__class__.AnimID)
        pass

    def checkTransition(self):
        #wait until view animation is done
        if(self.controller.AnimationDone[__class__.AnimID]==True):
            #maybe remove dead chars from combatants
            #if there are more combatants switch to the next one
            return StateCombatantAction.__name__

            #otherwise end turn
            return StateTurnEnd.__name__

class StateTurnEnd(State):
    def __init__(self,battleController):
        super().__init__(__class__.__name__)
        self.controller = battleController

    def onEnter(self):
        self.controller.battleData.notifyOnNewTurn()
        pass

    def checkTransition(self):
        #start next cycle
        return StateCheckDefeat.__name__

class StatePlayerLoss(State):
    def __init__(self,battleController):
        super().__init__(__class__.__name__)
        self.controller = battleController

    def onEnter(self):
        #show defeat screen
        pass

    def checkTransition(self):
        #wait until confirmation, then terminate
        return StateDeinit.__name__

class StatePlayerVictory(State):
    def __init__(self,battleController):
        super().__init__(__class__.__name__)
        self.controller = battleController

    def onEnter(self):
        #show win screen
        pass

    def checkTransition(self):
        #wait until confirmation, then terminate
        return StateDeinit.__name__

class StateDeinit(State):
    def __init__(self,battleController):
        super().__init__(__class__.__name__)
        self.controller = battleController

    def onEnter(self):
        #trigger the termination of BattleMode
        pass

    def checkTransition(self):
        return ''

class BattleData():
    """datamodel of a battle
    only the controller should change the data, not the view
    """

    def __init__(self):
        self.__observers = []
        self.teams=[]
        self.arena = None
        self.turn = -1
        self.newTurn = False
        self.finishTurn = False
        self.currCharacter = None
        self.turnOrder = []
        pass

    def nextTurn(self):
        self.currCharacter = ''
        self.turn += 1
        self.newTurn = True
        self.finishTurn = False

    def nextCharacter(self):
        """this will select the next charcter according turn order as the current character
        if turn order wasnt estimated yet, it will be calculated first
        """
        if(self.newTurn and self.turnOrder==[]):
            self.newTurn = False
            for team in self.teams:                     #todo depends on agility aand surprise?
                for char in team.chars:
                    self.turnOrder.append(char)
        if(len(self.turnOrder)>0):
            self.currCharacter = self.turnOrder.pop(0)
        else:
            self.currCharacter = ''
            self.finishTurn = True
        pass

    def getCharacterByID(self,name):
        for team in self.teams:
            char = team.get_char(name)
            if(char!=None):
                return char
        return None

    def addObserver(self, observer):
        self.__observers.append(observer)

    def removeObserver(self, observer):
        if(self.__observers.count(observer)):
            self.__observers.remove(observer)

    def notifyOnInitBattle(self,ID):
        for observer in self.__observers:
            observer.OnInitBattle(ID)

    def notifyOnNewTurn(self,ID):
        for observer in self.__observers:
            observer.OnNewTurn(ID)

    def notifyOnNextPlayerChar(self,ID):
        for observer in self.__observers:
            observer.OnNextPlayerChar(ID)

class Arena():
    """defines the arena whee you are battling"""
    def __init__(self):
        self.bgImage = None