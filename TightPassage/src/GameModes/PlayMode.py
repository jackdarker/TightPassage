import pygame
import src.Const as Const
import src.GameMode as GameMode
import src.Block as Block
import src.Interactables.Unit as Unit
import src.GameState as GameState

class PlayMode(GameMode.GameMode):
    def __init__(self,state):     
        super().__init__(state)
        self.obstacles = self.make_obstacles()
        self.player = self.make_player()
        self.player.set_rects(pygame.Rect(50,50,50,50).center, "center")
        self.state.inGame = True

    def processInput(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.notifyQuitRequested()
                break
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.notifyShowMenuRequested()
                    
    def update(self):
        self.player.update(self.obstacles)
        
    def render(self, window):
        window.fill(Const.BACKGROUND_COLOR)
        self.obstacles.draw(window)
        self.player.draw(window)

    def make_player(self):
        return Unit.Unit((0,0,50,50), 3)

    def make_obstacles(self):
        """Prepare some obstacles for our player to collide with."""
        obstacles = [Block.Block((400,400)), Block.Block((300,270)), Block.Block((150,170))]
        for i in range(9):
            obstacles.append(Block.Block((i*50,0)))
            obstacles.append(Block.Block((450,50*i)))
            obstacles.append(Block.Block((50+i*50,450)))
            obstacles.append(Block.Block((0,50+50*i)))
        return pygame.sprite.Group(obstacles)

