
import heapq
import time

from src.Components import entityregistry

"""from dr0id_book_programing_game_ai_by_example
classes to send messages from one object to others
"""

SEND_MSG_IMMEDIATELY = 0.0
SENDER_ID_IRRELEVANT = -1
NO_ADDITIONAL_INFO = None


class Telegram(object):

    def __init__(self, sender_id, receiver_id, msg, extra_info=NO_ADDITIONAL_INFO):
        self.sender_id = sender_id
        self.receiver_id = receiver_id
        self.message = msg  # this is actually the message type
        self.extra_info = extra_info


_delayed_messages = []
heapq.heapify(_delayed_messages)

#todo move to signelton class?
def dispatch_message(delay_seconds, sender_id, receiver_id, msg, extra_info=NO_ADDITIONAL_INFO):
    """
    Dispatch a message.
    
    :Parameters:
        delay_seconds : float
            Delay the message about that timespan. For immediate dispatching
            this value should be <= 0.0
        sender_id : ID
            The id of the sender.
        receiver_id : ID
            The id of the receiver.
        msg : messagetype
            The type of message.
        extra_info : object
            Defaults to None. Can be any extra infor to pass.
            
    """
    telegram = Telegram(sender_id, receiver_id, msg, extra_info)

    if delay_seconds <= 0.0:
        # no delay, route telegram immediatly
        # print("Instant telegram dispatched at time: %s by %s for %s. Msg is  %s" \
        # % (time.time(), sender_id, receiver_id, msg))
        _discharge(receiver_id, telegram)
    else:
        # put it in the queue and deliver later
        dispatch_time = time.time() + delay_seconds
        heapq.heappush(_delayed_messages, (dispatch_time, telegram))
        # print("Delayed telegram from %s" " recorded at time %s for %s . Msg is %s" \
        # % (sender_id, time.time(), receiver_id, msg))


def dispatch_delayed_messages():
    """
    Send out any delayed messages. This method is called each time through
    the main game loop.
    """
    now = time.time()
    while _delayed_messages and _delayed_messages[0][0] < now:
        not_used, telegram = heapq.heappop(_delayed_messages)
        # print("Dispatching delayed message")
        _discharge(telegram.receiver_id, telegram)


def _discharge(receiver_id, telegram):
    """
    Dispatches the telegram to the receiver by calling its handle_messgage
    method.
    
    :Parameters:
        receiver_id : ID
            The id of the receiver.
        telegram : :class:`Telegram`
            The telegram to deliver.
    
    """
    receiver = entityregistry.get_entity_from_ID(receiver_id)
    # print("message discharge, sender: {0} receiver: {1} msg: {2} extra: {3}".format(telegram.sender_id, telegram.receiver_id, telegram.message, telegram.extra_info))

    if not receiver.handle_message(telegram):
        # print("receiver %s did not handle telegram '%s'" \
        # % (receiver, telegram.message))
        pass

