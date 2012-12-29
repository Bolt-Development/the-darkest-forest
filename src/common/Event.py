import time

class Event(object):
    def __init__(self, message_type, message='', reason=None):
        self.message_type = message_type
        self.message = message

        self.timestamp = time.time()
        self.reason = reason


if __name__ == '__main__':
    pass
