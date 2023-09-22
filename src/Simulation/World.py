from Simulation.PhysicalEnvironment.ServiceArea import ServiceArea
from Configuration.globals import CONFIG
from Simulation.PhysicalEnvironment.AreaType import AreaType
from Simulation.Events.EventHandler import EventHandler
from Simulation.Events.UserActivityEvent import UserActivityEvent
import math
'''Objects that represents the entire simulation environment'''
class World(object):
    
    def __init__(self) -> None:
        self.delayConfig = CONFIG.eventConfig.activityDelayRange
        self.eventHandler = EventHandler()
        self.serviceArea = []
        
    def isRunning(self):
        if (self.eventHandler.currentTime > 0 and self.eventHandler.isEmpty()):
            print("Terminating")
            return False
        return True
        
    def generateServiceAreas(self, cells):
        areaDefinitions = self.designateAreaTypes(cells)
        index = 0
        for (type, cell) in areaDefinitions:
            serviceArea = ServiceArea(index, cell, type)
            self.serviceArea.append(serviceArea)
            self.generateActivityUpdateEvent(serviceArea)
            index += 1
        print("Events in Queue: {count}".format(count = self.eventHandler.getEventCount()))
            
    def designateAreaTypes(self, cells):
        areaDefinitions = []
        areasByWeight = sorted(cells, key=lambda cell: cell.weight)
        areaCount = len(areasByWeight)
        amountRural = max(1, math.floor(areaCount * CONFIG.simConfig.SHARE_RURAL))
        amountDense = max(1, math.floor(areaCount * CONFIG.simConfig.SHARE_DENSE))
        for i in range(areaCount):
            area = areasByWeight[i]
            if i < amountRural:
                areaDefinitions.append((AreaType.RURAL, area))
            elif i >= areaCount - amountDense - 1:
                areaDefinitions.append((AreaType.DENSE_URBAN, area))
            else:
                areaDefinitions.append((AreaType.URBAN, area))
        return areaDefinitions
    
    def generateActivityUpdateEvent(self, serviceArea):
        event = UserActivityEvent.generateEvent(self.eventHandler.currentTime, serviceArea)
        self.eventHandler.addEvent(event.t, event)
    
    def printInfo(self):
        totalArea = 0.0
        for serviceArea in self.serviceArea:
            totalArea += serviceArea.cell.area
        print("Total area: {area}".format(area = totalArea))
        
    def Update(self):
        if(not self.eventHandler.advanceTime()):
            print("Advancing Time failed")
            return
        self.eventHandler.HandleCurrentEvents()
        
                
        
            
    def draw(self, window):
        for serviceArea in self.serviceArea:
            serviceArea.draw(window)
            
    def drawInfo(self, window):
        for serviceArea in self.serviceArea:
            serviceArea.drawInfo(window)