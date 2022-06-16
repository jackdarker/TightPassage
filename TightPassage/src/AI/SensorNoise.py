import pygame
import src.Const as Const
import src.Support as Support
from src.Vector import Vector2
from src.Components.UpdatableObj import UpdatableObj
from src.GameState import GameState

def detectInLoS(source,target,obstacles):
    _see=True
    for wall in obstacles:  # wall sprites with a rect attribute
        clip = wall.rect.clipline(source.hitrect.center, target.hitrect.center)
        if clip:
            _see = False
            break
    return(_see)

class SensorNone(UpdatableObj): 
    """ 
    """
    def detectTarget(self,target,obstacles):
        retrun(False)


class SensorNoise(SensorNone): #todo
    """ class that is used to detect noise caaused by player
    """



class SensorLineOfSight(SensorNone):

    def __init__(self,unit,radius):
        self.unit=unit
        self.radius=radius

    def detectTarget(self,target,obstacles):
        _dis=Vector2.distance(self.unit.position,target.position)
        if(_dis>self.radius):
            return(False)
        bFound=detectInLoS(self.unit,target,obstacles)
        return(bFound)
