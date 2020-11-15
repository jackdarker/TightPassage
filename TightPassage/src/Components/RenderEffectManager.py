import random
import pygame
import src.Support as Support
import src.Components.ResourceManager as RM
from src.Components.Skill import Skill,SkillCombat,Effect,SkillResult
import src.Components.SkillDB as SkillDB
import src.Const as Const
from src.Vector import Vector2
from src.Components.ComponentGraphics import *

class SkillEffectToRenderEffectConverter():

    def __init__(self):
        pass

    def convertSkillEffectToRenderEffect(self,skilleffect,avatars):
        """to separate GameLogic from Rendering, the StatEffects are translated to displayeffect here
        todo is there abetter way ?
        """
        pos = avatars[skilleffect.owner.name].rect.center
        if(type(skilleffect)==SkillDB.EffDamage):
            return(RE_Hit(pos))
        elif(type(skilleffect)==SkillDB.EffMiss):
            return(RE_Miss(pos))
        else:
            return(None)
        pass


class RenderEffectManager():

    def __init__(self,on_finished = None):
        self.effects = []
        self.running = []
        self._on_finished = on_finished

    def update(self,dt):
        finishedEff = []
        running = False
        for eff in self.running:
            running = True
            eff.update(dt)
            if(eff.finished==True):
                finishedEff.append(eff)

        if(not running):
            for eff in self.effects:
                self.running.append(eff)
                self.effects.remove(eff)
                eff.on_start()
                break
        
        for eff in finishedEff:
            eff.on_finished()
            self.running.remove(eff)
        pass

        if(len(self.running)==0 and len(finishedEff)>0):
            self._on_finished()

    def draw(self,surface):
        for eff in self.running:        #todo sprite.group is faster?
            eff.draw(surface)
        pass

    def addEffect(self, effect,defer=False):
        """ adds an effect to the manager and starts it
        if defer = True, the start will be delayed until all running effects are finished
        """
        self.effects.append(effect)
        


class RenderEffectBase():
    """ Baseclass for rendering effects 
    contains the information of graphic/animation/sound 
    """
    STATE_IDLE = 0
    STATE_RUN = 1
    STATE_FINISHED = -1
    def __init__(self):
        self.finished = False
        self.state = RenderEffectBase.STATE_IDLE  #state enum 
        pass
    def on_start(self):
        """implement to initialise rendering the effect
        """
        pass

    def on_finished(self):
        """gets called when effect done
        """
        pass

    def update(self,dt):
        """ implement to update your render, f.e. animation frame
        """
        pass

    def draw(self,surface):
        pass

class RenderEffect(RenderEffectBase):
    """ contains the information to display an effect
    - show an animation sprite
    - play a sound
    - move an object around
    """
    NAME="default"

    def __init__(self):
        super(RenderEffect,self).__init__()
        self.cGraphic = ComponentGraphics(self, on_done=self._on_done)
        self.sound= None
        self.sound_delay = 0
        self.sound_timer = 0
        

        SPRITEIMAGE = pygame.image.load(Const.resource_path("assets/sprites/Particles/Attack11.png")).convert_alpha()
        anim = AnimData()
        anim.fps=5
        anim.repeatCycles=0
        indices = [[0,0],[1,0],[0,0]]
        anim.frames = Support.get_images(SPRITEIMAGE, indices, (200,200))
        self.set_animation(anim,(0,0))

    def set_animation(self,anim,pos):
        """ set an animation to be played, f.e particle effect
        """
        self.cGraphic.addAnimation(RenderEffect.NAME,anim)
        self.cGraphic.set_rects(pos,attribute="center")

    def set_sound(self,sound,delay=0):
        """ set a pygame.mixer.sound to be played
        delay can be used to synchronize the sound with animation
        """
        self.sound = sound
        self.sound_delay = delay

    def _on_done(self,name):
        self.state = RenderEffectBase.STATE_FINISHED
        self.finished = True

    def on_start(self):
        self.state = RenderEffectBase.STATE_RUN
        self.cGraphic.switchTo(RenderEffect.NAME)
        self.sound_timer = 0
        pass

    def on_finished(self):
        """gets called when effect done
        """

        pass

    def update(self,dt):
        """ implement to update your render, f.e. animation frame
        """
        if(self.state==RenderEffectBase.STATE_RUN):
            
            if(self.sound_timer >=0):
                self.sound_timer += dt

            self.cGraphic.update()
            if(self.sound != None and self.sound_timer>= self.sound_delay):
                pygame.mixer.Channel(Interactable.SfxCh_Hit).play(self.sound)
                self.sound_timer = -1 #-1 = disable replay sound
        else:
            self.starttime = 0
        pass

    def draw(self,surface):
        if(self.state==RenderEffectBase.STATE_RUN):
            self.cGraphic.draw(surface)   #self.cGraphic.draw(surface)
        pass

class RE_Hit(RenderEffect):
    def __init__(self,pos):
        super(RE_Hit,self).__init__()
        HITSOUND = RM.get_sound("hit3.wav")
        HITSOUND.set_volume(1.0)
        SPRITEIMAGE = RM.get_image("sprites/Particles/Attack11.png").convert_alpha()
        anim = AnimData()
        anim.fps=5
        anim.repeatFrom = 2
        anim.repeatCycles = 10
        indices = [[0,0],[1,0],[0,0]]
        anim.frames = Support.get_images(SPRITEIMAGE, indices, (200,200))
        self.set_animation(anim,pos)
        self.set_sound(HITSOUND,500)

class RE_Miss(RenderEffect):
    def __init__(self,pos):
        super(RE_Miss,self).__init__()
        SPRITEIMAGE = RM.get_image("sprites/Particles/ComicEffect.png").convert_alpha()
        anim = AnimData()
        anim.fps=1
        anim.repeatCycles=2
        indices = [[1,0]]
        anim.frames = Support.get_images(SPRITEIMAGE, indices, (200,200))
        self.set_animation(anim,pos)

