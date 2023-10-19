from Simulation.PhysicalEnvironment.ServiceArea import ServiceArea
from Configuration.globals import GetConfig
from Simulation.Events.EventHandler import EventHandler
from Simulation.Events.Event import Event
from Simulation.Events.EventFactory import EventFactory
from DataOutput.TimeDataRecorder import TimeDataRecorder

'''Objects that represents the entire simulation environment'''
class World(object):
    
    def __init__(self, eventHandler : EventHandler, serviceAreas : list[ServiceArea], companies,
        activityHistory : TimeDataRecorder) -> None:
        self.delayConfig = GetConfig().eventConfig.activityEventDelayRange
        self.eventHandler = eventHandler
        self.serviceAreas = serviceAreas
        self.companies = companies
        self.activeProcesses = set()
        self.activityHistory = activityHistory
        self.totalTime = None
        
    def isRunning(self, showOutput = False):
        if (self.eventHandler.currentTime > 0 and self.eventHandler.isEmpty()):
            if showOutput:
                print("Terminating")
            return False
        return True
    
    def printInfo(self):
        totalArea = 0.0
        for serviceArea in self.serviceAreas:
            totalArea += serviceArea.cell.area
        print("Total area: {area}".format(area = totalArea))
        
    def Update(self, showOutput : bool):
        if(not self.eventHandler.advanceTime()):
            raise AttributeError("Advancing Time failed")
        if showOutput:
            print(self.eventHandler.currentTime)
        getNext = True
        while getNext:
            entry = self.eventHandler.getNextEvent()
            event : Event
            event = entry.item
            event.trigger()
            if(event.generateFollowUpEvent and self.eventHandler.hasBusinessActivityEvent()):
                followUpEvent = EventFactory.generateFollowUp(event)
                self.eventHandler.addEvent(followUpEvent.t, followUpEvent)
            if(self.eventHandler.isEmpty() or self.eventHandler.currentTime < (self.eventHandler.Peek()).priority):
                getNext = False
        
        
    def Terminate(self):
        self.totalTime = self.eventHandler.currentTime
        for serviceArea in self.serviceAreas:
            serviceArea.Terminate()
        self.activityHistory.terminate()
        
                
    def GetSimulationTime(self):
        return self.totalTime
            
    def draw(self, window):
        for serviceArea in self.serviceAreas:
            serviceArea.draw(window)
            
    def drawInfo(self, window):
        for serviceArea in self.serviceAreas:
            serviceArea.drawInfo(window)