from PubSub import *
from Event import *

class Handler(PubSub):
    def __init__(self, message_type, callback):
        PubSub.__init__(self)

        self.message_type = message_type
        
        self.callback = callback
        self.call_count = 0

    def handle(self, event, **kwargs):
        if self.message_type == event.message_type:
            self.callback(self.event, **kwargs)
            self.call_count = self.call_count + 1

            self.emit(Event('callback'))

if __name__ == '__main__':
    pass
