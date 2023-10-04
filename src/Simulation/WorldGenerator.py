from Utilities.RandomPointSpawner import *
from Utilities.SiteSpawner import *
from Utilities.VoronoiDiagram.Voronoi import *
from Configuration.globals import *
from Simulation.World import World
import math
from Simulation.PhysicalEnvironment.ServiceArea import ServiceArea
from Simulation.Events.EventHandler import EventHandler
from Simulation.Events.UserActivityEvent import UserActivityEvent
from Simulation.Events.LatencyEvent import LatencyEvent
from Simulation.BusinessEnvironment.Company import Company
from Simulation.Events.BusinessProcessActivationEvent import BusinessProcessActivationEvent

'''Responsible for generating the simulation environment'''
class WorldGenerator(object):
    
    def __init__(self) -> None:
        self.pointSpawner = RandomPointSpawner()
        self.siteSpawner = SiteSpawner()
        self.voronoi = Voronoi(self.siteSpawner.SpawnPoints())
        points = self.pointSpawner.SpawnPoints(CONFIG.simConfig.WEIGHTS)
        self.matchPointsToCell(points)
        self.eventHandler = EventHandler()
        self.serviceAreas = self.generateServiceAreas()
        self.world = World(self.eventHandler,
                           self.serviceAreas,
                           self.generateCompanies())
        self.world.printInfo()
        
    def generateServiceAreas(self):
        serviceAreas = []
        areaDefinitions = self.designateAreaTypes()
        areaDefinitions.sort(key= lambda item : item[1].weight)
        index = 0
        for (type, cell) in areaDefinitions:
            serviceArea = ServiceArea(index, cell, type)
            serviceArea.InitializeNetwork(0)
            serviceAreas.append(serviceArea)
            self.generateActivityUpdateEvent(serviceArea)
            self.generateLatencyUpdateEvent(serviceArea)
            index += 1
        print("Events in Queue: {count}".format(count = self.eventHandler.getEventCount()))
        return serviceAreas
        
    def generateCompanies(self):
        companies = []
        for i in range(CONFIG.simConfig.COMPANIES):
            serviceArea = CONFIG.randoms.companyLocationGeneration.choice(self.serviceAreas)
            company = Company(i, serviceArea)
            delayRange = CONFIG.eventConfig.businessProcessActivationDelayRange
            eventTime = CONFIG.randoms.businessProcessActivationSimulation.randint(delayRange[0], delayRange[1])
            activationEvent = BusinessProcessActivationEvent(eventTime, company)
            companies.append(company)
            self.eventHandler.addEvent(activationEvent.t, activationEvent)
        return companies
        
    def designateAreaTypes(self):
        cells = self.voronoi.cells
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
        
    def generateLatencyUpdateEvent(self, serviceArea):
        event = LatencyEvent.generateEvent(self.eventHandler.currentTime, serviceArea)
        self.eventHandler.addEvent(event.t, event)
        
        
    def matchPointsToCell(self, points):
        for point in points:
            print(point.position)
            for cell in self.voronoi.cells:
                if(cell.isPointinCell(point.position)):
                    point.color = Colors.GetColor(cell.colorcode)
                    cell.weight += 1
                    break
                
    def get_world(self):
        return self.world
                    
    def draw(self, window):
        self.world.draw(window)
        #self.world.drawInfo(window)
        #self.voronoi.drawEdges(window)
        