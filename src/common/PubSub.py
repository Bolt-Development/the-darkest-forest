from Message import *
from Guard import *

class PubSub(object):
    def __init__(self):
        self.handlers = {}

    def emit(self, message_type, **kwargs):
        if message_type in self.handlers:
            handlers = self.handlers[message_type]
            to_remove = []
            
            reason = guarded(lambda: kwargs['reason']) or 'none'
            message = guarded(lambda: kwargs['message']) or 'none'

            event = Message(message_type, message, reason)

            for handler in handlers:
                handler.handle(event, **kwargs)
                if guarded(lambda:handler.finished):
                    handlers.remove(handler)

            for finished in to_remove:
                handlers.remove(finished)

    def on(self, message_type, callback, repeats='infinite'):
        handler = LimitedHandler(message_type, callback, repeats)
        
        if not message_type in self.handlers:
            self.handlers[message_type] = []

        self.handlers[message_type].append(handler)

    def once(self, message_type, callback):
        self.on(message_type, callback, 0)

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
    pb = PubSub()

    def on_hello_world(event, **kwargs):
        print 'hello, world: from', guarded(lambda:kwargs['emitter']) or 'no one'

    pb.on('hello_world', on_hello_world, repeats=12)


    for x in xrange(20):
        pb.emit('hello_world',
                message = 'hello, world',
                reason = 'debugging',
                emitter = pb)
        print pb.handlers
