import pygame
import src.Const as Const
import src.Components.ResourceManager as RM
import src.GameMode as GameMode
import src.Support as Support
import src.Tools as Tools
from src.Tools import TileMapCreator
import src.Components.ComponentGraphics
from src.Components.ComponentGraphics import ComponentGraphics,AnimData

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

        self.image = pygame.Surface(Const.WINDOW_SIZE)

        self.bg=pygame.sprite.DirtySprite()
        self.bg.image = RM.get_image('cgs\\Nature Background.png')
        self.bg.rect = self.bg.image.get_rect()
        self.bg.rect.size = (400,400)#Const.WINDOW_SIZE
        self.bg.dirty=1
        self.image.blit(self.bg.image,(0,0))

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
                    
    def update(self,dt):
        self.cGraphic.update()  #Todo center graphic on Window

    def render(self, window):
        window.blit(self.bg.image,(0,0))
        self.cGraphic.draw(window)

    def show(self):
        self.enabled = True

