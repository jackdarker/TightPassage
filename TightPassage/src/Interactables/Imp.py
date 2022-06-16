
import pygame
import src.Const as Const
import src.Support as Support
from src.Vector import Vector2
from src.Interactables.Unit import Unit
from src.Components.ComponentGraphics import UnitGraphics,AnimData
from src.Components.ComponentGraphics import AnimData
from src.AI.BehaviourSteering import BehaviourSteerNone,BehaviourSteerBounce

class Imp(Unit):
    def factory():
        return(Imp((0,0,50,50)))

    def __init__(self, rect,  direction=Vector2(1,0)):
        """

        """
        _rect = pygame.Rect((rect[0],rect[1]), (52,52)) #imagesize !
        SPRITEIMAGE = pygame.image.load(Const.resource_path("assets/sprites/goblin.png")).convert_alpha()

        super().__init__( _rect, 3, direction)
        self.behaviorSteering = BehaviourSteerBounce(self)
        hit_size = int(0.4*self.rect.width), int(0.6*self.rect.height)
        self.hitrect = pygame.Rect((0,0), hit_size)
        self.hitrect.center = self.rect.center
        #build animations
        anim = AnimData()
        name="idleright"
        anim.fps=2
        indices = [[0,2],[1,2]]
        anim.frames = Support.get_images(SPRITEIMAGE, indices, self.rect.size)
        self.cGraphic.addAnimation(name,anim)
        anim = AnimData()
        name="idleleft"
        anim.frames = [pygame.transform.flip(frame, True, False) 
                       for frame in Support.get_images(SPRITEIMAGE, indices, self.rect.size)]
        self.cGraphic.addAnimation(name,anim)
        anim = AnimData()
        name="idleup"
        indices = [[0,5],[1,5]]
        anim.frames = Support.get_images(SPRITEIMAGE, indices, self.rect.size)
        self.cGraphic.addAnimation(name,anim)
        anim = AnimData()
        name="idledown"
        indices = [[0,8],[1,8]]
        anim.frames = Support.get_images(SPRITEIMAGE, indices, self.rect.size)
        self.cGraphic.addAnimation(name,anim)
        #
        anim = AnimData()
        name="walkright"
        indices = [[0,1],[1,1],[2,1]]
        anim.frames = Support.get_images(SPRITEIMAGE, indices, self.rect.size)
        self.cGraphic.addAnimation(name,anim)
        anim = AnimData()
        name="walkleft"
        anim.frames = [pygame.transform.flip(frame, True, False) 
                       for frame in Support.get_images(SPRITEIMAGE, indices, self.rect.size)]
        self.cGraphic.addAnimation(name,anim)
        anim = AnimData()
        name="walkup"
        indices = [[0,4],[1,4],[2,4],[3,4]]
        anim.frames = Support.get_images(SPRITEIMAGE, indices, self.rect.size)
        self.cGraphic.addAnimation(name,anim)
        anim = AnimData()
        name="walkdown"
        indices = [[0,7],[1,7],[2,7],[3,7]]
        anim.frames = Support.get_images(SPRITEIMAGE, indices, self.rect.size)
        self.cGraphic.addAnimation(name,anim)
        #
        anim = AnimData()
        name="attackright"
        indices = [[0,0],[1,0],[2,0],[3,0]]
        anim.frames = Support.get_images(SPRITEIMAGE, indices, self.rect.size)
        self.cGraphic.addAnimation(name,anim)
        anim = AnimData()
        name="attackleft"
        anim.frames = [pygame.transform.flip(frame, True, False) 
                       for frame in Support.get_images(SPRITEIMAGE, indices, self.rect.size)]
        self.cGraphic.addAnimation(name,anim)
        anim = AnimData()
        name="attackup"
        indices = [[0,3],[1,3],[1,3],[1,3]]
        anim.frames = Support.get_images(SPRITEIMAGE, indices, self.rect.size)
        self.cGraphic.addAnimation(name,anim)
        anim = AnimData()
        name="attackdown"
        indices = [[0,6],[1,6],[1,6],[1,6]]
        anim.frames = Support.get_images(SPRITEIMAGE, indices, self.rect.size)
        self.cGraphic.addAnimation(name,anim)
        #
        SPRITEIMAGE = pygame.image.load(Const.resource_path("assets/sprites/death.png")).convert_alpha()
        anim = AnimData()
        name="die"
        anim.fps=4
        indices = [[0,0],[1,0],[2,0],[3,0],[4,0]]
        anim.frames = Support.get_images(SPRITEIMAGE, indices, (48,48))
        self.cGraphic.addAnimation(name,anim)
        SPRITEIMAGE = None

        self.add_direction(pygame.K_DOWN)

