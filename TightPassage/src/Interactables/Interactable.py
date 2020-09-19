import pygame

class Interactable(pygame.sprite.Sprite):

    _next_valid_id = 1

    @staticmethod
    def get_next_valid_id():
        return Interactable._next_valid_id

    @staticmethod
    def reset_next_valid_id():
        Interactable._next_valid_id = 0

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

    def __init__(self,rect,direction,new_id=0):
        if(new_id==0):
            new_id=Interactable.get_next_valid_id()
        else:
            assert new_id >= Interactable._next_valid_id, "invalid id '{0}' <= {1}".format(new_id,
                                                                                         Interactable._next_valid_id)
        self._id = new_id
        Interactable._next_valid_id = self._id + 1

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
        self.enabled = True #enables update evaluation

    ID = property(lambda self: self._id, "unique id")

    def set_rects(self, value, attribute="topleft"):
        """
        Set the position of both self.rect and self.hitrect together.
        The attribute of self.rect will be set to value; then the midbottom
        points will be set equal.
        """
        setattr(self.rect, attribute, value)
        self.hitrect.center = self.rect.center

    def collide_other(self,myrect):
        """ The other argument is a pygame.Rect that you would like to use for
        sprite collision. Return value is a collided callable for use with the
        pygame.sprite.spritecollide function.
        """
        def collide(one, two):
            return myrect.colliderect(two.rect)
        return collide

    def update(self):
        pass

    def addObserver(self, observer):
        self.__observers.append(observer)

    def removeObserver(self, observer):
        if(self.__observers.count(observer)):
            self.__observers.remove(observer)

    def notifyOnHit(self,otherSprite):
        for observer in self.__observers:
            observer.OnHit(self,otherSprite)
