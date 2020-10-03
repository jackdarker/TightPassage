import enum
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
        self.fsm = FSM(model=self,
                       states=[StateInit(self),StateCheckDefeat(self),StateNewTurn(self),
                          StateCombatantSelection(self),StateCombatantAction(self),
                          StateTurnEnd(self),StatePlayerLoss(self),StatePlayerVictory(self),
                          StateDeinit(self)],
                       initial=StateInit.__name__)
        pass

    def update(self,dt):
        self.fsm.checkTransition()  #todo we dont need to poll this on every cycle

    def isPlayerDefeated(self):
        #is playerteam defeated?
        return False

    def isOpponentDefeated(self):
        #is other team defeated?
        return False

class StateInit(State,battleController):
    def __init__(self):
        super().__init__(__class__.__Name__)
        self.controller = battleController
    
    def onEnter(self):
        pass

    def checkTransition(self):
        return StateCheckDefeat.__name__

class StateCheckDefeat(State):
    def __init__(self,battleController):
        super().__init__(__class__.__Name__)
        self.controller = battleController

    def onEnter(self):
        pass

    def checkTransition(self):
        #evaluate if team is defeated and switch to postBattleScene
        if(self.controller.isPlayerDefeated()):
            return StatePlayerLoss.__Name__
        elif(self.controller.isOpponentDefeated()):
            return StatePlayerVictory.__Name__
        else:   return StateNewTurn.__name__

class StateNewTurn(State):
    def __init__(self,battleController):
        super().__init__(__class__.__Name__)
        self.controller = battleController

    def onEnter(self):
        #notify that new turn starts

        #trigger preTurn-Handling of teams to apply statuseffect

        #determine turn-order
        pass

    def checkTransition(self):
        return StateCombatantSelection.__Name__

class StateCombatantSelection(State):
    def __init__(self,battleController):
        super().__init__(__class__.__Name__)
        self.controller = battleController

    def onEnter(self):
        #notify about combatant change
        #if playercontrolled selectSkillAndTarget by View

        #if AIcontrolled selectSkillAndTarget by AI
        pass

    def checkTransition(self):
        #wait until combatant selected his move

        #if there are more combatants switch to the next one
        return StateCombatantSelection.__Name__

        #otherwise execute move
        return StateCombatantAction.__Name__

class StateCombatantAction(State):
    def __init__(self,battleController):
        super().__init__(__class__.__Name__)
        self.controller = battleController

    def onEnter(self):
        #execute skill
        pass

    def checkTransition(self):
        #wait until view animation is done
        #maybe remove dead chars from combatants
        #if there are more combatants switch to the next one
        return StateCheckDefeat.__Name__

        #otherwise end turn
        return StateTurnEnd.__Name__

class StateTurnEnd(State):
    def __init__(self,battleController):
        super().__init__(__class__.__Name__)
        self.controller = battleController

    def onEnter(self):
        pass

    def checkTransition(self):
        #start next cycle
        return StateCheckDefeat.__Name__

class StatePlayerLoss(State):
    def __init__(self,battleController):
        super().__init__(__class__.__Name__)
        self.controller = battleController

    def onEnter(self):
        #show defeat screen
        pass

    def checkTransition(self):
        #wait until confirmation, then terminate
        return StateDeinit.__Name__

class StatePlayerVictory(State):
    def __init__(self,battleController):
        super().__init__(__class__.__Name__)
        self.controller = battleController

    def onEnter(self):
        #show win screen
        pass

    def checkTransition(self):
        #wait until confirmation, then terminate
        return StateDeinit.__Name__

class StateDeinit(State):
    def __init__(self,battleController):
        super().__init__(__class__.__Name__)
        self.controller = battleController

    def onEnter(self):
        #trigger the termination of BattleMode
        pass

    def checkTransition(self):
        return ''

class BattleData():
    """datamodel of a battle"""

    def __init__(self):
        self.teams=[]
        self.arena = None
        self.turn = 0
        pass

class Arena():
    """defines the arena whee you are battling"""
    def __init__(self):
        self.bgImage = None