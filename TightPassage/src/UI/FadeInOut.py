import pygame
import src.Const as Const

class FadeInOut(pygame.sprite.Sprite):
    MODE_OFF = 0
    MODE_FADEOUT = 1
    MODE_FADEIN = 2
    MODE_BLACKSCREEN = 3

    def __init__(self, CB_onDone =  None):
        self.CB_onDone = CB_onDone
        pygame.sprite.Sprite.__init__(self)
        self.rect = pygame.Rect((0,0),Const.WINDOW_SIZE)
        self.image = pygame.Surface(Const.WINDOW_SIZE)
        self.image.fill((0, 0, 0))
        self.done = True
        self.mode = FadeInOut.MODE_OFF
        self.alpha = 0
        self.acceleration = 0.01
        self.speed = self.defaultspeed = 2/100

    def set_faded(self):
        """switches immediatly to black screen
        """
        self.done = False
        self.mode == FadeInOut.MODE_BLACKSCREEN

    def start_FadeOut(self):
        self.done = False
        self.speed = self.defaultspeed
        self.mode = FadeInOut.MODE_FADEOUT

    def start_FadeIn(self,fromBlack):
        self.done = False
        self.speed = self.defaultspeed
        self.mode = FadeInOut.MODE_FADEIN
        if(fromBlack): self.alpha = 255
    
    def _onDone(self):
        if(self.CB_onDone): self.CB_onDone(self.mode)

    def update(self, dt):
        if(self.done or self.mode == FadeInOut.MODE_OFF):
            return
        self.speed += self.acceleration * dt
        if(self.mode == FadeInOut.MODE_FADEOUT):
            self.alpha += 8#(self.speed*dt)
            if self.alpha >= 255:
                self.done = True
                self._onDone()
        elif(self.mode == FadeInOut.MODE_BLACKSCREEN):
            self.alpha = 255
            self.done = True
            self._onDone()
        else:
            self.alpha -= 8#(self.speed*dt)
            if self.alpha <= 0:
                self.done = True
                self._onDone()
           
    def draw(self, surface):
        if self.mode != FadeInOut.MODE_OFF:
            self.image.set_alpha(self.alpha)
            surface.blit(self.image, (0, 0))
