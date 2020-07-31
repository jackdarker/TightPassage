import os
import pygame
import src.Const as Const
import src.Interactables.Interactable as Interactable

class Unit(Interactable.Interactable):
    SPRITEIMAGE = None

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
        if(type(self).SPRITEIMAGE == None):
            type(self).SPRITEIMAGE = pygame.image.load(os.path.join("assets","sprites","skelly.png")).convert()
            type(self).SPRITEIMAGE.set_colorkey(Const.COLOR_KEY)
        self.direction_stack = []  #Held keys in the order they were pressed.
        self.redraw = False  #Force redraw if needed.
        self.image = None
        self.frame  = 0
        self.frames = self.get_frames()
        self.animate_timer = 0.0
        self.animate_fps = 7.0
        self.walkframes = []
        self.walkframe_dict = self.make_frame_dict()
        self.adjust_images()

    def draw(self, surface):
        """Draw method seperated out from update."""
        surface.blit(self.image, self.rect)

    def get_frames(self):
        """Get a list of all frames."""
        indices = [[0,0], [1,0], [2,0], [3,0]]
        return Interactable.get_images(type(self).SPRITEIMAGE, indices, self.rect.size)

    def make_frame_dict(self):
        """
        Create a dictionary of direction keys to frames. We can use
        transform functions to reduce the size of the sprite sheet we need.
        """
        frames = {pygame.K_LEFT : [self.frames[0], self.frames[1]],
                  pygame.K_RIGHT: [pygame.transform.flip(self.frames[0], True, False),
                               pygame.transform.flip(self.frames[1], True, False)],
                  pygame.K_DOWN : [self.frames[3],
                               pygame.transform.flip(self.frames[3], True, False)],
                  pygame.K_UP   : [self.frames[2],
                               pygame.transform.flip(self.frames[2], True, False)]}
        return frames

    def adjust_images(self):
        """Update the sprite's walkframes as the sprite's direction changes."""
        if self.direction != self.old_direction:
            self.walkframes = self.walkframe_dict[self.direction]
            self.old_direction = self.direction
            self.redraw = True
        self.make_image()

    def make_image(self):
        """Update the sprite's animation as needed."""
        now = pygame.time.get_ticks()
        if self.redraw or now-self.animate_timer > 1000/self.animate_fps:
            if self.direction_stack:
                self.frame = (self.frame+1)%len(self.walkframes)
                self.image = self.walkframes[self.frame]
            self.animate_timer = now
        if not self.image:
            self.image = self.walkframes[self.frame]
        self.redraw = False

    def add_direction(self, key):
        """Add a pressed direction key on the direction stack."""
        if key in DIRECT_DICT:
            if key in self.direction_stack:
                self.direction_stack.remove(key)
            self.direction_stack.append(key)
            self.direction = self.direction_stack[-1]

    def pop_direction(self, key):
        """Pop a released key from the direction stack."""
        if key in DIRECT_DICT:
            if key in self.direction_stack:
                self.direction_stack.remove(key)
            if self.direction_stack:
                self.direction = self.direction_stack[-1]

    def update(self, obstacles):
        """Adjust the image and move as needed."""
        self.adjust_images()
        if self.direction_stack:
            self.movement(obstacles, 0)
            self.movement(obstacles, 1)

    def movement(self, obstacles, i):
        """Move player and then check for collisions; adjust as necessary.
        i =0 is x; i=1 is y 
        """
        direction_vector = DIRECT_DICT[self.direction]
        self.hitrect[i] += self.speed*direction_vector[i]
        callback = collide_other(self.hitrect)  #Collidable callback created.
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