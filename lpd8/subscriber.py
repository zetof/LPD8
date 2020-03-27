class Subscriber:
    """
    Class that defines a subscriber to a specific event
    """

    def __init__(self, callback_class, callback_method, program, event_type, object_id):
        self._callback_class = callback_class
        self._callback_method = callback_method
        self._program = program
        self._event_type = event_type
        self._object_id = object_id

    def match(self, program, event_type, object_id):
        """
        Looks for a subscriber to a specific event
        :param program: The program as defined in Program class
        :param event_type: The event type (NOTE_ON, NOTE_OFF, CTRL or PGM_CHG)
        :param object_id: The knob, pad or program change ID
        """
        match = False
        if self._program == program and self._event_type == event_type and self._object_id == object_id:
            match = True
        return match

    def notify(self, program, object_id, data):
        """
        Call the subscriber (subscribed method of an object) and send available data if any
        :param program: The program as defined in Program class
        :param object_id: The knob, pad or program change ID
        :param data: The data to send to the subscriber for processing if any
        """
        if data == None:
            self._callback_method.__func__(self._callback_class, [program, object_id])
        else:
            self._callback_method.__func__(self._callback_class, [program, object_id, data])
