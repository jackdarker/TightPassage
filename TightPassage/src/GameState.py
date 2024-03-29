import pygame
from src.Vector import Vector2
from src.Components.StatEngine import *
import src.Support as Support

class GameStateObserver():

    def sceneTriggered(self,scene):
        pass

    def battleTriggered(self,scene):
        pass

    def warpTriggered(self,warp):
        pass

    def bulletFired(self,unit):
        pass

    def unitDestroyed(self,unit):
        pass

class GameState():
    """Holds all the data of the game
        a Singleton to store Leveldata"""
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(GameState, cls).__new__(cls)
            # Put any initialization here.
            cls._instance.reset()
        return cls._instance


    def reset(self):
        self.worldSize = Vector2(16,16) #todo is screensize in tiles
        self.observers = [ ]
        self.inGame = False
        #actual room vars
        self.units = []
        self.shoots = pygame.sprite.Group()
        self.obstacles = []
        self.doors = []
        self._player = None
        self.players = []
        self.fileName = ""
        self.playerSpawn = None
        #maze vars
        self.mazeGenerator = None
        self.mazeNodes = []
        self.currentMazeNode = None
        #battlevars
        self.battleData = None
        self.StatEngine = StatEngine("Game")

    @property
    def player(self):
        return self._player

    @player.setter
    def player(self, val):
        self._player=val
        if(len(self.players)==0):
            self.players=[self._player]
        else:
            self.players[0]=self._player

    @property
    def worldWidth(self):
        """
        Returns the world width as an integer
        """
        return int(self.worldSize.x)
    
    @property
    def worldHeight(self):
        """
        Returns the world height as an integer
        """
        return int(self.worldSize.y)        

    def isInside(self,position):
        """
        Returns true is position is inside the world
        """
        return position.x >= 0 and position.x < self.worldWidth \
           and position.y >= 0 and position.y < self.worldHeight

    def findUnit(self,position):
        """
        Returns the index of the first unit at position, otherwise None.
        """
        for unit in self.units:
            if  int(unit.position.x) == int(position.x) \
            and int(unit.position.y) == int(position.y):
                return unit
        return None
    
    #def findLiveUnit(self,position):
    #    """
    #    Returns the index of the first live unit at position, otherwise None.
    #    """
    #    unit = self.findUnit(position)
    #    if unit is None or unit.status != STAT_ALIVE:
    #        return None
    #    return unit
    
    def addObserver(self,observer):
        """
        Add a game state observer. 
        All observer is notified when something happens (see GameStateObserver class)
        """
        self.observers.append(observer)
        
    def notifyUnitDestroyed(self,unit):
        for observer in self.observers:
            observer.unitDestroyed(unit)

    def notifyBulletFired(self,unit):
        for observer in self.observers:
            observer.bulletFired(unit)

    def notifyWarpTriggered(self,warp):
        for observer in self.observers:
            observer.warpTriggered(warp)

    def notifySceneTriggered(self,triggersource,scene):
        if(type(scene['params'])==str):     #todo nah not params !
            #callthis = Support.get_class('Tutorial.'+scene['params'],scene['params'],scene['params'])
            #callthis = Support.factory('Tutorial.'+scene['params']+'.'+scene['params'])
            callthis = Support.factory(scene['params'])
            scene = callthis
        for observer in self.observers:
            observer.sceneTriggered(scene)

    def notifyBattleTriggered(self,triggersource,scene):
        if(type(scene['params'])==str):     #todo nah not params !
            #callthis = Support.factory(scene['params'])
            #scene = callthis
            pass
        for observer in self.observers:
            observer.battleTriggered(scene)

