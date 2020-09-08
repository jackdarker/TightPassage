import pygame
import src.Const as Const
import src.GameMode as GameMode
import src.Support as Support
import src.Tools as Tools
from src.Tools import TileMapCreator
import src.Components.ComponentGraphics
from src.Components.ComponentGraphics import ComponentGraphics
from src.Components.ComponentGraphics import AnimData

class SceneData():
    """contains data for a dialogscene
    """
    def __init__(self):
        pass

    def loadImageStrip(self,basedir,fps):
        creator = TileMapCreator()
        self.name,texture,data = creator.SpritesToTilemap(basedir)
        self.anim = AnimData()
        self.anim.fps=fps
        self.anim.frames = Support.get_allImages(texture, data[0].get('size'))  #Todo need to support different sizes?


class MovieMode(GameMode.GameMode):
    def __init__(self,scene):     
        super().__init__(scene)
        self.rect = pygame.Rect((0,0),Const.WINDOW_SIZE)
        self.cGraphic = ComponentGraphics(self)
        self.cGraphic.addAnimation(scene.name,scene.anim)
        self.cGraphic.switchTo(scene.name)
        self.enabled=False

    def processInput(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.notifyQuitRequested()
                break
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE \
                or event.key == pygame.K_SPACE \
                or event.key == pygame.K_RETURN:
                    self.notifyShowMenuRequested()
                    self.enabled = False
                    
    def update(self):
        self.cGraphic.update()  #Todo center graphic on Window

    def render(self, window):
        self.cGraphic.draw(window)

    def show(self):
        self.enabled = True

