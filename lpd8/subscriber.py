class Subscriber:

    def __init__(self, callback_class, callback_method, program, event_type, object_id):
        self._callback_class = callback_class
        self._callback_method = callback_method
        self._program = program
        self._event_type = event_type
        self._object_id = object_id

    def match(self, program, event_type, object_id):
        match = False
        if self._program == program and self._event_type == event_type and self._object_id == object_id:
            match = True
        return match

    def notify(self, program, object_id, data):
        if data == None:
            self._callback_method.__func__(self._callback_class, [program, object_id])
        else:
            self._callback_method.__func__(self._callback_class, [program, object_id, data])
