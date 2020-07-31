import pygame

def collide_other(other):
    """
    The other argument is a pygame.Rect that you would like to use for
    sprite collision. Return value is a collided callable for use with the
    pygame.sprite.spritecollide function.
    """
    def collide(one, two):
        return other.colliderect(two.rect)
    return collide

def get_images(sheet, frame_indices, size):
    """Get desired images from a sprite sheet image."""
    frames = []
    for cell in frame_indices:
        frame_rect = ((size[0]*cell[0],size[1]*cell[1]), size)
        frames.append(sheet.subsurface(frame_rect))
    return frames

class Interactable(pygame.sprite.Sprite):
    STAT_ALIVE = "alive"
    def __init__(self,rect,direction):
        #self.state = state
        self.status = Interactable.STAT_ALIVE
        pygame.sprite.Sprite.__init__(self)
        self.rect = pygame.Rect(rect)
        self.direction = direction
        self.old_direction = None  #The Players previous direction every frame.

    def set_rects(self, value, attribute="topleft"):
        """
        Set the position of both self.rect and self.hitrect together.
        The attribute of self.rect will be set to value; then the midbottom
        points will be set equal.
        """
        setattr(self.rect, attribute, value)
        self.hitrect.midbottom = self.rect.midbottom
