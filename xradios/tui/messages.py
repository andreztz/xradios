class EventEmitter:
    def __init__(self):
        self.listeners = dict()

    def _add_listener(self, event, func):
        self.listeners.setdefault(event, set()).add(func)

    def on(self, event, func):
        self._add_listener(event, func)

    def remove_listener(self, event, func):
        if event in self.listeners and func in self.listeners[event]:
            self.listeners[event].remove(func)

    def remove_all_listeners(self, event):
        if event in self.listeners:
            del self.listeners[event]

    def emit(self, event, *args, **kwargs):
        if event in self.listeners:
            listener_copy = self.listeners[event]  # .copy()
            for func in listener_copy:
                return func(*args, **kwargs)


emitter = EventEmitter()
