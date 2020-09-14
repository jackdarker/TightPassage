import os
import pygame
import src.Const as Const
import src.Support as Support
import src.Interactables.Interactable
from src.Interactables.Interactable import Interactable
import src.Components.ComponentGraphics
from src.Components.ComponentGraphics import UnitGraphics
from src.GameState import GameState

class Unit(Interactable):

    #resourcefiles for this unit
    SPRITEIMAGE = None
    ATTACKIMAGE = None
    HITSOUND = None
    MOVESOUND = None
    DEATHSOUND = None

    def __init__(self, rect, speed, direction=pygame.K_RIGHT):
        """
        Arguments are a rect representing the Player's location and
        dimension, the speed(in pixels/frame) of the Player, and the Player's
        starting direction (given as a key-constant).
        """
        super().__init__(rect,direction)
        self.image = pygame.Surface((rect.width,rect.height),pygame.SRCALPHA)
        hit_size = int(0.6*self.rect.width), int(0.4*self.rect.height)
        self.hitrect = pygame.Rect((0,0), hit_size)
        self.hitrect.center = self.rect.center
        self.speed = speed
        self.health = 3
        #loading resources
        if(type(self).SPRITEIMAGE == None):
            type(self).SPRITEIMAGE = pygame.image.load(Const.resource_path("assets/sprites/skelly.png")).convert()
            type(self).SPRITEIMAGE.set_colorkey(Const.COLOR_KEY)
        if(type(self).ATTACKIMAGE == None):
            type(self).ATTACKIMAGE = pygame.Surface((30,30)).convert_alpha()
            type(self).ATTACKIMAGE.fill((100,0,0))
        if(type(self).HITSOUND == None):
            type(self).HITSOUND = pygame.mixer.Sound(Const.resource_path("assets/sounds/hit3.wav"))
            type(self).HITSOUND.set_volume(1.0)
        if(type(self).MOVESOUND == None):
            type(self).MOVESOUND = pygame.mixer.Sound(Const.resource_path("assets/sounds/walk3.wav"))
            type(self).MOVESOUND.set_volume(1.0)
        if(type(self).DEATHSOUND == None):
            type(self).DEATHSOUND = pygame.mixer.Sound(Const.resource_path("assets/sounds/death.wav"))
            type(self).DEATHSOUND.set_volume(1.0)
        self.direction_stack = []  #Held keys in the order they were pressed.
        self.direction_offset = pygame.Vector2(0,0)
        self.coolDown_Attack = 0 #cooldown attack
        self.timer_Atk = 0
        self.attacking = False
        self.cGraphic = UnitGraphics(self)
        self.levelData = GameState() #reference to singleton
        self.canUseDoors =False

    def draw(self, surface):
        """draws the image"""
        self.cGraphic.update()
        self.cGraphic.draw(self.image)   #self.cGraphic.draw(surface)

    def add_direction(self, key):
        """Add a pressed direction key on the direction stack."""
        if key in Interactable.DIRECT_DICT:
            if key in self.direction_stack:
                self.direction_stack.remove(key)
            self.direction_stack.append(key)
            self.direction = self.direction_stack[-1]

    def pop_direction(self, key):
        """Pop a released key from the direction stack."""
        if key in Interactable.DIRECT_DICT:
            if key in self.direction_stack:
                self.direction_stack.remove(key)
            if self.direction_stack:
                self.direction = self.direction_stack[-1]

    def update(self):
        """Adjust the image and move as needed."""
        now = pygame.time.get_ticks()
        
        if(self.status == Interactable.STAT_DIEING):
            self.frame+=1
            if ( self.frame>= self.die_timer): 
                self.OnDeath()
            return
        elif(self.health<=0):
            if(self.status == Interactable.STAT_ALIVE): self.start_dieing()
            return
        else:
            if(self.coolDown_Attack>0): 
                self.coolDown_Attack-=1
            if(self.timer_Atk>0): 
                self.timer_Atk-=1
            else:
                self.attacking = False
            
            if self.direction_stack or self.direction_offset != pygame.Vector2(0,0):
                self.movement( 0)
                self.movement( 1)
            #if(self.canUseDoors):
            #    callback = self.collide_other(self.hitrect)  #Collidable callback created.
            #    collisions = pygame.sprite.spritecollide(self, self.levelData.doors, False, callback)
            #    while collisions:
            #        collision = collisions.pop()
            #        self.levelData.notifyWarpTriggered(collision)


    def start_dieing(self):
        """ triggers the die-sequence
            returns false if die already started before
        """
        if(self.status != Interactable.STAT_DIEING and self.status != Interactable.STAT_DEAD):
            self.status = Interactable.STAT_DIEING
            self.frame = 0
            self.redraw = True
            self.die_timer = 10#todolen(self.dieframes)
            pygame.mixer.Channel(Interactable.SfxCh_Hit).play(type(self).DEATHSOUND)
            return True
        return False

    def OnDeath(self):
        self.kill()

    def attack(self):
        """attack in view direction"""
        if(self.coolDown_Attack<=0):
            self.coolDown_Attack = Const.FPS
            self.timer_Atk = Const.FPS // 2 #todo depends on attack
            self.attacking = True
            #return Fireball.Fireball(self, 10, self.direction)
        else:
            return None

    def damage(self,amount,direction):
        """apply damage to the target"""
        self.health-=amount
        pygame.mixer.Channel(Interactable.SfxCh_Hit).play(type(self).HITSOUND)
        self.direction_offset = Interactable.DIRECT_DICT[direction]
        self.direction_offset = self.direction_offset.elementwise()*4*amount  #push in oposite direction on hit
        

    def movement(self,  i):
        """Move player and then check for collisions; adjust as necessary.
        i =0 is x; i=1 is y 
        """
        obstacles = self.levelData.obstacles
        if self.direction_stack:
            if(not pygame.mixer.Channel(Interactable.SfxCh_Move).get_busy()):
                pygame.mixer.Channel(Interactable.SfxCh_Move).play(type(self).MOVESOUND)
            direction_vector = Interactable.DIRECT_DICT[self.direction]
            self.hitrect[i] += self.speed*direction_vector[i]

        self.hitrect[i] += self.direction_offset[i]
        if self.direction_offset[i]>0: self.direction_offset[i] -= 1    #... to make it so that the offset is stretched about several frames
        callback = self.collide_other(self.hitrect)  #Collidable callback created.
        collisions = pygame.sprite.spritecollide(self, obstacles, False, callback)
        while collisions:
            collision = collisions.pop()
            self.adjust_on_collision(self.hitrect, collision, i)
        self.rect.center = self.hitrect.center

    def adjust_on_collision(self, rect_to_adjust, collide, i):
        """Adjust player's position if colliding with a solid block."""
        if rect_to_adjust[i] < collide.rect[i]:
            rect_to_adjust[i] = collide.rect[i]-rect_to_adjust.size[i]
        else:
            rect_to_adjust[i] = collide.rect[i]+collide.rect.size[i]