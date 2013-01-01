from Message import *
from Guard import *

class PubSub(object):
    def __init__(self):
        self.handlers = {}
        self.conditions = {}
        self.memory = {}

    def emit(self, message_type, **kwargs):
        if message_type in self.handlers:
            handlers = self.handlers[message_type]
            to_remove = []

            event = self._parse_msg_from_kwargs(message_type, **kwargs)

            for handler in handlers:
                handler.handle(event, **kwargs)
                condition = self._handle_condition(handler, event, **kwargs)
                if not condition or guarded(lambda:handler.finished):
                    to_remove.append(handler)

            for finished in to_remove:
                handlers.remove(finished)

        # only remembers last arguments
        self.memory[message_type]=kwargs

    def on(
            self,
            message_type,
            callback,
            repeats='infinite',
            condition=False,
            memory=False,
            unique=True
        ):

        handler = LimitedHandler(message_type, callback, repeats)
        
        if not message_type in self.handlers:
            self.handlers[message_type] = []

        if self._add_handler(message_type, handler, memory, unique):
            if condition:
                self.conditions[handler] = condition

    def once(self, message_type, callback):
        self.on(message_type, callback, 0)

    def _parse_kwargs(self, **kwargs):
        return (guarded(lambda: kwargs['reason']) or 'none',
                guarded(lambda: kwargs['message']) or 'none')

    def _parse_msg_from_kwargs(self, msg, **kwargs):
        reason, message = self._parse_kwargs(**kwargs)
        return Message(msg, message, reason)
                               
    def _call_immediately(self, handler, message_type, memory=False):
        if memory and message_type in self.memory:
            kwargs = self.memory[message_type]
            event = self._parse_msg_from_kwargs(message_type, **kwargs)
            handler.handle(event, **kwargs)

    def _add_handler(self, message_type, handler, memory=False, unique=True):
        handlers = self.handlers[message_type]

        if unique and handler not in handlers:
            self._call_immediately(handler, message_type, memory)
            handlers.append(handler)
            return True
        else:
            return False

    def _handle_condition(self, handler, event, **args):
        condition = guarded(lambda:self.conditions[handler]) or False
        if condition:
            return condition(handler, event, **args)
        else:
            return True
    

class Handler(PubSub):
    def __init__(self, message_type, callback):
        PubSub.__init__(self)

        self.message_type = message_type
        
        self.callback = callback
        self.call_count = 0

    def handle(self, event, **kwargs):
        if self.message_type == event.message_type:
            try:
                self.callback(event, **kwargs)
            except TypeError:
                self.callback()
                
            self.call_count = self.call_count + 1

            self.emit('callback')

    def __eq__(self, other):
        return (isinstance(other, Handler) and
                self.message_type == other.message_type and
                self.callback == other.callback)

    def __repr__(self):
        return " ".join([self.message_type or 'no_type',
                         str(self.callback),
                         str(self.call_count)])

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

    def __repr__(self):
        return " ".join([Handler.__repr__(self),
                         str(self.repeats)])
                         


if __name__ == '__main__':
    pb = PubSub()

    def on_hello_world(event, **kwargs):
        print 'hello, world: from', guarded(lambda:kwargs['emitter']) or 'no one'

    def on_init(event, **kwargs):
        print 'This was called from memory, while', kwargs['message']

    pb.emit('init', message='this was called before any emits.')

    def stop_at_three(handler, event, **kwargs):
        return handler.call_count < 3
    
    pb.on('hello_world', on_hello_world, repeats=12, condition=stop_at_three)
    pb.on('hello_world', on_hello_world, repeats=12)


    for x in xrange(20):
        pb.emit('hello_world',
                message = 'hello, world',
                reason = 'debugging',
                emitter = pb)
        print pb.handlers

    pb.on('init', on_init, memory=True)
