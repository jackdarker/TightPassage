import pygame
from src.FSM import FSM,State
import src.Const as Const
from src.BattleMode.BattleScreen import SkillRenderData
from src.Components.Skill import SkillResult
from src.Components.SkillDB import *

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
                          StateTurnEnd(self),
                          StatePlayerLoss(self),StatePlayerVictory(self),StatePlayerFlee(self),
                          StateDeinit(self)],
                       initialState=StateBeforeInit.__name__)
        pass

    def update(self,dt):
        self.fsm.checkTransition()  #todo we dont need to poll this on every cycle

    def selectSkillForCharacter(self,charname,skillname,targets):
        char =self.battleData.getCharacterByID(charname)
        char.skillInNextTurn = skillname
        char.skillTarget = targets

    def isTeamDefeated(self,faction, invers=False):
        #is playerteam/other team defeated?
        defeat = False
        for team in self.battleData.teams:
            if((team.faction != faction and invers==False) or
               (team.faction == faction and invers==True)): break
            defeat = True
            for char in team.chars:
                defeat = defeat and (team.get_char(char).stats.HP<=0)
        return defeat

    def isTeamFleeing(self,faction, invers=False):
        #is playerteam/other team defeated?
        for team in self.battleData.teams:
            if((team.faction != faction and invers==False) or
               (team.faction == faction and invers==True)): break
            for char in team.chars:
                for effect in team.get_char(char).effects:
                    if( type(effect) == EffFlee):
                        return True
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
        self.controller
        if(self.controller.isTeamFleeing('Player')):
            return StatePlayerFlee.__name__
        elif(self.controller.isTeamDefeated('Player')):
            return StatePlayerLoss.__name__
        elif(self.controller.isTeamDefeated('Player',invers=True)):
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
                self.controller.battleData.resetNextCharacter() #reset iterator since looping again in next state
                self.controller.battleData.nextCharacter()
                return StateCombatantAction.__name__
        pass

class StateCombatantAction(State):
    AnimID = hash('OnCombatAction')

    def __init__(self,battleController):
        super().__init__(__class__.__name__)
        self.controller = battleController

    def onEnter(self):
        #execute skill
        self.controller.AnimationDone[__class__.AnimID]=False
        char = self.controller.battleData.getCharacterByID(self.controller.battleData.currCharacter)
        #maybe remove dead chars from combatants
        move = self.controller.battleData.calculateSkillResult(char)
        self.controller.battleData.applySkillResult(move)
        self.controller.battleData.notifyOnCombatAction(__class__.AnimID, move)
        pass

    def checkTransition(self):
        #wait until view animation is done
        if(self.controller.AnimationDone[__class__.AnimID]==True):
            #if there are more combatants switch to the next one
            self.controller.battleData.nextCharacter()
            if(not self.controller.battleData.finishTurn ):
                #if there are more combatants switch to the next one
                return StateCombatantAction.__name__

            #otherwise end turn
            return StateTurnEnd.__name__
        pass

class StateTurnEnd(State):
    AnimID = hash('OnTurnEnd')
    def __init__(self,battleController):
        super().__init__(__class__.__name__)
        self.controller = battleController

    def onEnter(self):
        #self.controller.battleData.notifyOnTurnDone(__class__.AnimID)
        pass

    def checkTransition(self):
        #start next cycle
        return StateCheckDefeat.__name__
    pass

class StatePlayerLoss(State):
    AnimID = hash('OnDefeat')
    def __init__(self,battleController):
        super().__init__(__class__.__name__)
        self.controller = battleController

    def onEnter(self):
        #self.battleData..postBattle(playerdefeat=True)
        #show defeat screen
        self.controller.AnimationDone[__class__.AnimID]=False
        self.controller.battleData.notifyOnDefeat(__class__.AnimID)
        pass

    def checkTransition(self):
        #wait until confirmation, then terminate
        if(self.controller.AnimationDone[__class__.AnimID]==True):
            return StateDeinit.__name__
        pass

