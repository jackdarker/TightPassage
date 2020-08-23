import os, sys
from os.path import abspath
import json
from stat import *
import pygame
import numpy as np
import src.Const as Const
import src.Support as Support
from pygame.math import Vector2

class OgmoImporter():
    """ imports Ogmo3-Json files
    tileset-label needs to match the relative path to the asset f.e. assets/sprites/Tileset.png
    """
    def __init__(self):
        pass

    def importJson(self,pathToJson):
        self.level = LevelData()
        with open(abspath(pathToJson)) as json_file:
            data = json.load(json_file)
            version = data.get("ogmoVersion")   #todo throw exception if not ogmofile or wrong vresion
            if(version==None): 
                raise LookupError("invalid version in file ",pathToJson)
            self.level.width = data["width"]
            self.level.height =data["height"]
            self.level.layers=[]
            self.level.grids=[]
            for layer in data['layers']:
                _layer = self.extractLayer(layer)
                if(_layer!=None and _layer.type=="tile"): self.level.layers.append(_layer)
                if(_layer!=None and _layer.type=="grid"): self.level.grids.append(_layer)
            self.level.layers.reverse() #in ogmo lowest level is drawed on top
        return self.level

    def extractLayer(self,layerdata):
        layer = LayerData()
        layer.type = None
        layer.name = layerdata["name"]
        layer.width = self.level.width
        layer.height = self.level.height
        layer.cellWidth = layerdata["gridCellWidth"]
        layer.cellHeight = layerdata["gridCellHeight"]
        layer.CellsX = layerdata["gridCellsX"]
        layer.CellsY = layerdata["gridCellsY"]
        if(layerdata.get("entities")!=None): # entity layer
            return None
        elif(layerdata.get("grid")!=None):
            layer.type = "grid"
            layer.grid = self.extractGrid(layerdata,layer)
            return layer
        elif(layerdata.get("decals")!=None):
            return None
        else:   #tile layer
            exportMode =  layerdata["exportMode"]
            arrayMode = layerdata["arrayMode"]
            layer.type = "tile"
            layer.tilesetpath = layerdata["tileset"]
            layer.tileimage = pygame.image.load(Const.resource_path(layer.tilesetpath)).convert_alpha()
            layer.tiles =self.extractTiles(layerdata,layer)
        return layer

    def extractGrid(self,layerdata,layer):
        name = layerdata["name"]
        data = layerdata.get("grid")
        maxx = layer.CellsX
        if(data!=None): #1D array with 1 char
            return np.reshape(data,(maxx,-1),order='F')
        else:
            raise LookupError("invalid dataformat in layer ",name)  #todo add other formats
        pass

    def extractTiles(self,layerdata,layer):
        name = layerdata["name"]
        data = layerdata.get("data")
        if(data!=None): #1D array with frameID
            layercoords = []
            tilecoords = []
            maxtilex = layer.tileimage.get_width() // layer.cellWidth
            maxx = layer.CellsX
            
            x = -1
            y = 0
            for id in data:
                x +=1
                if((x // maxx)>0):
                   y+=1
                   x = 0

                _x = pygame.Rect(x * layer.cellWidth,
                                    y * layer.cellHeight,
                                    layer.cellWidth,layer.cellHeight)
                _y = pygame.Rect((id%maxtilex)*layer.cellWidth,
                                 (id//maxtilex)*layer.cellHeight,
                                 layer.cellWidth,layer.cellHeight)
                layercoords.append(_x)
                tilecoords.append(_y)
            return np.reshape(tilecoords,(maxx,-1,4),order='F')
            #return self.createLayerSurface(layercoords,tilecoords,layer.tileimage)

        else:
            raise LookupError("invalid dataformat in layer ",name)  #todo add other formats
            data = layerdata.get("dataCoord")
            if(data!=None):
                
                pass
            else:
                data = layerdata.get("data2D")
                if(data!=None):
                    pass
                else:
                    data = layerdata.get("dataCoords2D")
                    if(data!=None):
                        pass
                    else:
                        raise LookupError("invalid dataformat in layer ",name)
                    pass
        pass

    def createLayerSurface(self, layercoords, tilecoords, tilesheet):
        surface = pygame.Surface((self.level.width,self.level.height),pygame.SRCALPHA)
        i=0
        for tilecoord in tilecoords:
            if(tilecoord[0]>=0 and tilecoord[1]>=0):
                surface.blit(tilesheet, layercoords[i],tilecoord)
            i+=1
        return surface

class LevelData():
    def __init__(self):
        pass

class LayerData():
    """struct for layer data
    type="tile" => struct contains tiles to render
    type="grid" => struct contains grid for static collisionobjects
    """
    def __init__(self):
        pass

def renderLayer(surface,layer,offset=(0,0)):
    """renders the layer to screen-surface
    offset is x,y offset in tiles 
    """
    screensize=surface.get_size()
    countx = screensize[0]//layer.cellWidth
    county = screensize[1]//layer.cellHeight
    x = offset[0]
    y = offset[1]
    screenx =0
    screeny =0
    while(x< (offset[0]+countx) and y< (offset[1]+county)):
        surface.blit(layer.tileimage, (screenx*layer.cellWidth,screeny*layer.cellHeight,layer.cellWidth,layer.cellHeight),layer.tiles[x,y])
        x +=1
        screenx+=1
        if(((x-offset[0]) // countx)>0):
            y+=1
            x = offset[0]
            screenx=0
            screeny+=1

def renderGrid(surface,layer,offset=(0,0)):
    """renders the layer to screen-surface
    offset is x,y offset in tiles 
    """
    screensize=surface.get_size()
    countx = screensize[0]//layer.cellWidth
    county = screensize[1]//layer.cellHeight
    x = offset[0]
    y = offset[1]
    screenx =0
    screeny =0
    colors = {'0':(0,100,0,0),'1':(255,0,0,255)}
    while(x< (offset[0]+countx) and y< (offset[1]+county)):
        color = colors[layer.grid[x,y]]
        if(layer.grid[x,y]!='0'): pygame.draw.rect(surface,color, (screenx*layer.cellWidth,screeny*layer.cellHeight,layer.cellWidth,layer.cellHeight),1)
        x +=1
        screenx+=1
        if(((x-offset[0]) // countx)>0):
            y+=1
            x = offset[0]
            screenx=0
            screeny+=1

if __name__ == '__main__':
    pygame.init()
    screen = pygame.display.set_mode((640,480), pygame.HWSURFACE | pygame.DOUBLEBUF )
    screen2 = pygame.Surface(screen.get_size(), flags=pygame.HWSURFACE | pygame.SRCALPHA)
    creator = OgmoImporter()
    level = creator.importJson(Const.resource_path("assets/levels/level0.json"))
    screen2.fill(Const.BACKGROUND_COLOR)
    for layer in level.layers:
        renderLayer(screen2,layer, (0,0))
    for grid in level.grids:
        renderGrid(screen2,grid, (0,0))
        pass
        #screen.blit(layer.surface,pygame.Rect(0,0,level.width,level.height))
    screen.blit(screen2,(0,0,0,0))
    pygame.display.flip()
    while(True):
        pass
    pass

