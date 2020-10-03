import pygame
import src.GameMode as GameMode

class MessageMode(GameMode.GameMode):
    def __init__(self,state,message):
        self.state = state
        super().__init__(self.state)
        #self.font = pygame.font.Font("assets/ui/BD_Cartoon_Shout.ttf", 36)
        self.font = pygame.font.Font(pygame.font.get_default_font(),36)
        self.message = message
        self.enabled=True

    def processInput(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.notifyQuitRequested()
                break
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE \
                or event.key == pygame.K_SPACE \
                or event.key == pygame.K_RETURN:
                    self.resume_game()
                    
    def update(self,dt):
        pass
        
    def render(self, window):
        surface = self.font.render(self.message, True, (200, 0, 0))
        x = (window.get_width() - surface.get_width()) // 2
        y = (window.get_height() - surface.get_height()) // 2
        window.blit(surface, (x, y))

    def resume_game(self):
        self.enabled=False
