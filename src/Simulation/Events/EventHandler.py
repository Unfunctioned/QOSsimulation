from queue import PriorityQueue
from dataclasses import dataclass, field
from typing import Any
from Configuration.globals import CONFIG

'''Class to wrap PriorityQueue entries'''
@dataclass(order=True)
class PrioritizedItem:
    priority: int
    item: Any=field(compare=False)
    
'''Handles the events generated during the simulation'''
class EventHandler(object):
    
    def __init__(self) -> None:
        self.currentTime = 0
        self._activityEventQueue = PriorityQueue()
        
    def addEvent(self, time : int, event):
        if(time < self.currentTime):
            raise ValueError("Event time is in the past")
        self._activityEventQueue.put(PrioritizedItem(time, event))
        
    def getNextEvent(self) -> PrioritizedItem:
        return self._activityEventQueue.get()
    
    def getEventCount(self):
        return self._activityEventQueue._qsize()
    
    def setCurrentTime(self, time):
        self.currentTime = time
        
    def isEmpty(self):
        try:
            _ = self._activityEventQueue.queue[0]
            return False
        except:
            return True
    
    def Peek(self) -> PrioritizedItem:
        try:
            entry = self._activityEventQueue.queue[0]
            return entry
        except:
            return None
        
    def advanceTime(self):
        if(self.isEmpty()):
            return False
        try:
            entry = self.Peek()
            self.setCurrentTime(entry.priority)
            return True
        except:
            return False