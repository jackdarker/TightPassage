import os
from sys import maxsize as sys_maxsize
import math as math
import pygame
import src.Const as Const
import src.Support as Support
import src.Vector as Vector
from src.Vector import Vector2,EPSILON
from src.Components.UpdatableObj import UpdatableObj
from src.GameState import GameState

class BehaviourNone(UpdatableObj):
    def __init__(self, unit):
        self.mob = unit
        pass
    
    def update(self, milliseconds):
        pass

class BehaviourSteering(BehaviourNone):
    """ class used to move a mob in the world 
    """

    def __init__(self, unit):
        self.mob = unit     #vehicle this behaviour is parented to
        self.steering_force = Vector2.zero()    # calculated force applied to the vehicle
        pass

    def point_to_world_2d(local_point, x_axis, y_axis, global_pos):
        # m11 m12 m13       r11 r12 t13       xax yax pox
        # m21 m22 m23  =>   r21 r22 t23  =>   xay yay poy
        # m31 m32 m33       m31 m32 1.0       m31 m32 1.0
        assert x_axis.length < 1.0 + EPSILON and x_axis.length > 1.0 - EPSILON
        assert y_axis.length < 1.0 + EPSILON and y_axis.length > 1.0 - EPSILON
        return Vector2(x_axis.x * local_point.x + y_axis.x * local_point.y + global_pos.x,
                   x_axis.y * local_point.x + y_axis.y * local_point.y + global_pos.y)


    def point_to_local_2d(global_point, x_axis, y_axis, position):
        # m11 m12 m13       r11 r12 t13       xax xay -pox
        # m21 m22 m23  =>   r21 r22 t23  =>   yax yay -poy
        # m31 m32 m33       m31 m32 1.0       m31 m32 1.0
        assert x_axis.length < 1.0 + EPSILON and x_axis.length > 1.0 - EPSILON
        assert y_axis.length < 1.0 + EPSILON and y_axis.length > 1.0 - EPSILON
        gx = global_point.x - position.x
        gy = global_point.y - position.y
        return Vector2(x_axis.x * gx + x_axis.y * gy,
                   y_axis.x * gx + y_axis.y * gy)


    def vector_to_world_2d(local_vector, x_axis, y_axis):
        # m11 m12 m13       r11 r12 t13       xax yax pox
        # m21 m22 m23  =>   r21 r22 t23  =>   xay yay poy
        # m31 m32 m33       m31 m32 1.0       m31 m32 1.0
        assert x_axis.length < 1.0 + EPSILON and x_axis.length > 1.0 - EPSILON
        assert y_axis.length < 1.0 + EPSILON and y_axis.length > 1.0 - EPSILON
        return Vector2(x_axis.x * local_vector.x + y_axis.x * local_vector.y,
                   x_axis.y * local_vector.x + y_axis.y * local_vector.y)


    def vector_to_local_2d(global_vector, x_axis, y_axis):
        # m11 m12 m13       r11 r12 t13       xax yax pox
        # m21 m22 m23  =>   r21 r22 t23  =>   xay yay poy
        # m31 m32 m33       m31 m32 1.0       m31 m32 1.0
        assert x_axis.length < 1.0 + EPSILON and x_axis.length > 1.0 - EPSILON
        assert y_axis.length < 1.0 + EPSILON and y_axis.length > 1.0 - EPSILON
        return Vector2(x_axis.x * global_vector.x + x_axis.y * global_vector.y,
                   y_axis.x * global_vector.x + y_axis.y * global_vector.y)
    
    def getLineIntersectRect(From,To,rect):
        """checks if a line is intersecting a rect
        returns true/false ; the scalar distance to interceptionpoint and the interceptionpoint in worldspace
        """
        intersection = False
        dist_to_closest = sys_maxsize
        point =None
        normal = None
        for C,D in [(Vector2(rect.topleft[0],rect.topleft[1]),Vector2(rect.bottomleft[0],rect.bottomleft[1])),
                    (Vector2(rect.bottomleft[0],rect.bottomleft[1]),Vector2(rect.bottomright[0],rect.bottomright[1])),
                    (Vector2(rect.bottomright[0],rect.bottomright[1]),Vector2(rect.topright[0],rect.topright[1])),
                    (Vector2(rect.topright[0],rect.topright[1]),Vector2(rect.topleft[0],rect.topleft[1]))]:
            intersection2, dist_to_current2, point2 = Vector.line_intersection_2d(From,To, C,D)
            if(intersection2==True and dist_to_closest>dist_to_current2):
                intersection=True
                dist_to_closest=dist_to_current2
                point=point2
                normal = (D-C).perp
        
        return intersection,dist_to_closest,point,normal


    def update(self, milliseconds):
        dist_to_closest = sys_maxsize
        closest_wall = None
        closest_point = None
        closest_normal = None
        steering_force = Vector2(0.0, 0.0)

        for obstacle in GameState().obstacles:  #todo only check obstacles in feelerrange
            for feeler_local in self.mob.sensorObstacle.feelers:
                feeler = BehaviourSteering.point_to_world_2d(feeler_local, self.mob.direction, self.mob.direction.perp, self.mob.position)
                intersection, dist_to_current, point, normal = BehaviourSteering.getLineIntersectRect(self.mob.position,feeler,obstacle.rect)           
                if intersection:
                    if dist_to_current < dist_to_closest:
                        dist_to_closest = dist_to_current
                        closest_wall = obstacle
                        closest_point = point
                        closest_normal = normal.normalized

            if closest_wall:
                overshoot = feeler - closest_point
                # create force away from wall
                steering_force += closest_normal * math.hypot(overshoot.x, overshoot.y)
                # makes a difference is last or first feeler wins?
                break

        self.steering_force= steering_force * self.mob.weight
