from LimitedHandler import *
from Guard import *

class PubSub(object):
    def __init__(self):
        self.handlers = {}

    def emit(self, message_type, **kwargs):
        if message_type in self.handlers:
            handlers = self.handlers[message_type]
            
            reason = guarded(lambda: kwargs['reason']) or 'none'
            message = guarded(lambda: kwargs['message']) or 'none'

            event = Message(message_type, message, reason)

            for handler in handlers:
                handler.handle(event, **kwargs)
        


if __name__ == '__main__':
    pb = PubSub()

    pb.emit('hello_world', message = 'hello, world', reason = 'debugging')
