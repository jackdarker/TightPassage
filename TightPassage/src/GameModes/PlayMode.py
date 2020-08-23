import pygame
import src.Const as Const
import src.GameMode as GameMode
import src.Interactables.Block as Block
import src.Interactables.Unit as Unit
import src.Interactables.Player as Player
import src.GameState as GameState
import src.Layers.OgmoImporter as OgmoImporter

class PlayMode(GameMode.GameMode):
    """ implements the behaviour of the game (walking around, hitting walls & enemy)
    """
    def __init__(self,state):
        super().__init__(state)
        loader = OgmoImporter.OgmoImporter()
        self.leveldata = loader.importJson(Const.resource_path("assets/levels/level0.json"))
        self.obstacles = self.make_obstacles()
        self.units = [] #self.make_units()
        self.shoots = pygame.sprite.Group()
        self.player =  Player.Player((0,0,32,32), 3)
        self.player.set_rects(pygame.Rect(120,110,32,32).center, "center")
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
        #self.obstacles.draw(window)
        for layer in self.leveldata.layers:
            self.renderLayer(window,layer, (0,0))
        for unit in self.units:
            unit.draw(window)   #todo sort z depth
        self.player.draw(window)
        for unit in self.shoots:
            unit.draw(window)   #todo sort z depth

    def renderLayer(self,surface,layer,offset=(0,0)):
        """renders the layer to screen-surface
        offset is x,y offset in tiles 
        """
        x = offset[0]
        y = offset[1]
        screenx =0
        screeny =0
        while(y< (offset[1]+layer.CellsY)):
            surface.blit(layer.tileimage, (screenx*layer.cellWidth,screeny*layer.cellHeight,layer.cellWidth,layer.cellHeight),layer.tiles[x,y])
            x +=1
            screenx+=1
            if(((x-offset[0]) // layer.CellsX)>0):
                y+=1
                x = offset[0]
                screenx=0
                screeny+=1

    def make_obstacles(self):
        obstacles = []
        for grid in self.leveldata.grids:
            if(grid.name=="movement"):
                x=0
                y=0
                _flat= grid.grid.flat
                for item in _flat:  #iterating y first !
                    if(item=='2'):
                        block=Block.Block((x*grid.cellWidth,y*grid.cellHeight))
                        obstacles.append(block)
                    y+=1
                    if(((y) //grid.CellsY)>0):
                        x+=1
                        y =0
        return pygame.sprite.Group(obstacles)

    def make_obstacles_old(self):
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

