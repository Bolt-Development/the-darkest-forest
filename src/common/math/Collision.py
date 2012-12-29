from .. import PubSub

class Collision(PubSub.PubSub):
    def __init__(self):
        PubSub.PubSub.__init__(self)
        print 'collision class created instance-of'
