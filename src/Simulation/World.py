from Simulation.PhysicalEnvironment.ServiceArea import ServiceArea
from Configuration.globals import CONFIG
from Simulation.PhysicalEnvironment.AreaType import AreaType
from Simulation.Events.EventHandler import EventHandler
from Simulation.Events.UserActivityEvent import UserActivityEvent
from Simulation.Events.LatencyEvent import LatencyEvent
from Simulation.BusinessEnvironment.Company import Company
import math
'''Objects that represents the entire simulation environment'''
class World(object):
    
    def __init__(self, eventHandler, serviceAreas : list[ServiceArea], companies) -> None:
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
        self.eventHandler.HandleCurrentEvents()
        
        
    def Terminate(self):
        for serviceArea in self.serviceAreas:
            serviceArea.Terminate()
        
                
        
            
    def draw(self, window):
        for serviceArea in self.serviceAreas:
            serviceArea.draw(window)
            
    def drawInfo(self, window):
        for serviceArea in self.serviceAreas:
            serviceArea.drawInfo(window)