import pygame
import pyscroll
import src.Const as Const
import src.GameMode as GameMode
import src.Interactables.Block as Block
import src.Interactables.Unit as Unit
import src.Interactables.Player as Player
import src.Interactables.Imp as Imp
from src.GameState import GameState
import pytmx
from src.Components.TiledImporter import TiledImporter

class PlayMode(GameMode.GameMode):
    """ implements the behaviour of the game (walking around, hitting walls & enemy)
    """
    def __init__(self,state):
        super().__init__(state)
        state.addObserver(self)
        self.loadLevel()
        self.state.inGame = True

    def processInput(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.notifyQuitRequested()
                break
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.notifyShowMenuRequested()
                elif event.key == Player.Player.KEY_ATTACK:
                    attack = self.state.player.attack()
                    if attack!= None:
                        attack.addObserver(self)
                        self.state.shoots.add(attack)
                        self.group.add(attack)
                else: self.state.player.add_direction(event.key)
            elif event.type == pygame.KEYUP:
                self.state.player.pop_direction(event.key)
            #elif event.type == pygame.MOUSEMOTION:
            #    print(event.pos)

    def loadLevel(self, playerSpawnPoint=None):
        importer = TiledImporter(self.state)
        self.tiled_map = importer.loadMap(self.state.fileName)
        # create new data source for pyscroll and create new renderer (camera)
        self.map_layer = pyscroll.BufferedRenderer(pyscroll.data.TiledMapData(self.tiled_map), 
                                                   Const.WINDOW_SIZE, clamp_camera=False, tall_sprites=1)
        self.map_layer.zoom = 1
        # pyscroll supports layered rendering.  our map has 3 'under' layers
        # layers begin with 0, so the layers are 0, 1, and 2.
        # since we want the sprite to be on top of layer 1, we set the default
        # layer for sprites as 2
        self.group = pyscroll.PyscrollGroup(map_layer=self.map_layer, default_layer=2)

        #self.state.obstacles = self.make_obstacles()
        #self.state.units = self.make_units()
        #self.state.shoots = pygame.sprite.Group()
        self.group.add(self.state.obstacles)
        self.group.add(self.state.doors)
        self.group.add(self.state.units)
        self.group.add(self.state.player)
        self.group.add(self.state.shoots)

        for door in self.state.doors:
            door.addObserver(self)

        if(playerSpawnPoint!=None):
            if(type(playerSpawnPoint)==pygame.Rect):
                self.state.player.set_rects(playerSpawnPoint.center, "center")
                pass
            else:
                #spawnPoint is a text-label
                if(playerSpawnPoint=="north"):playerSpawnPoint ="south"
                elif(playerSpawnPoint=="south"):playerSpawnPoint ="north"
                elif(playerSpawnPoint=="east"):playerSpawnPoint ="west"
                elif(playerSpawnPoint=="west"):playerSpawnPoint ="east"
                for door in self.state.doors:
                    if(door.target == playerSpawnPoint): self.state.player.set_rects(door.rect.center, "center") #.move(-64,0)
                    pass

    def update(self):
        self.group.update()
        return
        
    def render(self, window):
        #window.fill(Const.BACKGROUND_COLOR)
         # center the map/screen on our Hero
        #   no camera tracking? 
        #self.group.center(self.levelData.player.rect.center)
        for unit in self.state.units:
            unit.draw(window)   #todo sort z depth
        self.state.player.draw(window)
        for unit in self.state.shoots:
            unit.draw(window)   #todo sort z depth
        # draw the map and all sprites
        self.group.draw(window)
        return


    def OBSOLETE_renderLayer(self,surface,layer,offset=(0,0)):
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
        return


    def OnHit(self,sprite,otherSprite):
        """called by notifyOnHit"""
        if(self.state.doors.has(sprite)):
            self.state.notifyWarpTriggered(sprite)
            return
        #kill shoot if shoot hits wall
        if self.state.shoots.has(sprite) and self.state.obstacles.has(otherSprite):
           sprite.OnHit(otherSprite)
           #sprite.kill()
        elif self.state.shoots.has(sprite): 
            #check if non-player-shoot hits player
            if self.state.player == otherSprite and sprite.parent!=self.state.player:
                sprite.OnHit(otherSprite)

            #check player shoots hits enemy
            elif self.state.units.has(otherSprite) and sprite.parent==self.state.player:
                sprite.OnHit(otherSprite) 

            else:
                pass
        return

    def warpTriggered(self,warp):
        """called on door/teleporter trigger"""
        if(warp.map != None):
            self.state.fileName = Const.resource_path("assets/levels/"+warp.map)
            self.playerSpawn = warp.target
            self.loadLevel(self.playerSpawn)
        else:
            pass #todo


