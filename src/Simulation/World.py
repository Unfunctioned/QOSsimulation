from Simulation.PhysicalEnvironment.ServiceArea import ServiceArea
from Configuration.globals import GetConfig
from Simulation.Events.EventHandler import EventHandler
from Simulation.Events.Event import Event
from Simulation.Events.EventFactory import GetEventFactory
from DataOutput.TimeDataRecorder import TimeDataRecorder
from pygame import Surface
from pygame.font import Font
from Simulation.Events.BusinessEvents.BusinessEvent import BusinessEvent
from Simulation.BusinessEnvironment.Company import Company

'''Objects that represents the entire simulation environment'''
class World(object):
    
    def __init__(self, eventHandler : EventHandler, serviceAreas : list[ServiceArea], companies : list[Company],
        activityHistory : TimeDataRecorder) -> None:
        self.delayConfig = GetConfig().eventConfig.activityEventDelayRange
        self.eventHandler = eventHandler
        self.serviceAreas = serviceAreas
        self.companies = companies
        self.activeProcesses = set()
        self.activityHistory = activityHistory
        self.totalTime = -1
        
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
        eventsOnTimeStep = 0
        while getNext:
            entry = self.eventHandler.getNextEvent()
            event : Event
            event = entry.item
            event.trigger()
            isBusinessEvent = isinstance(event, BusinessEvent)
            hasBusinessEvents = self.eventHandler.hasBusinessActivityEvent()
            if(event.generateFollowUpEvent and (hasBusinessEvents or isBusinessEvent)):
                followUpEvent = GetEventFactory().generateFollowUp(event)
                self.eventHandler.addEvent(followUpEvent.t, followUpEvent)
            if(self.eventHandler.isEmpty() or self.eventHandler.currentTime < (self.eventHandler.Peek()).priority):
                getNext = False
            eventsOnTimeStep += 1
            if eventsOnTimeStep % 1000 == 999:
                print("Processed {count} events on timestep: {time}".format(count = eventsOnTimeStep+1, time = self.eventHandler.currentTime))
        
        
    def Terminate(self):
        self.totalTime = self.eventHandler.currentTime
        for serviceArea in self.serviceAreas:
            serviceArea.Terminate()
        self.activityHistory.terminate()
        
                
    def GetSimulationTime(self) -> int:
        if self.totalTime < 0:
            raise ValueError("Total time not set")
        return self.totalTime
            
    def draw(self, surface : Surface, font : Font):
        for serviceArea in self.serviceAreas:
            serviceArea.draw(surface, font)
            
    def drawInfo(self, surface : Surface, font : Font):
        for serviceArea in self.serviceAreas:
            serviceArea.drawInfo(surface, font)
            
    def printInfo(self):
        areaSize = 0.0
        totalUsers = 0
        for serviceArea in self.serviceAreas:
            areaSize += serviceArea.areaSize
            totalUsers += serviceArea.totalUsers
        print("Size: {size} km^2".format(size = areaSize))
        print("Users: {users}".format(users = totalUsers + len(self.companies)))
        print("Total Time: {time}".format(time = self.totalTime))