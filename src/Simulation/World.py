from Simulation.PhysicalEnvironment.ServiceArea import ServiceArea
from Configuration.globals import CONFIG
from Simulation.Events.EventHandler import EventHandler
from Simulation.Events.Event import Event
from Simulation.Events.EventFactory import EventFactory
'''Objects that represents the entire simulation environment'''
class World(object):
    
    def __init__(self, eventHandler : EventHandler, serviceAreas : list[ServiceArea], companies) -> None:
        self.delayConfig = CONFIG.eventConfig.activityEventDelayRange
        self.eventHandler = eventHandler
        self.serviceAreas = serviceAreas
        self.companies = companies
        self.activeProcesses = set()
        
    def isRunning(self):
        if (self.eventHandler.currentTime > 0 and self.eventHandler.isEmpty()):
            print("Terminating")
            return False
        return True
    
    def printInfo(self):
        totalArea = 0.0
        for serviceArea in self.serviceAreas:
            totalArea += serviceArea.cell.area
        print("Total area: {area}".format(area = totalArea))
        
    def Update(self):
        if(not self.eventHandler.advanceTime()):
            print("Advancing Time failed")
            return
        print(self.eventHandler.currentTime)
        getNext = True
        while getNext:
            entry = self.eventHandler.getNextEvent()
            event : Event
            event = entry.item
            event.trigger()
            if(event.generateFollowUpEvent and self.eventHandler.currentTime < CONFIG.simConfig.MAX_TIME):
                followUpEvent = EventFactory.generateFollowUp(event)
                self.eventHandler.addEvent(followUpEvent.t, followUpEvent)
            if(self.eventHandler.isEmpty() or self.eventHandler.currentTime < (self.eventHandler.Peek()).priority):
                getNext = False
        
        
    def Terminate(self):
        for serviceArea in self.serviceAreas:
            serviceArea.Terminate()
        
                
        
            
    def draw(self, window):
        for serviceArea in self.serviceAreas:
            serviceArea.draw(window)
            
    def drawInfo(self, window):
        for serviceArea in self.serviceAreas:
            serviceArea.drawInfo(window)