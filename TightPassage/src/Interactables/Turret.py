import pygame
import src.Const as Const
import src.Support as Support
from src.Vector import Vector2
from src.Interactables.Interactable import Interactable
from src.Interactables.Unit import Unit
from src.Interactables.Damager import Damager,DamagerInfo
from src.Interactables.Fireball import Fireball
from src.Components.ComponentGraphics import UnitGraphics,AnimData
from src.GameState import GameState
from src.AI.BehaviourSteering import BehaviourSteerNone
from src.AI.SensorNoise import SensorNone,SensorLineOfSight

class Spikes(Unit):
    def factory():
        return(Spikes((0,0,0,0)))

    def __init__(self, rect,  direction=Vector2(0,0)):
        """something that hurts the player if he runs into it

        """
        _s=32
        _w=rect.width//_s
        _h=rect.height//_s
        _rect = pygame.Rect((rect[0],rect[1]), (_w*_s,_h*_s))
        SPRITEIMAGE = pygame.image.load(Const.resource_path("assets/sprites/Dungeon_Tileset.png")).convert_alpha()
        super().__init__( _rect, 0, direction)
        self.sensorPlayer = SensorNone(self)
        self.behaviorSteering = BehaviourSteerNone(self)
        hit_size = int(self.rect.width-4), int(self.rect.height-4) #todo better player hitbox
        self.hitrect = pygame.Rect((0,0), hit_size)
        self.hitrect.center = self.rect.center
        #build animations
        anim = AnimData()
        anim.fps=2
        indices = [[3,15],[4,15],[5,15]]
        anim.frames = Support.get_images(SPRITEIMAGE, indices,(_s,_s)) #self.rect.size)
        anim.frames= Support.extend_frames(anim.frames,_w,_h)
        self.cGraphic.addAnimation("idle",anim)
        self.cGraphic.addAnimation("walk",anim)
        self.cGraphic.addAnimation("attack",anim)
        self.cGraphic.addAnimation("die",anim)
        self.CB_onEnter = self.attack
        self.CB_onExit = None
        self.enterTriggered= self.exitWait = False

    def update(self,dt):
        state=GameState()
        if(not state.inGame):
            return
        self.triggerSource = state.player   # todo at construction of trigger player doesnt yet exist and triggersource is invalid
        if(self.coolDown_Attack>0): 
            self.coolDown_Attack-=1
            return
        _inside=False#_inside = pygame.sprite.collide_rect(self,self.triggerSource)
        callback = self.collide_other(self.hitrect)
        collisions = pygame.sprite.spritecollide(self, self.levelData.players, False, callback)
        while collisions:
            collision = collisions.pop()
            _inside=True #self.notifyOnHit(collision)

        if(_inside and not self.enterTriggered):
            if(self.CB_onEnter!= None): self.CB_onEnter()
            self.enterTriggered  = True
            return
        if(not _inside and self.enterTriggered): 
            if(self.CB_onExit!= None):self.CB_onExit()
            self.enterTriggered=False
            return

    def attack(self):
        if(self.coolDown_Attack<=0):
            self.coolDown_Attack = Const.FPS
            self.attacking = True
            self.triggerAttack(Damager(self,DamagerInfo(self.direction, Const.FPS//2,1,self.hitrect.size,(0,0))))



class Turret(Unit):
    def factory():
        return(Turret((0,0,0,0)))

    def __init__(self, rect,  direction=Vector2(1,0)):
        """something that shoots at player if in range

        """
        _rect = pygame.Rect((rect[0],rect[1]), (80,96))
        SPRITEIMAGE = pygame.image.load(Const.resource_path("assets/sprites/eye.png")).convert_alpha()

        super().__init__( _rect, 0, direction)
        self.sensorPlayer = SensorLineOfSight(self,160)
        self.behaviorSteering = BehaviourSteerNone(self)
        hit_size = int(0.4*self.rect.width), int(0.6*self.rect.height)
        self.hitrect = pygame.Rect((0,0), hit_size)
        self.hitrect.center = self.rect.center
        #build animations
        anim = AnimData()
        name="idleright"
        anim.fps=2
        indices = [[0,1],[1,1],[2,1],[3,1]]
        anim.frames = Support.get_images(SPRITEIMAGE, indices, self.rect.size)
        self.cGraphic.addAnimation(name,anim)
        ####
        anim = AnimData()
        name="walkright"
        anim.fps=2
        anim.frames = Support.get_images(SPRITEIMAGE, indices, self.rect.size)
        self.cGraphic.addAnimation(name,anim)
        ####
        anim = AnimData()
        name="attackright"
        anim.fps=4
        anim.frames = Support.get_images(SPRITEIMAGE, indices, self.rect.size)
        self.cGraphic.addAnimation(name,anim)
        ####
        anim = AnimData()
        name="idleleft"
        anim.frames = [pygame.transform.flip(frame, True, False) 
                       for frame in Support.get_images(SPRITEIMAGE, indices, self.rect.size)]
        self.cGraphic.addAnimation(name,anim)
        ###
        anim = AnimData()
        name="walkkleft"
        anim.fps=2
        anim.frames = Support.get_images(SPRITEIMAGE, indices, self.rect.size)
        self.cGraphic.addAnimation(name,anim)
        ####
        anim = AnimData()
        name="attackleft"
        anim.fps=4
        anim.frames = Support.get_images(SPRITEIMAGE, indices, self.rect.size)
        self.cGraphic.addAnimation(name,anim)
        anim = AnimData()
        name="idleup"
        anim.fps=2
        indices = [[0,4],[1,4],[2,4],[3,4]]
        anim.frames = Support.get_images(SPRITEIMAGE, indices, self.rect.size)
        self.cGraphic.addAnimation(name,anim)
        ####
        anim = AnimData()
        name="walkup"
        anim.fps=2
        anim.frames = Support.get_images(SPRITEIMAGE, indices, self.rect.size)
        self.cGraphic.addAnimation(name,anim)
        ####
        anim = AnimData()
        name="attackup"
        anim.fps=4
        anim.frames = Support.get_images(SPRITEIMAGE, indices, self.rect.size)
        self.cGraphic.addAnimation(name,anim)
        anim = AnimData()
        ####
        name="idledown"
        anim.fps=2
        indices = [[0,7],[1,7],[2,7],[3,7]]
        anim.frames = Support.get_images(SPRITEIMAGE, indices, self.rect.size)
        self.cGraphic.addAnimation(name,anim)
        ####
        anim = AnimData()
        name="walkdown"
        anim.fps=2
        anim.frames = Support.get_images(SPRITEIMAGE, indices, self.rect.size)
        self.cGraphic.addAnimation(name,anim)
        ####
        anim = AnimData()
        name="attackdown"
        anim.fps=4
        anim.frames = Support.get_images(SPRITEIMAGE, indices, self.rect.size)
        self.cGraphic.addAnimation(name,anim)
        SPRITEIMAGE = pygame.image.load(Const.resource_path("assets/sprites/death.png")).convert_alpha()
        anim = AnimData()
        name="die"
        anim.fps=4
        indices = [[0,0],[1,0],[2,0],[3,0],[4,0]]
        anim.frames = Support.get_images(SPRITEIMAGE, indices, (48,48))
        self.cGraphic.addAnimation(name,anim)
        SPRITEIMAGE = None

    def attack(self):
        """attack in view direction"""
        if(self.coolDown_Attack<=0):
            self.coolDown_Attack = Const.FPS
            self.timer_Atk = Const.FPS // 2 #todo depends on attack
            self.attacking = True
            self.triggerAttack(Fireball(self, 10, self.direction))

    def updateBrain(self):
        self.throttleAI-=1
        if(self.throttleAI<=0):
            self.throttleAI = Const.FPS #todo
            if(self.sensorPlayer.detectTarget(GameState().player,GameState().obstacles)):
                if(self.ai==Interactable.AI_IDLE or self.ai==Interactable.AI_SEARCH):
                    self.ai=Interactable.AI_ATTACK
            else:
                if(self.ai==Interactable.AI_ATTACK):
                    self.ai=Interactable.AI_SEARCH

            if(self.ai==Interactable.AI_ATTACK):
                self.direction_stack.clear()
                _dir=GameState().player.position-self.position
                if(abs(_dir.x)>abs(_dir.y)):
                    if(_dir.x>0):
                        self.direction=Vector2(1, 0)
                    else:
                        self.direction=Vector2(-1, 0)
                else:
                    if(_dir.y>0):
                        self.direction=Vector2(0, 1)
                    else:
                        self.direction=Vector2(0, -1)
                self.attack()
                