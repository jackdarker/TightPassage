import pygame
import src.Const as Const
import src.Support as Support
from src.UI.Controls import *

class test():
    def __init__(self):
        pygame.init()
        pygame.display.set_mode(Const.WINDOW_SIZE)
        self.screen = pygame.display.get_surface()
        self.screen_rect = self.screen.get_rect()
        self.clock = pygame.time.Clock()
        self.fps = 60.0
        self.done = False
        self.keys = pygame.key.get_pressed()
        self.Health = PercentBar((100,10),[(0,Const.RED),(0.2,Const.YELLOW),(0.5,Const.GREEN)])
        self.Health.rect.topleft=(50,100)
        self.Health2 = PercentBar((20,50),[(0,Const.RED),(0.2,Const.YELLOW),(0.5,Const.GREEN)],horizontal=False)
        self.Health2.rect.topleft=(200,100)

    def event_loop(self):
        """Add/pop directions from player's direction stack as necessary."""
        for event in pygame.event.get():
            self.keys = pygame.key.get_pressed()
            if event.type == pygame.QUIT or self.keys[pygame.K_ESCAPE]:
                self.done = True
            elif event.type == pygame.KEYDOWN:
                #self.Health.set_percent(self.Health.percent-0.3)
                pass
            elif event.type == pygame.KEYUP:
                if(event.key== pygame.K_s):
                    self.Health.set_percent(self.Health.percent-0.3)
                    self.Health2.set_percent(self.Health.percent-0.3)
                elif(event.key== pygame.K_a):
                    self.Health.set_percent(self.Health.percent+0.1)
                    self.Health2.set_percent(self.Health.percent+0.1)
                pass

    def draw(self):
        """Draw all elements to the display surface."""
        self.screen.fill(Const.BRIGHT_GRAY)
        self.Health.update(10)
        self.Health.draw(self.screen)
        self.Health2.update(10)
        self.Health2.draw(self.screen)

    def display_fps(self):
        """Show the program's FPS in the window handle."""
        caption = "{} - FPS: {:.2f}".format("test", self.clock.get_fps())
        pygame.display.set_caption(caption)

    def main_loop(self):
        """Our main game loop; I bet you'd never have guessed."""
        while not self.done:
            self.event_loop()
            self.draw()
            pygame.display.update()
            self.clock.tick(self.fps)
            self.display_fps()


if __name__ == "__main__":
    test().main_loop()