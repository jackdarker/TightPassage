# -*- coding: utf-8 -*-
from __future__ import print_function, division

import logging

from src.Interactable import Interactable

logger = logging.getLogger(__name__)

"""from dr0id_book_programing_game_ai_by_example
baseclasses that triggers messages
"""

class TriggerRegion(object):
    def is_touching(self, entity_pos, entity_radius):
        raise NotImplementedError()


class TriggerRegionRectangle(TriggerRegion):

    def __init__(self, topleft, bottomright):
        self._trigger = Pygame.Rect(topleft, bottomright)       #todo fixme

    #  there's no need to do an accurate (and expensive) circle v
    #  rectangle intersection test. Instead we'll just test the bounding box of
    #  the given circle with the rectangle.
    def is_touching(self, entity_pos, entity_radius):
        half = Vector2(entity_radius, entity_radius)
        entity_box = Pygame.Rect(entity_pos - half, entity_pos + half)       #todo fixme
        return self._trigger.colliderect(entity_box)


class TriggerRegionCircle(TriggerRegion):

    def __init__(self, pos, radius):
        self._pos = pos
        self._radius = radius

    def is_touching(self, entity_pos, entity_radius):
        return self._pos.get_distance_sq(entity_pos) < (entity_radius + self._radius) ** 2


class Trigger(Interactable):

    def __init__(self, rect,direction,new_id):
        Interactable.__init__(self, rect,direction,new_id)
        #  Every trigger owns a trigger region. If an entity comes within this 
        #  region the trigger is activated
        self._region_of_influence = None
        #  if this is true the trigger will be removed from the game
        self.is_to_be_removed = False
        #  it's convenient to be able to deactivate certain types of triggers
        #  on an event. Therefore a trigger can only be triggered when this
        #  value is true (respawning triggers make good use of this facility)
        self.active = True  # fixme: rename to is_active?
        #  some types of trigger are twinned with a graph node. This enables
        #  the path finding component of an AI to search a navgraph for a specific
        #  type of trigger.
        self.graph_node_index = -1

    #   //when this is called the trigger determines if the entity is within the
    #   //trigger's region of influence. If it is then the trigger will be
    #   //triggered and the appropriate action will be taken.
    def try_entity(self, entity):
        raise NotImplementedError()

    #
    #   //called each update-step of the game. This methods updates any internal
    #   //state the trigger may have
    def update(self):
        raise NotImplementedError()

    def is_touching_trigger(self, entity_pos, entity_radius):
        if self._region_of_influence:
            return self._region_of_influence.is_touching(entity_pos, entity_radius)
        return False

    def add_rectangular_trigger_region(self, topleft, bottomright):
        self._region_of_influence = TriggerRegionRectangle(topleft, bottomright)

    def add_circular_trigger_region(self, center, radius):
        self._region_of_influence = TriggerRegionCircle(center, radius)


class TriggerLimitedLifetime(Trigger):
    """
    defines a trigger that only remains in the game for a specified number of update steps
    """

    def __init__(self, life_time, rect,direction):
        Trigger.__init__(self, rect,direction, Interactable.get_next_valid_id())
        self._life_time = life_time
        logger.debug("trigger %s created with life time %s", self.ID, life_time)

    def update(self):
        self._life_time -= 1
        if self._life_time <= 0:
            self.is_to_be_removed = True
            logging.debug("trigger %s set to be removed from game: end of lief time", self.ID)

    def try_entity(self, entity):
        raise NotImplementedError


class TriggerRespawning(Trigger):
    """
    When a bot comes within this trigger's area of influence it is triggered
    but then becomes inactive for a specified amount of time. These values
    control the amount of time required to pass before the trigger becomes
    active once more.
    """

    def __init__(self, rect,direction, trigger_id):
        Trigger.__init__(self, rect,direction, trigger_id)
        self._num_updates_between_respawns = 0
        self._num_update_remaining_until_respawn = 0

    def deactivate(self):
        self.active = False
        self._num_update_remaining_until_respawn = self._num_updates_between_respawns
        logger.debug("trigger %s deactivated", self.ID)

    def update(self):
        self._num_update_remaining_until_respawn -= 1
        if self._num_update_remaining_until_respawn <= 0 and not self.active:
            logger.debug("trigger %s activated", self.ID)
            self.active = True

    def set_respawn_delay(self, num_ticks):
        self._num_updates_between_respawns = num_ticks

    def try_entity(self, entity):
        raise NotImplementedError()


class TriggerSystem(object):
    """
    Class to manage a collection of triggers. Triggers may be
    registered with an instance of this class. The instance then
    takes care of updating those triggers and of removing them from
    the system if their lifetime has expired.

    """

    def __init__(self):
        self.triggers = []

    def clear(self):
        self.triggers = []

    def _update_triggers(self):
        """
        this method iterates through all the triggers present in the system and
        calls their Update method in order that their internal state can be
        updated if necessary. It also removes any triggers from the system that
        have their m_bRemoveFromGame field set to true.
        """
        # keep only th ones not market to be removed
        self.triggers = [_t for _t in self.triggers if not _t.is_to_be_removed]

        # update the triggers
        for trig in self.triggers:
            trig.update()

    def _try_entities(self, entities):
        """
        this method iterates through the container of entities passed as a
        parameter and passes each one to the Try method of each trigger *provided*
        the entity is alive and provided the entity is ready for a trigger update.

        :param entities:
        :return:
        """
        #  test each entity against the triggers
        for ent in entities:
            #  alive before it is tested against each trigger.
            if ent.is_read_for_trigger_update and ent.is_alive:
                for trig in self.triggers:
                    trig.try_entity(ent)

    def update(self, entities):
        """
        This method should be called each update-step of the game. It will first
        update the internal state odf the triggers and then try each entity against
        each active trigger to test if any should be triggered.

        :param entities:
        :return:
        """
        self._update_triggers()
        self._try_entities(entities)

    def register(self, trigger):
        """
        this is used to register triggers with the TriggerSystem (the TriggerSystem
        will take care of tidying up memory used by a trigger)

        :param trigger:
        :return:
        """
        self.triggers.append(trigger)

