# -*- coding: utf-8 -*-

"""from dr0id_book_programing_game_ai_by_example
baseclasses for goal oriented action planning
"""

import logging
from abc import ABCMeta, ABC

logger = logging.getLogger(__name__)

class CannotAddGoalsToAtomicGoalsException(Exception):
    pass


class Goal(object):
    Active = 0
    Inactive = 1
    Completed = 2
    Failed = 3

    state_to_string = {Active: "Active", Inactive: "Inactive", Completed: "Completed", Failed: "Failed"}

    def __init__(self, owner, goal_type):
        self._owner = owner
        self.goal_type = goal_type
        self._status = Goal.Inactive

    def activate(self):
        """logic to run when the goal is activated."""
        raise NotImplementedError()

    def process(self):
        """logic to run each update-step"""
        raise NotImplementedError()

    def terminate(self):
        """logic to run when the goal is satisfied. (typically used to switch off any active steering behaviors)"""
        raise NotImplementedError()

    def handle_message(self, msg):
        """
        goals can handle messages. Many don't though, so this defines a default
        behavior
        :return:
        """
        return False

    def add_sub_goal(self, goal):
        """
        a Goal is atomic and cannot aggregate subgoals yet we must implement
        this method to provide the uniform interface required for the goal
        hierarchy.
        """
        raise CannotAddGoalsToAtomicGoalsException()

    @property
    def is_completed(self):
        return self._status == Goal.Completed

    @property
    def is_active(self):
        return self._status == Goal.Active

    @property
    def is_inactive(self):
        return self._status == Goal.Inactive

    @property
    def has_failed(self):
        return self._status == Goal.Failed

    def reactivate_if_failed(self):
        """if m_iStatus is failed this method sets it to inactive so that the goal
            will be reactivated (replanned) on the next update-step."""
        if self.has_failed:
            self._status = Goal.Inactive
            logger.info("%s status %s", self.__class__.__name__, Goal.Inactive)

    def activate_if_inactive(self):
        if self.is_inactive:
            self.activate()


class CompositeGoal(Goal, ABC):
    __metaclass__ = ABCMeta

    def __init__(self, owner, goal_type):
        Goal.__init__(self, owner, goal_type)
        self._sub_goals = []

    def handle_message(self, msg):
        """
        if a child class of Goal_Composite does not define a message handler
        the default behavior is to forward the message to the front-most
        subgoal
        """
        return self.forward_to_front_most_sub_goal(msg)

    def remove_all_sub_goals(self):
        logger.debug("remove all sub-goals of %s", self.__class__.__name__)
        for _g in self._sub_goals:
            _g.terminate()

        self._sub_goals[:] = []
        logger.debug("sub-goals cleared of %s", self.__class__.__name__)

    def process_sub_goals(self):
        """
        this method first removes any completed goals from the front of the
        subgoal list. It then processes the next goal in the list (if there is one)
        """
        #   //remove all completed and failed goals from the front of the sub-goal list
        while self._sub_goals and (self._sub_goals[0].is_completed or self._sub_goals[0].has_failed):
            _g = self._sub_goals.pop(0)
            _g.terminate()
            logger.debug("%s: terminate sub goal %s (%s)", self.__class__.__name__, _g.__class__.__name__, id(_g))

        #   //if any sub-goals remain, process the one at the front of the list
        if self._sub_goals:
            status_of_subgoal = self._sub_goals[0].process()

            #     //we have to test for the special case where the front-most sub-goal
            #     //reports 'completed' *and* the sub-goal list contains additional goals.When
            #     //this is the case, to ensure the parent keeps processing its sub-goal list
            #     //we must return the 'active' status.
            if status_of_subgoal == Goal.Completed and len(self._sub_goals) > 1:
                logger.debug("%s: first sub goal completed but there are more.", self.__class__.__name__)
                return Goal.Active
            return status_of_subgoal
        else:
            return Goal.Completed

    def add_sub_goal(self, new_goal):
        #   add the new goal to the front of the list
        logger.info("add_sub_goal %s (%s)", new_goal.__class__.__name__, id(new_goal))
        self._sub_goals.insert(0, new_goal)

    def forward_to_front_most_sub_goal(self, msg):
        if self._sub_goals:
            return self._sub_goals[0].handle_message(msg)

        # return false if the message has not been handled
        return False

    def terminate(self):
        logger.debug("%s (%s) terminate", self.__class__.__name__, id(self))
        for _g in self._sub_goals:
            _g.terminate()
            logger.debug("terminate sub-goal %s (%s) because parent %s (%s) is terminated", _g.__class__.__name__, id(_g), self.__class__.__name__, id(self))

