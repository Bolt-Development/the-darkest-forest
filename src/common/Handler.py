from PubSub import *
from Message import *

class Handler(PubSub):
    def __init__(self, message_type, callback):
        PubSub.__init__(self)

        self.message_type = message_type
        
        self.callback = callback
        self.call_count = 0

    def handle(self, event, **kwargs):
        if self.message_type == event.message_type:
            self.callback(event, **kwargs)
            self.call_count = self.call_count + 1

            self.emit('callback')

if __name__ == '__main__':
    def say_hello(event, **kwargs):
        print 'hello, world', kwargs
        
    handler = Handler('say_hello', say_hello)
    handler.handle(Message('say_hello'), reason='unspecified', target='audience')
