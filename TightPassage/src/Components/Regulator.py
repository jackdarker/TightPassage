import random
import pygame


class Regulator(object):
    """Helper-class to distribute task that dont need to be executed on every cycle.
    F.e. a Mob doesnt need to check every frame if a target is in weapon range
    """

    def __init__(self, num_update_per_sec):
        """
        """
        self._next_update_time = pygame.time.get_ticks() + random.random() * 1000.0
        if num_update_per_sec > 0:
            self._update_period = 1000.0 / num_update_per_sec  # ms
        elif num_update_per_sec == 0.0:
            self._update_period = 0.0
        elif num_update_per_sec < 0.0:
            self._update_period = -1
        # print('Regulator init: next: {0}  period: {1}'.format(self._next_update_time, self._update_period))

    def is_ready(self):
        """
        //returns true if the current time exceeds m_dwNextUpdateTime
        """
        # //if a regulator is instantiated with a zero freq then it goes into
        # //stealth mode (doesn't regulate)
        if self._update_period == 0.0:
            return True

        # //if the regulator is instantiated with a negative freq then it will
        # //never allow the code to flow
        if self._update_period < 0.0:
            return False

        current_time = pygame.time.get_ticks()  # / 1000.0

        # //the number of milliseconds the update period can vary per required
        # //update-step. This is here to make sure any multiple clients of this class
        # //have their updates spread evenly
        update_period_variator = 10.0

        if current_time >= self._next_update_time:
            self._next_update_time = current_time + self._update_period + random.randint(-update_period_variator,
                                                                                         update_period_variator)
            # print('Regulator update: current: {0}  next: {1}  period: {2}'.format(current_time, self._next_update_time, self._update_period))
            return True

        return False

