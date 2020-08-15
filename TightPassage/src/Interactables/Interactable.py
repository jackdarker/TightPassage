import pygame

class Interactable(pygame.sprite.Sprite):

    #using channels for different sound effects to be able to use channel.get_busy 
    SfxCh_Move = 1
    SfxCh_Attack = 2
    SfxCh_Hit = 3

    #map of movementkeys to movement direction
    DIRECT_DICT = {pygame.K_LEFT  : pygame.Vector2(-1, 0),
               pygame.K_RIGHT : pygame.Vector2( 1, 0),
               pygame.K_UP    : pygame.Vector2( 0,-1),
               pygame.K_DOWN  : pygame.Vector2( 0, 1)}

    #codes for self.status
    STAT_ALIVE = "alive"
    STAT_DIEING = "dieing"
    STAT_DEAD = "dead"

    def __init__(self,rect,direction):
        self.__observers = []
        self.status = Interactable.STAT_ALIVE
        pygame.sprite.Sprite.__init__(self)
        self.rect = pygame.Rect(rect)
        self.direction = direction
        self.old_direction = None  #The Players previous direction every frame.
        self.parent = None
        self.redraw = False  #Force redraw if needed.
        self.frame  = 0
        self.animate_timer = 0.0
        self.animate_fps = 7.0  #todo animationdataclass
        self.die_timer = 0.0
        self.image = None   # the image to render in next frame

    def set_rects(self, value, attribute="topleft"):
        """
        Set the position of both self.rect and self.hitrect together.
        The attribute of self.rect will be set to value; then the midbottom
        points will be set equal.
        """
        setattr(self.rect, attribute, value)
        self.hitrect.midbottom = self.rect.midbottom

    def collide_other(self,other):
        """ The other argument is a pygame.Rect that you would like to use for
        sprite collision. Return value is a collided callable for use with the
        pygame.sprite.spritecollide function.
        """
        def collide(one, two):
            return other.colliderect(two.rect)
        return collide

    def addObserver(self, observer):
        self.__observers.append(observer)

    def removeObserver(self, observer):
        if(self.__observers.count(observer)):
            self.__observers.remove(observer)

    def notifyOnHit(self,otherSprite):
        for observer in self.__observers:
            observer.OnHit(self,otherSprite)
