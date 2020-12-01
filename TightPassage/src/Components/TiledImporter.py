import pygame
import numpy as np
import src.Const as Const
from src.GameState import GameState
from pytmx.util_pygame import  load_pygame
import src.Interactables.Block as Block
import src.Interactables.Unit as Unit
import src.Interactables.Player as Player
import src.Interactables.Imp as Imp
import src.Interactables.Warp as Warp
import src.Interactables.Container as Container

class TiledImporter():
    """imports a map defined in Tiled and stores it in GameState-Singleton"""

    def __init__(self,state):
        self.state = state
        pass

    def loadMap(self,filename):
        self.tiled_map = load_pygame(filename)      #todo error when loading objects with property of type 'object'
        self.parseObjects()
        return self.tiled_map

    def parseObjects(self):
        self.state.obstacles = pygame.sprite.Group()
        self.state.units = pygame.sprite.Group()
        self.state.doors = pygame.sprite.Group()
        self.state.shoots = pygame.sprite.Group()
        for object in self.tiled_map.objects:
            if(object.type=='Wall'):
                obstacle = Block.Block(pygame.Rect(object.x, object.y,object.width, object.height))
                self.state.obstacles.add(obstacle)
            elif(object.type=='Enemy'):
                obstacle = Imp.Imp((0,0,50,50)) #todo dynamic enemy creation
                obstacle.set_rects(pygame.Rect(object.x, object.y,50, 50).center, "center")
                self.state.units.add(obstacle)
            elif(object.type=='Warp'):
                obstacle = Warp.Warp(pygame.Rect(object.x, object.y,object.width, object.height))
                obstacle.setTarget(object.properties.get('map'),object.properties.get('target'),object.properties.get('world'))
                self.state.doors.add(obstacle)
            elif(object.type=='Player'):
                self.playerSpawn = pygame.Rect(object.x, object.y,64,64)
                if(self.state.player == None): self.state.player =  Player.Player((0,0,0,0), 3)
                self.state.player.set_rects(self.playerSpawn.center, "center")
            elif(object.type=='Trigger'):
                if(object.ID=='$Chest'):
                    obstacle = Container.Chest(pygame.Rect(0,0,32,32)) 
                    obstacle.image = object.image
                    obstacle.set_rects(pygame.Rect((object.x, object.y),object.image.get_size()).center, "center")
                    self.state.units.add(obstacle)
                else:   #if ID is not a keyword it is aconcrete class , f.e. 'Tutorial.Tutorial1'
                    if(object.OnEnter=='showScene'):
                        obstacle = Warp.Trigger(pygame.Rect(0,0,32,32), 
                            CB_onEnter = GameState().notifySceneTriggered, params =object.properties.get('ID')) 
                        obstacle.image = object.image
                        obstacle.set_rects(pygame.Rect((object.x, object.y),object.image.get_size()).center, "center")
                        self.state.units.add(obstacle)
                    elif(object.OnEnter=='startBattle'):
                        obstacle = Warp.Trigger(pygame.Rect(0,0,32,32), 
                            CB_onEnter = GameState().notifyBattleTriggered, params =object.properties.get('ID')) 
                        obstacle.image = object.image
                        obstacle.set_rects(pygame.Rect((object.x, object.y),object.image.get_size()).center, "center")
                        self.state.units.add(obstacle)
                pass

