from queue import PriorityQueue
from dataclasses import dataclass, field
from typing import Any
from Simulation.Events.UserActivityEvent import UserActivityEvent
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
        self._eventQueue = PriorityQueue()
        
    def addEvent(self, time : int, event):
        if(time < self.currentTime):
            ValueError("Event time is in the past")
        self._eventQueue.put(PrioritizedItem(time, event))
        
    def getNextEvent(self):
        return self._eventQueue.get()
    
    def getEventCount(self):
        return self._eventQueue._qsize()
    
    def setCurrentTime(self, time):
        self.currentTime = time
        
    def isEmpty(self):
        try:
            entry = self._eventQueue.queue[0]
            return False
        except:
            return True
    
    def Peek(self):
        try:
            entry = self._eventQueue.queue[0]
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
        
    def HandleCurrentEvents(self):
        getNext = True
        while(getNext):
            entry = self.getNextEvent()
            event = entry.item
            event.trigger()
            if(event.generateFollowUp and self.currentTime < CONFIG.simConfig.MAX_TIME):
                followUpEvent = UserActivityEvent.generateEvent(self.currentTime, event.area)
                self.addEvent(followUpEvent.t, followUpEvent)
            if(self.isEmpty() or self.currentTime < (self.Peek()).priority):
                getNext = False
            
        print(self.currentTime)