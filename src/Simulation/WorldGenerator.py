from Utilities.RandomPointSpawner import *
from Utilities.SiteSpawner import *
from Utilities.VoronoiDiagram.Voronoi import *
from Configuration.globals import GetConfig
from Simulation.World import World
from Utilities.VoronoiDiagram.Cell import Cell
import math
from Simulation.PhysicalEnvironment.ServiceArea import ServiceArea
from Simulation.Events.EventHandler import EventHandler
from Simulation.Events.UserActivityEvent import UserActivityEvent
from Simulation.Events.LatencyEvent import LatencyEvent
from Simulation.BusinessEnvironment.Company import Company
from Simulation.Events.EventFactory import EventFactory
from Simulation.BusinessEnvironment.BusinessActivity import *

from Simulation.BusinessEnvironment.BusinessProcessFactory import BuisnessProcessFactory
'''Responsible for generating the simulation environment'''
class WorldGenerator(object):
    
    def __init__(self, showOutput = False) -> None:
        self.showOutput = showOutput
        self.pointSpawner = RandomPointSpawner()
        self.siteSpawner = SiteSpawner()
        self.voronoi = Voronoi(self.siteSpawner.SpawnPoints())
        points = self.pointSpawner.SpawnPoints(GetConfig().simConfig.WEIGHTS)
        self.matchPointsToCell(points)
        self.eventHandler = EventHandler()
        self.activityHistory = TimeDataRecorder(-1, ["PROCESS_ID", "STATUS", "ACTIVITY_TYPE", "QOS_AVAILABILITY",
                                                        "FAILURE_CAUSE", "CAPACITY_VIOLATION_TIME", "LATENCY_VIOLATION_TIME"])
        self.activityHistory.createFileOutput(GetConfig().filePaths.simulationPath, "WorldActivity")
        self.serviceAreas = self.generateServiceAreas()
        BuisnessProcessFactory.SetBusinessProcessFlows()
        BuisnessProcessFactory.SetServiceAreas(self.serviceAreas)
        EventFactory.InitializeOutput()
        EventFactory.InitializeSpikeTimes(self.serviceAreas)
        self.world = World(self.eventHandler,
                           self.serviceAreas,
                           self.generateCompanies(),
                           self.activityHistory)
        if self.showOutput:
            self.world.printInfo()
        
    def generateServiceAreas(self):
        serviceAreas = []
        areaDefinitions = self.designateAreaTypes()
        areaDefinitions.sort(key= lambda item : item[1].weight)
        for i in range(len(areaDefinitions)):
            type, cell = areaDefinitions[i]
            serviceArea = ServiceArea(i, cell, type)
            serviceArea.InitializeNetwork(0)
            serviceAreas.append(serviceArea)
            self.generateActivityUpdateEvent(serviceArea)
            self.generateLatencyUpdateEvent(serviceArea)
        if self.showOutput:
            print("Events in Queue: {count}".format(count = self.eventHandler.getEventCount()))
        return serviceAreas
        
    def generateCompanies(self):
        companies = []
        for i in range(GetConfig().simConfig.COMPANIES):
            serviceArea = GetConfig().randoms.companyLocationGeneration.choice(self.serviceAreas)
            businessProcessFlow = BuisnessProcessFactory.SelectBusinessProcessFlow()
            company = Company(i, serviceArea, businessProcessFlow, self.activityHistory)
            delayRange = GetConfig().eventConfig.businessProcessActivationDelayRange
            eventTime = GetConfig().randoms.businessProcessActivationSimulation.randint(delayRange[0], delayRange[1])
            activationEvent = EventFactory.generateBusinessProcessActivationEvent(eventTime, company)
            companies.append(company)
            self.eventHandler.addEvent(activationEvent.t, activationEvent)
        return companies
        
    def designateAreaTypes(self) -> list[Cell]:
        cells = self.voronoi.cells
        areaDefinitions = []
        areasByWeight = sorted(cells, key=lambda cell: cell.weight)
        areaCount = len(areasByWeight)
        amountRural = max(1, math.floor(areaCount * GetConfig().simConfig.SHARE_RURAL))
        amountDense = max(1, math.floor(areaCount * GetConfig().simConfig.SHARE_DENSE))
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
            if self.showOutput:
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
        