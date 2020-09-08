import pygame
import src.Interactables.Interactable
from src.Interactables.Interactable import Interactable

class AnimData():
    """struct to store info for animation"""
    def __init__(self):
        #self.name = ""  #name of the animationstrip
        self.frames =[] #image frames
        self.repeatFrom =0 #frameindex from that the animation will repeat; -1 for not repeat
        self.fps = 7

class ComponentGraphics(pygame.sprite.Sprite):
    """helper class to render animations and switch between different animationsets"""
    def __init__(self, parent):
        self.parent = parent    #interatable this Component is assigned to
        self.frame_dict = {}    #{walk : frames[], idle : frames[]}
        self.redraw = False
        self.anim_frameNo = -2 #no frames
        self.anim_frames = []
        self.anim_name = ""
        self.anim_fps = 7.0
        self.anim_timer = 0
        self.image = None

    def addAnimation(self,name, animData):
        self.frame_dict[name] = animData

    def draw(self, surface):
        """Draw method seperated out from update."""
        if(self.image!=None):
            surface.fill((128, 0, 128,0))
            surface.blit(self.image,(0,0))#, self.parent.rect)

    def update(self):
        now = pygame.time.get_ticks()
        if self.redraw or now-self.anim_timer > 1000/self.anim_fps:
            if(self.anim_frameNo>=-1):  #todo and self.anim_data.repeat>-1
                self.anim_frameNo = (self.anim_frameNo+1)%len(self.anim_data.frames)
                self.image = self.anim_data.frames[self.anim_frameNo]
            self.anim_timer = now
        if not self.image:
            #todo self.image = self.walkframes[self.frame]
            pass
        self.redraw = False

    def switchTo(self,name,direction=""):
        """activates the animation if not already running
        If an animation with name+direction is found, this is used; otherwise the animation with name.
        So you can use "walk"+"_left" or just "walk"
        """
        name2 = name+direction
        if(self.anim_name == name or self.anim_name == name2):
            pass
        else:
            self.anim_data = self.frame_dict.get(name2)
            self.anim_name = name2
            if(self.anim_data==None): 
                self.anim_data = self.frame_dict.get(name)
                self.anim_name = name
            if(self.anim_data==None):
                return #todo what if anim missing?
            if(len(self.anim_data.frames)<=0):  self.anim_frameNo = -2  # flag that there are no frames
            else : self.anim_frameNo = -1   
            self.anim_fps = self.anim_data.fps  #todo
            self.redraw = True
        pass

class UnitGraphics(ComponentGraphics):
    """translates unitstate-to-animation"""
    def __init__(self, parent):
        super().__init__(parent)

    def update(self):
        now = pygame.time.get_ticks()
        facing = pygame.key.name(self.parent.direction)
        if(self.parent.status==Interactable.STAT_DIEING):
            self.switchTo("die",facing)
        elif self.parent.direction_stack:
            self.switchTo("walk",facing)
        elif (self.parent.attacking==True):
            self.switchTo("attack",facing)   #todo attack should not loop
        elif (True):
            self.switchTo("idle",facing)
        if self.redraw or now-self.anim_timer > 1000/self.anim_fps:
            if(self.anim_frameNo>=-1):  #todo and self.anim_data.repeat>-1
                self.anim_frameNo = (self.anim_frameNo+1)%len(self.anim_data.frames)
                self.image = self.anim_data.frames[self.anim_frameNo]
            self.anim_timer = now
        if not self.image:
            #todo self.image = self.walkframes[self.frame]
            pass
        self.redraw = False

