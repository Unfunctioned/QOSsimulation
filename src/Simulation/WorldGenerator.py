from Utilities.RandomPointSpawner import RandomPointSpawner
from Utilities.VoronoiDiagram.Voronoi import Voronoi
from UI.Colors import Colors
from Simulation.PhysicalEnvironment.AreaType import AreaType
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
from UI.UIPoint import UIPoint
from DataOutput.TimeDataRecorder import TimeDataRecorder
from pygame import Surface
from pygame.font import Font
from Utilities.PathGenerator import SetPathGenerator, PathGenerator
from memory_profiler import profile

from Simulation.BusinessEnvironment.BusinessProcessFactory import BuisnessProcessFactory
from Simulation.BusinessEnvironment.BusinessProcessFactory import SetBusinessProcessFactory
from Simulation.BusinessEnvironment.BusinessProcessFactory import GetBusinessProcessFactory
'''Responsible for generating the simulation environment'''
class WorldGenerator(object):
    
    def __init__(self, showOutput = False) -> None:
        self.showOutput = showOutput
        self.eventHandler = EventHandler()
        voronoi = Voronoi()
        self.matchPointsToCell(voronoi.getCells())
        self.activityHistory = TimeDataRecorder(-1, ["PROCESS_ID", "STATUS", "ACTIVITY_TYPE", "QOS_AVAILABILITY",
                                                        "FAILURE_CAUSE", "CAPACITY_VIOLATION_TIME", "LATENCY_VIOLATION_TIME"])
        self.activityHistory.createFileOutput(GetConfig().filePaths.simulationPath, "WorldActivity")
        self.serviceAreas = self.generateServiceAreas(voronoi.getCells())
        generator = PathGenerator(self.serviceAreas)
        SetPathGenerator(generator)
        SetBusinessProcessFactory(BuisnessProcessFactory(generator))
        EventFactory.InitializeOutput()
        EventFactory.InitializeSpikeTimes(self.serviceAreas)
        self.world = World(self.eventHandler,
                           self.serviceAreas,
                           self.generateCompanies(),
                           self.activityHistory)
        if self.showOutput:
            self.world.printInfo()
    
    def generateServiceAreas(self, cells):
        serviceAreas = []
        areaDefinitions = self.designateAreaTypes(cells)
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
            businessProcessFlow = GetBusinessProcessFactory().SelectBusinessProcessFlow()
            company = Company(i, serviceArea, businessProcessFlow, self.activityHistory)
            delayRange = GetConfig().eventConfig.businessProcessActivationDelayRange
            eventTime = GetConfig().randoms.businessProcessActivationSimulation.randint(delayRange[0], delayRange[1])
            activationEvent = EventFactory.generateBusinessProcessActivationEvent(eventTime, company)
            companies.append(company)
            self.eventHandler.addEvent(activationEvent.t, activationEvent)
        return companies
        
    def designateAreaTypes(self, cells) -> list[Cell]:
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
        
        
    def matchPointsToCell(self, cells):
        points = RandomPointSpawner.SpawnPoints(GetConfig().simConfig.WEIGHTS)
        point : UIPoint
        for point in points:
            if self.showOutput:
                print(point.position)
            cell : Cell
            for cell in cells:
                if(cell.isPointinCell(point.position)):
                    point.color = Colors.GetColor(cell.colorcode)
                    cell.weight += 1
                    break
                
    def get_world(self):
        return self.world
                    
    def draw(self, surface : Surface, font : Font):
        self.world.draw(surface, font)
        