import os
import pygame
import src.Const as Const
import src.Support as Support
from src.Vector import Vector2
from src.Components.UpdatableObj import UpdatableObj
from src.Vector import Vector2

class SensorObstacle(UpdatableObj):
    """ class that is used to detect if there is an obstacle in the path
    """

    def __init__(self,unit):
        self.feelers = self.create_feelers(unit)
        pass

    def create_feelers(self,unit):
        """
        Returns feelers in local coordinates.
        """
        feelers = []
        feeler_length = 20.0 #self._params.WallDetectionFeelerLength
        feelers.append(Vector2(unit.rect.center[0],unit.rect.center[1]) + 
                       unit.direction * feeler_length)
        feelers.append(Vector2(unit.rect.center[0],unit.rect.center[1]) + 
                       (unit.direction + unit.direction.perp) * feeler_length  * 0.5 * 0.70710678118654752440084436210485)
        feelers.append(Vector2(unit.rect.center[0],unit.rect.center[1]) + 
                       (unit.direction - unit.direction.perp) * feeler_length  * 0.5 * 0.70710678118654752440084436210485)
        return feelers