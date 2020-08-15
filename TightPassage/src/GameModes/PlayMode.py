import pygame
import src.Const as Const
import src.GameMode as GameMode
import src.Interactables.Block as Block
import src.Interactables.Unit as Unit
import src.Interactables.Player as Player
import src.GameState as GameState

class PlayMode(GameMode.GameMode):
    def __init__(self,state):     
        super().__init__(state)
        self.obstacles = self.make_obstacles()
        self.units = self.make_units()
        self.shoots = pygame.sprite.Group()
        self.player =  Player.Player((0,0,50,50), 3)
        self.player.set_rects(pygame.Rect(50,50,50,50).center, "center")
        self.state.inGame = True
        self.commands = []

    def processInput(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.notifyQuitRequested()
                break
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.notifyShowMenuRequested()
                elif event.key == Player.Player.KEY_ATTACK:
                    attack = self.player.attack()
                    if attack!= None:
                        attack.addObserver(self)
                        self.shoots.add(attack)
                else: self.player.add_direction(event.key)
            elif event.type == pygame.KEYUP:
                self.player.pop_direction(event.key)

    def update(self):
        #check collision
        for unit in self.units:
            unit.update(self.obstacles)
        for shoot in self.shoots:
            shoot.update(pygame.sprite.Group(self.obstacles,self.units))
        self.player.update(self.obstacles)
        
    def render(self, window):
        window.fill(Const.BACKGROUND_COLOR)
        self.obstacles.draw(window)
        for unit in self.units:
            unit.draw(window)   #todo sort z depth
        self.player.draw(window)
        for unit in self.shoots:
            unit.draw(window)   #todo sort z depth

    def make_obstacles(self):
        """Prepare some obstacles for our player to collide with."""
        obstacles = [Block.Block((400,400)), Block.Block((300,270)), Block.Block((150,170))]
        for i in range(9):
            obstacles.append(Block.Block((i*50,0)))
            obstacles.append(Block.Block((450,50*i)))
            obstacles.append(Block.Block((50+i*50,450)))
            obstacles.append(Block.Block((0,50+50*i)))
        return pygame.sprite.Group(obstacles)

    def make_units(self):
        """Prepare some enemys."""
        obstacles = []
        for i in range(1):
            obstacle = Unit.Unit((0,0,50,50), 3)
            obstacle.set_rects(pygame.Rect(i*50+100,i*50+100,50,50).center, "center")
            obstacles.append(obstacle)
        return pygame.sprite.Group(obstacles)

    def OnHit(self,sprite,otherSprite):
        #kill shoot if shoot hits wall
        if self.shoots.has(sprite) and self.obstacles.has(otherSprite):
           sprite.kill()
        if self.shoots.has(sprite): 
            #check if non-player-shoot hits player
            if self.player == otherSprite and sprite.parent!=self.player:
                sprite.OnHit(otherSprite)

            #check player shoots hits enemy
            elif self.units.has(otherSprite) and sprite.parent==self.player:
                sprite.OnHit(otherSprite) 

            else:
                pass

