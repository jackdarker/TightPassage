class GameModeObserver():
    """Observers can recieve notifications from GameModes"""
    def loadLevelRequested(self, fileName):
        pass
    def worldSizeChanged(self, worldSize):
        pass
    def showMenuRequested(self):
        pass
    def showPopupRequested(self):
        pass
    def showGameRequested(self,Message):
        pass
    def gameWon(self):
        pass
    def gameLost(self):
        pass
    def quitRequested(self):
        pass