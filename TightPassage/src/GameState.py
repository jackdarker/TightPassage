import pygame
from src.Vector import Vector2

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
        self.player = None
        self.fileName = ""
        self.playerSpawn = None
        #maze vars
        self.mazeGenerator = None
        self.mazeNodes = []
        self.currentMazeNode = None
        #battlevars
        self.battleData = None

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
