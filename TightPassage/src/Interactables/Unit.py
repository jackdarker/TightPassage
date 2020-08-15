import os
import pygame
import src.Const as Const
import src.Support as Support
import src.Interactables.Interactable
from src.Interactables.Interactable import Interactable

class Unit(Interactable):

    #resourcefiles for this unit
    SPRITEIMAGE = None
    ATTACKIMAGE = None
    HITSOUND = None
    MOVESOUND = None

    def __init__(self, rect, speed, direction=pygame.K_RIGHT):
        """
        Arguments are a rect representing the Player's location and
        dimension, the speed(in pixels/frame) of the Player, and the Player's
        starting direction (given as a key-constant).
        """
        super().__init__(rect,direction)
        
        hit_size = int(0.6*self.rect.width), int(0.4*self.rect.height)
        self.hitrect = pygame.Rect((0,0), hit_size)
        self.hitrect.midbottom = self.rect.midbottom
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
        self.direction_stack = []  #Held keys in the order they were pressed.
        self.direction_offset = pygame.Vector2(0,0)
        self.cd_Atk = 0 #cooldown attack
        self.attacking = False
        self.walkframes = []
        self.dieframes = []
        self.idleframes = []
        self.make_frame_dict()
        self.adjust_images()
        

    def draw(self, surface):
        """Draw method seperated out from update."""
        self.adjust_images()
        surface.blit(self.image, self.rect)

    def make_frame_dict(self):
        """
        Create a dictionary of direction keys to frames. We can use
        transform functions to reduce the size of the sprite sheet we need.
        """
        indices = [[0,0], [1,0], [2,0], [3,0]]
        frames = Support.get_images(type(self).SPRITEIMAGE, indices, self.rect.size)
        self.walkframe_dict = {pygame.K_LEFT : [frames[0], frames[1]],
                  pygame.K_RIGHT: [pygame.transform.flip(frames[0], True, False),
                               pygame.transform.flip(frames[1], True, False)],
                  pygame.K_DOWN : [frames[3],
                               pygame.transform.flip(frames[3], True, False)],
                  pygame.K_UP   : [frames[2],
                               pygame.transform.flip(frames[2], True, False)] }
        self.dieframe_dict = self.walkframe_dict
        self.idleframe_dict = self.walkframe_dict

    def adjust_images(self):
        """Update the sprite's walkframes as the sprite's direction changes."""
        if self.direction != self.old_direction:
            self.walkframes = self.walkframe_dict[self.direction]
            self.dieframes = self.dieframe_dict[self.direction]
            self.idleframes = self.idleframe_dict[self.direction]
            self.old_direction = self.direction
            self.redraw = True
        self.make_image()

    def make_image(self):
        """Update the sprite's animation as needed."""
        now = pygame.time.get_ticks()
        if self.redraw or now-self.animate_timer > 1000/self.animate_fps:
            if(self.status==Interactable.STAT_DIEING):
                self.frame = (self.frame+1)%len(self.dieframes)
                self.image = self.dieframes[self.frame]
            elif self.direction_stack:
                self.frame = (self.frame+1)%len(self.walkframes)
                self.image = self.walkframes[self.frame]
            elif len(self.idleframes)>0:
                self.frame = (self.frame+1)%len(self.idleframes)
                self.image = self.idleframes[self.frame]
            self.animate_timer = now
        if not self.image:
            self.image = self.walkframes[self.frame]
        self.redraw = False

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

    def update(self, obstacles):
        """Adjust the image and move as needed."""
        now = pygame.time.get_ticks()
        if(self.status == Interactable.STAT_DIEING):
            if (self.frame+1 >= self.die_timer): self.OnDeath()
        if(self.health<=0):
            if(self.status == Interactable.STAT_ALIVE): self.start_dieing()
            return
        if(self.cd_Atk>0): 
            self.cd_Atk-=1
        else:
            self.attacking = False
        
        if self.direction_stack or self.direction_offset != pygame.Vector2(0,0):
            self.movement(obstacles, 0)
            self.movement(obstacles, 1)

    def start_dieing(self):
        """ triggers the die-sequence
            returns false if die already started before
        """
        if(self.status != Interactable.STAT_DIEING and self.status != Interactable.STAT_DEAD):
            self.status = Interactable.STAT_DIEING
            self.frame = 0
            self.redraw = True
            self.die_timer = len(self.dieframes)
            return True
        return False

    def OnDeath(self):
        self.kill()

    def attack(self):
        """attack in view direction"""
        if(self.cd_Atk<=0):
            self.cd_Atk = Const.FPS
            self.attacking = True
            #return Fireball.Fireball(self, 10, self.direction)
        else:
            return None

    def damage(self,amount,direction):
        """apply damage to the target"""
        self.health-=amount
        pygame.mixer.Channel(Interactable.SfxCh_Hit).play(type(self).HITSOUND)
        self.direction_offset = Interactable.DIRECT_DICT[direction]
        self.direction_offset = self.direction_offset.elementwise()*10  #push in oposite direction on hit
        

    def movement(self, obstacles, i):
        """Move player and then check for collisions; adjust as necessary.
        i =0 is x; i=1 is y 
        """
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
        self.rect.midbottom = self.hitrect.midbottom

    def adjust_on_collision(self, rect_to_adjust, collide, i):
        """Adjust player's position if colliding with a solid block."""
        if rect_to_adjust[i] < collide.rect[i]:
            rect_to_adjust[i] = collide.rect[i]-rect_to_adjust.size[i]
        else:
            rect_to_adjust[i] = collide.rect[i]+collide.rect.size[i]