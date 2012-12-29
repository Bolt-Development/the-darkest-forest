from PubSub import *

class Handler(PubSub):
    def __init__(self, message_type, fun):
        PubSub.__init__(self)

        self.message_type = message_type
        
        self.fun = fun
        self.call_count = 0

    def handle(self, event, **kwargs):
        if self.message_type == event.message_type:
            self.fun(self.event, **kwargs)
            self.call_count = self.call_count + 1

if __name__ == '__main__':
    pass
