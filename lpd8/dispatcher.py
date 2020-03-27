from lpd8.subscriber import Subscriber

class Dispatcher:
    """
    Class used to store subscribers to LPD8 events. A subscriber may be added or suppressed from the dispatcher array
    When a specific event arrives, the notify method is used to retrieve all subscribers to this event and send them
    a notification and associated data
    """
    def __init__(self):
        self._subscribers = []

    def subscribe(self, callback_object, callback_method, program, event_type, object_id):
        """
        Method used to subscribe to a particular event
        :param callback_object: An object holding the callback method
        :param callback_method: The callback method itself
        :param program: The program as defined in Program class
        :param event_type: The event type (NOTE_ON, NOTE_OFF, CTRL or PGM_CHG)
        :param object_id: The knob, pad or program change ID
        """
        self._subscribers.append(Subscriber(callback_object, callback_method, program, event_type, object_id))

    def unsubscribe(self, program, event_type, object_id):
        """
        Method used to unsubscribe to a particular event
        :param program: The program as defined in Program class
        :param event_type: The event type (NOTE_ON, NOTE_OFF, CTRL or PGM_CHG)
        :param object_id: The knob, pad or program change ID
        """
        for subscriber in self._subscribers:
            if subscriber.match(program, event_type, object_id):
                self._subscribers.remove(subscriber)
                break

    def notify(self, program, event_type, object_id, data=None):
        """
        Method used to trigger a notification to a specific event if a subscriber exists for this event
        :param program: The program as defined in Program class
        :param event_type: The event type (NOTE_ON, NOTE_OFF, CTRL or PGM_CHG)
        :param object_id: The knob, pad or program change ID
        :param data: The data to be sent to the subscriber
        """
        for subscriber in self._subscribers:
            if subscriber.match(program, event_type, object_id):
                subscriber.notify(program, object_id, data)
