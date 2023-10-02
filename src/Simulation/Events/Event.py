'''Abstract class defining events'''
class Event(object):
    
    def __init__(self, eventTime) -> None:
        self.t = eventTime
        self.generateFollowUpEvent = False
        
    def trigger(self):
        pass