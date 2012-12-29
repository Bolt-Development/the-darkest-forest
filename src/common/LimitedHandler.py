from Handler import *
from Message import *

class LimitedHandler(Handler):
    def __init__(self, message_type, callback, repeats='infinite'):
        Handler.__init__(self, message_type, callback)

        self.repeats = repeats

    def handle(self, event, **kwargs):
        if self.repeats is 'infinite' or self.call_count <= self.repeats:
            Handler.handle(self, event, **kwargs)
        else:
            self.emit('finished', emitter=self)
            self.finished = True
            
if __name__ == '__main__':
    def say_hello(event, **kwargs):
        print 'hello, world', kwargs
        
    handler = LimitedHandler('say_hello', say_hello, repeats=2)

    for x in xrange(0, 20):
        handler.handle(Message('say_hello'), reason='unspecified', target='audience')
