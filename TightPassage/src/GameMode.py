class GameMode():
    """your Menu-, Battle-, Whatever-GameMode should derive from this class to send notifications"""
    def __init__(self,state):
        self.__observers = []
        self.state = state
    def addObserver(self, observer):
        self.__observers.append(observer)

    def removeObserver(self, observer):
        if(self.__observers.count(observer)):
            self.__observers.remove(observer)
    def notifyNewBattleRequested(self,Battle):
        for observer in self.__observers:
            observer.newBattleRequested(Battle)
    def notifyNewGameRequested(self,MazeGenerator="MazeGenerator"):
        for observer in self.__observers:
            observer.newGameRequested(MazeGenerator)
    def notifyLoadLevelRequested(self, fileName):
        for observer in self.__observers:
            observer.loadLevelRequested(fileName)
    def notifyWorldSizeChanged(self, worldSize):
        for observer in self.__observers:
            observer.worldSizeChanged(worldSize)
    def notifyShowMenuRequested(self):
        for observer in self.__observers:
            observer.showMenuRequested()
    def notifyShowPopupRequested(self,Message):
        for observer in self.__observers:
            observer.showPopupRequested(Message)
    def notifyShowGameRequested(self):
        for observer in self.__observers:
            observer.showGameRequested()
    def notifyGameWon(self):
        for observer in self.__observers:
            observer.gameWon()
    def notifyGameLost(self):
        for observer in self.__observers:
            observer.gameLost()
    def notifyQuitRequested(self):
        for observer in self.__observers:
            observer.quitRequested()
        
    def processInput(self):
        raise NotImplementedError()
    def update(self,dt):
        raise NotImplementedError()
    def render(self, window):
        raise NotImplementedError()
