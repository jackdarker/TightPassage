import pygame
import pyscroll
import src.Const as Const
import src.GameMode as GameMode
import src.Interactables.Block as Block
import src.Interactables.Unit as Unit
import src.Interactables.Player as Player
import src.Interactables.Imp as Imp
import src.GameState as GameState
import src.Layers.OgmoImporter as OgmoImporter
import pytmx
from pytmx.util_pygame import load_pygame


class PlayMode(GameMode.GameMode):
    """ implements the behaviour of the game (walking around, hitting walls & enemy)
    """
    def __init__(self,state):
        super().__init__(state)
        self.tiled_map = load_pygame(Const.resource_path("assets/levels/Arena.tmx"))

        # create new data source for pyscroll
        map_data = pyscroll.data.TiledMapData(self.tiled_map)

        # create new renderer (camera)
        self.map_layer = pyscroll.BufferedRenderer(map_data, Const.WINDOW_SIZE, clamp_camera=False, tall_sprites=1)
        self.map_layer.zoom = 1

        # pyscroll supports layered rendering.  our map has 3 'under' layers
        # layers begin with 0, so the layers are 0, 1, and 2.
        # since we want the sprite to be on top of layer 1, we set the default
        # layer for sprites as 2
        self.group = pyscroll.PyscrollGroup(map_layer=self.map_layer, default_layer=2)

        self.units = []
        self.shoot = []
        #loader = OgmoImporter.OgmoImporter()
        #self.leveldata = loader.importJson(Const.resource_path("assets/levels/level0.json"))
        self.obstacles = self.make_obstacles()
        self.units = self.make_units()
        self.shoots = pygame.sprite.Group()
        self.player =  Player.Player((0,0,32,32), 3)
        self.player.set_rects(pygame.Rect(120,110,32,32).center, "center")
        self.group.add(self.player)
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
        self.group.update(self.obstacles)
        return
        # check if the sprite's feet are colliding with wall
        # sprite must have a rect called feet, and move_back method,
        # otherwise this will fail
        for sprite in self.group.sprites():
            if sprite.feet.collidelist(self.obstacles) > -1:
                sprite.move_back(dt)

        #check collision
        for unit in self.units:
            unit.update(self.obstacles)
        for shoot in self.shoots:
            shoot.update(pygame.sprite.Group(self.obstacles,self.units))
        self.player.update(self.obstacles)
        
    def render(self, window):
         # center the map/screen on our Hero
        self.group.center(self.player.rect.center)
        for unit in self.units:
            unit.draw(window)   #todo sort z depth
        self.player.draw(window)
        for unit in self.shoots:
            unit.draw(window)   #todo sort z depth
        # draw the map and all sprites
        self.group.draw(window)
        return

        window.fill(Const.BACKGROUND_COLOR)
        #self.obstacles.draw(window)
        for layer in self.leveldata.layers:
            self.renderLayer(window,layer, (0,0))
        

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
        obstacles = list()
        for object in self.tiled_map.objects:
            obstacles.append(Block.Block(pygame.Rect(object.x, object.y,object.width, object.height)))
        return pygame.sprite.Group(obstacles)

        #obstacles = []
        #for grid in self.leveldata.grids:
        #    if(grid.name=="movement"):
        #        x=0
        #        y=0
        #        _flat= grid.grid.flat
        #        for item in _flat:  #iterating y first !
        #            if(item=='2'):
        #                block=Block.Block((x*grid.cellWidth,y*grid.cellHeight))
        #                obstacles.append(block)
        #            y+=1
        #            if(((y) //grid.CellsY)>0):
        #                x+=1
        #                y =0
        #return pygame.sprite.Group(obstacles)

    def make_units(self):
        """Prepare some enemys."""
        obstacles = []
        for i in range(1):
            obstacle = Imp.Imp((0,0,50,50))
            obstacle.set_rects(pygame.Rect(i*50+100,i*50+100,50,50).center, "center")
            obstacles.append(obstacle)
            self.group.add(obstacle)
        return pygame.sprite.Group(obstacles)

    def OnHit(self,sprite,otherSprite):
        #kill shoot if shoot hits wall
        if self.shoots.has(sprite) and self.obstacles.has(otherSprite):
           sprite.OnHit(otherSprite)
           #sprite.kill()
        if self.shoots.has(sprite): 
            #check if non-player-shoot hits player
            if self.player == otherSprite and sprite.parent!=self.player:
                sprite.OnHit(otherSprite)

            #check player shoots hits enemy
            elif self.units.has(otherSprite) and sprite.parent==self.player:
                sprite.OnHit(otherSprite) 

            else:
                pass

