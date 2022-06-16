import pygame
from src.Vector import Vector2
import src.Const as Const
import src.Interactables.Interactable
from src.Interactables.Interactable import Interactable

class AnimData():
    """struct to store info for animation"""
    def __init__(self):
        #self.name = ""  #name of the animationstrip
        self.frames =[] #image frames
        self.repeatFrom =0 #frameindex from that the animation will repeat
        self.repeatCycles =-1 #how many repetitions 0=none ;-1 = unlimited
        self.fps = 7

class ComponentGraphics(pygame.sprite.Sprite):
    """helper class to render animations and switch between different animationsets"""
    def __init__(self, parent, on_done = None):
        pygame.sprite.Sprite.__init__(self)
        self.parent = parent    #interatable this Component is assigned to
        self.frame_dict = {}    #{walk : frames[], idle : frames[]}
        self.redraw = False
        self.anim_frameNo = -2 #no frames
        self.anim_cycles = 0
        self.anim_frames = []
        self.anim_name = ""
        self.anim_fps = 7.0
        self.anim_timer = 0
        #image and rect is needed for use of pygame.sprite.group
        self.image = pygame.Surface((2,2))
        self.image.fill(Const.YELLOW)
        self.rect = self.image.get_rect()
        self.done = False
        self.on_done = on_done  #callback triggered when non continous animation finishs

    def addAnimation(self,name, animData):
        self.frame_dict[name] = animData

    def draw(self, surface):
        """draws the actual animation frame to surface
        if you add this component to sprite.group, this will not be called, just update
        """
        if(self.image!=None and self.done == False):
            #surface.fill((128, 0, 128,0))  dont overwrite existing surface
            surface.blit(self.image,self.rect.topleft)#, self.parent.rect)

    def update(self):
        now = pygame.time.get_ticks()
        finished = False
        if (self.done==False and self.anim_frameNo>=-1 and (self.redraw or now-self.anim_timer > 1000/self.anim_fps)):
            
            cycledone = (self.anim_frameNo) == len(self.anim_data.frames)-1
            if(cycledone==True):
                self.anim_cycles+=1
            #finished if no repeat or number repeated and all frames done
            finished = (self.anim_data.repeatCycles !=-1 and self.anim_data.repeatCycles <= self.anim_cycles) and cycledone
            #select frame to display
            if(self.anim_frameNo==-1 or finished==False):
                if(self.anim_data.repeatFrom>=0 and ((self.anim_frameNo+1)//len(self.anim_data.frames))>0):
                    self.anim_frameNo = self.anim_data.repeatFrom #repeat from specified frame after first cycle finished
                else:
                    self.anim_frameNo = (self.anim_frameNo+1)%len(self.anim_data.frames)
                self.image = self.anim_data.frames[self.anim_frameNo]
            self.anim_timer = now
        if not self.image:
            #todo error if invalid image
            pass
        self.redraw = False
        if(finished):
            self.done =True
            if(self.on_done != None): self.on_done(self.anim_name)


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
                self.anim_frameNo = -2
                return #todo what if anim missing?
            if(len(self.anim_data.frames)<=0):  
                self.anim_frameNo = -2  # flag that there are no frames
            else : 
                self.anim_frameNo = -1   # -1 marks that the animation didnt run yet
            self.anim_fps = self.anim_data.fps
            self.anim_cycles = 0
            self.redraw = True
            self.done = False
        pass

    def set_rects(self, value, attribute="topleft"):
        """
        """
        setattr(self.rect, attribute, value)


class UnitGraphics(ComponentGraphics):
    """translates unitstate-to-animation"""
    def __init__(self, parent):
        super().__init__(parent)

    def update(self):
        now = pygame.time.get_ticks()
        facing = Interactable.Direct_Dict_Inverse(self.parent.direction)
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

