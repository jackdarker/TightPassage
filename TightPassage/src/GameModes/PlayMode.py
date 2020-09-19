import pygame
import pyscroll
import src.Const as Const
import src.Support as Support
import src.GameMode as GameMode
import src.Interactables.Block as Block
import src.Interactables.Unit as Unit
import src.Interactables.Player as Player
import src.Interactables.Imp as Imp
from src.GameState import GameState
import pytmx
from src.Components.TiledImporter import TiledImporter
import src.Components.MazeGenerator as MazeGenerator

class PlayMode(GameMode.GameMode):
    """ implements the behaviour of the game (walking around, hitting walls & enemy)
    """
    def __init__(self,state):
        super().__init__(state)
        state.addObserver(self)
        self.group=None
        self.startNewGame()
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
        pass

    def startNewGame(self):
        #self.state.fileName = Const.resource_path("assets/levels/Level0.tmx")
        #todo put this into a loader ?
        gbuilder = MazeGenerator.GridBuilderRect()
        gbuilder.setParams(5, 4)
        if(self.state.mazeGenerator!=None and 
           type(self.state.mazeGenerator)==type('')):   #text should be a classname (subclass of mazegenerator) 
            mzbuilder =getattr(MazeGenerator,self.state.mazeGenerator)() #getattr on a module returns a class or function
        else: mzbuilder = MazeGenerator.MazeGenerator()
        mzbuilder.setParams(10, gbuilder)
        mzbuilder.createMap()
        lvlbuilder = MazeGenerator.RoomDesigner()
        lvlbuilder.setMapNodes(mzbuilder.nodes)
        lvlbuilder.parseLevelTemplates([Const.resource_path("assets/levels/Level0.tmx"),
                                        Const.resource_path("assets/levels/Level1.tmx"),
                                        Const.resource_path("assets/levels/Level2.tmx"),
                                        Const.resource_path("assets/levels/Level3.tmx"),
                                        Const.resource_path("assets/levels/Level4.tmx"),
                                        Const.resource_path("assets/levels/Level5.tmx"),
                                        Const.resource_path("assets/levels/Level6.tmx"),
                                        Const.resource_path("assets/levels/Level7.tmx"),
                                        Const.resource_path("assets/levels/Level8.tmx"),
                                        Const.resource_path("assets/levels/Level9.tmx"),
                                        Const.resource_path("assets/levels/Level10.tmx"),
                                        Const.resource_path("assets/levels/Level11.tmx"),
                                        Const.resource_path("assets/levels/Level12.tmx"),
                                        Const.resource_path("assets/levels/Level13.tmx"),
                                        Const.resource_path("assets/levels/Level14.tmx")])
        lvlbuilder.createWorld()
        self.state.mazeNodes = lvlbuilder.nodes
        self.loadLevel(MazeGenerator.MapNode.getPlayerSpawnNode(self.state.mazeNodes))

    def loadLevel(self,targetNode, playerSpawnPoint=None):
        #cleanup actual level
        for door in self.state.doors:
            door.removeObserver(self)
        if(self.group!=None):
            self.group.remove(self.state.obstacles)
            self.group.remove(self.state.doors)
            self.group.remove(self.state.units)
            self.group.remove(self.state.player)
            self.group.remove(self.state.shoots)

        self.state.currentMazeNode = targetNode
        importer = TiledImporter(self.state)
        self.tiled_map = importer.loadMap(targetNode.fileName)
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
                    if(door.target == playerSpawnPoint): 
                        self.state.player.set_rects(door.rect.center, "center") #.move(-64,0)
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


    def OBSOLETE_renderLayer(self,surface,layer,offset=(0,0)): #not used , using pyscroll
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
        if(warp.target != None):
            #self.state.fileName = Const.resource_path("assets/levels/"+warp.map)
            map=self.state.currentMazeNode.doorResolver(self.state.mazeNodes,self.state.currentMazeNode,warp.target)
            self.loadLevel(map,warp.target,)
        else:
            pass #todo


