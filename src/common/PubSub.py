from LimitedHandler import *
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
                guarded(lambda:handler.finished, lambda x:to_remove.append(x))

            for finished in to_remove:
                self.handlers.remove(finished)

    def on(self, message_type, callback, repeats='infinite'):
        handler = LimitedHandler(message_type, callback, repeats)
        
        if not message_type in self.handlers:
            self.handlers[message_type] = []

        self.handlers[message_type].append(handler)

    def once(self, message_type, callback):
        self.on(message_type, callback, 0)


if __name__ == '__main__':
    pb = PubSub()

    def on_hello_world(event, **kwargs):
        print 'hello, world: from', guarded(lambda:kwargs['emitter']) or 'no one'

    pb.on('hello_world', on_hello_world)


    pb.emit('hello_world',
            message = 'hello, world',
            reason = 'debugging',
            emitter = pb)
