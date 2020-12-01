import pygame
import src.Const as Const
from src.UI.Controls import PercentBar

class BattleAvatar(pygame.sprite.Sprite):
    """ represents a character displayed in Battlescreen

    - the character in the screen is represented as pgu-container with additional controls (healthbar,...)
    """
    def __init__(self,char):
        pygame.sprite.Sprite.__init__(self)
        self.char = char
        self.image = pygame.Surface(char.cGraphic.image.get_size()).convert_alpha() #todo where to get size
        self.Health = PercentBar((100,10),[(0,Const.RED),(0.2,Const.YELLOW),(0.5,Const.GREEN)])
        self.rect = self.image.get_rect()
        self.rect.topleft = (0,20)
        pass

    def set_pos(self,position, facing):
        self.HomePosition = position
        setattr(self.rect, "topleft", position)
        #self.char.cGraphic.set_rects(position)
        pass

    def update(self,dt):
        self.image.fill((128, 0, 128,0))
        self.char.cGraphic.update()
        self.char.cGraphic.draw(self.image)
        val = self.char.HP / self.char.MaxHP
        if(self.Health.percent != val):
            self.Health.set_percent(val)
        self.Health.update(dt)
        self.Health.draw(self.image)
            
        pass

    def draw(self,surface):
        pass

