from queue import PriorityQueue
'''Handles the events generated during the simulation'''
class EventHandler(object):
    
    def __init__(self) -> None:
        self.currentTime = 0
        self._eventQueue = PriorityQueue()
        
    def addEvent(self, time, event):
        if(time < self.currentTime):
            ValueError("Event time is in the past")
        self._eventQueue.put((time, event))
        
    def getNextEvent(self):
        return self._eventQueue.get()
    
    def setCurrentTime(self, time):
        self.currentTime = time