class Snake(Unit):
    def factory():
        return(Snake((0,0,50,50)))

    def __init__(self, rect,  direction=Vector2(1,0)):
        """

        """
        _rect = pygame.Rect((rect[0],rect[1]), (32,32))
        SPRITEIMAGE = pygame.image.load(Const.resource_path("assets/sprites/Cobra Sprite Sheet.png")).convert_alpha()

        super().__init__( _rect, 1, direction)
        self.behaviorSteering = BehaviourSteerNone(self)
        hit_size = int(0.4*self.rect.width), int(0.6*self.rect.height)
        self.hitrect = pygame.Rect((0,0), hit_size)
        self.hitrect.center = self.rect.center
        #build animations
        anim = AnimData()
        name="idleright"
        anim.fps=2
        indices = [[0,0],[1,0],[2,0],[3,0],[4,0],[5,0],[6,0],[7,0]]
        anim.frames = Support.get_images(SPRITEIMAGE, indices, self.rect.size)
        self.cGraphic.addAnimation(name,anim)
        anim = AnimData()
        name="idleleft"
        anim.frames = [pygame.transform.flip(frame, True, False) 
                       for frame in Support.get_images(SPRITEIMAGE, indices, self.rect.size)]
        self.cGraphic.addAnimation(name,anim)
        anim = AnimData()
        name="idleup"
        anim.frames = [pygame.transform.flip(frame, True, False) 
                       for frame in Support.get_images(SPRITEIMAGE, indices, self.rect.size)]
        self.cGraphic.addAnimation(name,anim)
        anim = AnimData()
        name="idledown"
        anim.frames = [pygame.transform.flip(frame, True, False) 
                       for frame in Support.get_images(SPRITEIMAGE, indices, self.rect.size)]
        self.cGraphic.addAnimation(name,anim)
        #
        anim = AnimData()
        name="walkright"
        indices = [[0,1],[1,1],[2,1],[3,1],[4,1],[5,1],[6,1],[7,1]]
        anim.frames = Support.get_images(SPRITEIMAGE, indices, self.rect.size)
        self.cGraphic.addAnimation(name,anim)
        anim = AnimData()
        name="walkleft"
        anim.frames = [pygame.transform.flip(frame, True, False) 
                       for frame in Support.get_images(SPRITEIMAGE, indices, self.rect.size)]
        self.cGraphic.addAnimation(name,anim)
        anim = AnimData()
        name="walkup"
        anim.frames = [pygame.transform.flip(frame, True, False) 
                       for frame in Support.get_images(SPRITEIMAGE, indices, self.rect.size)]
        self.cGraphic.addAnimation(name,anim)
        anim = AnimData()
        name="walkdown"
        anim.frames = [pygame.transform.flip(frame, True, False) 
                       for frame in Support.get_images(SPRITEIMAGE, indices, self.rect.size)]
        self.cGraphic.addAnimation(name,anim)
        #
        anim = AnimData()
        name="attackright"
        indices = [[0,2],[1,2],[2,2]]
        anim.frames = Support.get_images(SPRITEIMAGE, indices, self.rect.size)
        self.cGraphic.addAnimation(name,anim)
        anim = AnimData()
        name="attackleft"
        anim.frames = [pygame.transform.flip(frame, True, False) 
                       for frame in Support.get_images(SPRITEIMAGE, indices, self.rect.size)]
        self.cGraphic.addAnimation(name,anim)
        anim = AnimData()
        name="attackup"
        anim.frames = [pygame.transform.flip(frame, True, False) 
                       for frame in Support.get_images(SPRITEIMAGE, indices, self.rect.size)]
        self.cGraphic.addAnimation(name,anim)
        anim = AnimData()
        name="attackdown"
        anim.frames = [pygame.transform.flip(frame, True, False) 
                       for frame in Support.get_images(SPRITEIMAGE, indices, self.rect.size)]
        self.cGraphic.addAnimation(name,anim)
        #
        anim = AnimData()
        name="die"
        anim.fps=4
        indices = [[0,4],[1,4],[2,4],[3,4],[4,4],[5,4]]
        anim.frames = Support.get_images(SPRITEIMAGE, indices, self.rect.size)
        self.cGraphic.addAnimation(name,anim)
        SPRITEIMAGE = None