class StatePlayerVictory(State):
    AnimID = hash('OnVictory')
    def __init__(self,battleController):
        super().__init__(__class__.__name__)
        self.controller = battleController

    def onEnter(self):
        #self.battleData..postBattle(playerdefeat=False)
        #show win screen
        self.controller.AnimationDone[__class__.AnimID]=False
        self.controller.battleData.notifyOnVictory(__class__.AnimID)
        pass

    def checkTransition(self):
        #wait until confirmation, then terminate
        if(self.controller.AnimationDone[__class__.AnimID]==True):
            return StateDeinit.__name__
        pass

class StatePlayerFlee(State):
    AnimID = hash('OnFleeing')
    def __init__(self,battleController):
        super().__init__(__class__.__name__)
        self.controller = battleController

    def onEnter(self):
        #self.battleData.postBattle(playerflee=True)
        #show flee screen
        self.controller.AnimationDone[__class__.AnimID]=False
        self.controller.battleData.notifyOnFleeing(__class__.AnimID)
        pass

    def checkTransition(self):
        #wait until confirmation, then terminate
        if(self.controller.AnimationDone[__class__.AnimID]==True):
            return StateDeinit.__name__
        pass

class StateDeinit(State):
    def __init__(self,battleController):
        super().__init__(__class__.__name__)
        self.controller = battleController

    def onEnter(self):
        #trigger the termination of BattleMode
        self.battleData.finishBattle = False
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
        self.finishBattle = False
        pass

    def nextTurn(self):
        self.currCharacter = ''
        self.turnOrder=[]
        self.turnOrderIdx = 0
        self.turn += 1
        self.newTurn = True
        self.finishTurn = False

    def resetNextCharacter(self):
        self.finishTurn = False
        self.turnOrderIdx = 0

    def nextCharacter(self):
        """this will select the next charcter according turn order as the current character
        if turn order wasnt estimated yet, it will be calculated first
        """
        if(self.newTurn and self.turnOrder==[]):
            self.newTurn = False
            for team in self.teams:                     #todo depends on agility aand surprise?
                for char in team.chars:
                    self.turnOrder.append(char)
        if(self.turnOrderIdx)<len(self.turnOrder):
            self.currCharacter = self.turnOrder[self.turnOrderIdx]
            self.turnOrderIdx+=1
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

    def calculateSkillResult(self, char):
        """calculates the effect of an skill without applying it
        """
        res = SkillResult()
        if(char.isInhibited()):
            return res
        skill = char.getSkillForID(char.skillInNextTurn)
        targets = char.skillTarget
        if(skill != None and len(targets)>0):
            res = skill.previewCast(targets)
            
        return res
        pass

    def applySkillResult(self, result):
        """applys the previous calculated effect
        """
        if(result.success==True):
            for effect in result.effects:
                effect.on_apply()
        pass

    def getAllChars(self):
        chars = []
        for team in self.teams:
            for char in team.chars:
                chars.append(team.get_char(char))
        return chars

    def getTeamForCharacterName(self,name):
        for team in self.teams:
            char = team.get_char(name)
            if(char!=None):
                return team
        return None

    #def getEnemysForCharacterName(self,name):
    #    for team in self.teams:
    #        char = team.get_char(name)
    #        if(char==None):
    #            return team
    #    return None

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

    def notifyOnCombatAction(self,ID,ActionResult):
        for observer in self.__observers:
            observer.OnCombatAction(ID,ActionResult)

    def notifyOnVictory(self,ID):
        for observer in self.__observers:
            observer.OnVictory(ID)

    def notifyOnFleeing(self,ID):
        for observer in self.__observers:
            observer.OnFleeing(ID)

    def notifyOnDefeat(self,ID):
        for observer in self.__observers:
            observer.OnDefeat(ID)

class Arena():
    """defines the arena whee you are battling"""
    def __init__(self):
        self.bgImage = None