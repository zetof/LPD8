from lpd8.subscriber import Subscriber

class Dispatcher:

    def __init__(self):
        self._subscribers = []

    def subscribe(self, callback_class, callback_method, program, event_type, object_id):
        self._subscribers.append(Subscriber(callback_class, callback_method, program, event_type, object_id))

    def unsubscribe(self, program, event_type, object_id):
        for subscriber in self._subscribers:
            if subscriber.match(program, event_type, object_id):
                self._subscribers.remove(subscriber)
                break

    def notify(self, program, event_type, object_id, data=None):
        for subscriber in self._subscribers:
            if subscriber.match(program, event_type, object_id):
                subscriber.notify(program, object_id, data)
