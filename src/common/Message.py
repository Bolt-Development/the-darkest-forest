import time

class Message(object):
    def __init__(self, message_type, message='', reason=None):
        self.message_type = message_type
        self.message = message

        self.timestamp = time.time()
        self.reason = reason

    def __repr__(self):
        return ' '.join(['[Message:',
                         self.message_type or 'no_type',
                         self.message or 'no_message',
                         str(self.timestamp),
                         self.reason or 'no_reason',
                        ']'])


if __name__ == '__main__':
    print Message('update')
