from Simulation.PhysicalEnvironment.ServiceArea import ServiceArea
from Utilities.VoronoiDiagram.Cell import Cell
from queue import PriorityQueue
import math
from dataclasses import dataclass, field
from typing import Any
from Configuration.globals import GetConfig

'''Class to wrap PriorityQueue entries'''
@dataclass(order=True)
class PrioritizedItem:
    priority: float
    item: Any=field(compare=False)

'''Computes routes between service areas'''
class PathGenerator(object):
    
    def __init__(self, serviceAreas : list[ServiceArea]) -> None:
        self.serviceAreas = serviceAreas
        self.cellToServiceArea : dict[Cell, ServiceArea]
        self.cellToServiceArea = dict()
        for serviceArea in serviceAreas:
            self.cellToServiceArea[serviceArea.cell] = serviceArea
            
    
    def GenerateShortestPath(self, startLocation : ServiceArea, endLocation : ServiceArea) -> list[ServiceArea]:
        cellWeights = self.CalculateWeights(startLocation, endLocation)
        startingCell = startLocation.cell
        endingCell = endLocation.cell
        path = []
        currentCell = endingCell
        while currentCell in cellWeights:
            previousMarking = cellWeights[currentCell]
            if currentCell == startingCell:
                break
            path.append(self.cellToServiceArea[currentCell])
            currentCell = previousMarking[1]
        path.append(self.cellToServiceArea[currentCell])
        if not currentCell == startingCell:
            raise ValueError("Invalid path")
        path.reverse()
        return path
    
    def CalculateWeights(self, startLocation : ServiceArea, endLocation : ServiceArea) -> dict[Cell, tuple[float, Cell]]:
        if self.serviceAreas is None:
            raise ValueError("ServiceAreas not initialized")
        startingCell = startLocation.cell
        endingCell = endLocation.cell
        markingQueue = PriorityQueue()
        cellWeights = dict[Cell, tuple[float, Cell]]
        cellWeights = dict()
        markedCells : set[Cell]
        markedCells = set()
        markingQueue.put(PrioritizedItem(0.0, startingCell))
        while not len(markingQueue.queue) == 0:
            entry : PrioritizedItem
            entry = markingQueue.get()
            cell : Cell
            cell = entry.item
            currentWeight : float
            currentWeight = entry.priority
            if cell in markedCells:
                continue
            neighbour : Cell
            for neighbour in cell.neighbours:
                weight = self.CalculateDistance(cell.site, neighbour.site)
                newWeight = currentWeight + weight
                newCell = not neighbour in cellWeights
                if not newCell and cellWeights[neighbour][0] == currentWeight + weight:
                    raise ValueError("Incomparable weights")
                closerCell = neighbour in cellWeights and cellWeights[neighbour][0] > newWeight
                if newCell or closerCell:
                    cellWeights[neighbour] = (newWeight, cell)
                if neighbour == endingCell:
                    return cellWeights
                markingQueue.put(PrioritizedItem(newWeight, neighbour))
            markedCells.add(cell)        
                
    @staticmethod
    def CalculateDistance(pointA, pointB):
        distance = math.sqrt((pointB[0]-pointA[0]) ** 2 + (pointB[1]-pointA[1]) ** 2)
        if not isinstance(distance, float):
            raise TypeError("Invalid result")
        if distance < 0.0:
            raise ValueError("Distance cannot be negative")
        return distance
    
    def calculateExpectedDuration(self, movementPath : list[ServiceArea]) -> int:
        totalTime = 0
        if len(movementPath) == 2:
            unitDistance = self.CalculateDistance(movementPath[0].cell.site, movementPath[1].cell.site)
            scaledDistance = GetConfig().simConfig.SCALE * unitDistance
            return math.ceil(scaledDistance * GetConfig().mobilityConfig.localSpeed)
        for i in range(len(movementPath)-1):
            unitDistance = self.CalculateDistance(movementPath[i].cell.site, movementPath[i+1].cell.site)
            scaledDistance = GetConfig().simConfig.SCALE * unitDistance
            if i == 0 or i == len(movementPath)-2:
                totalTime += scaledDistance * (GetConfig().mobilityConfig.localSpeed + GetConfig().mobilityConfig.passingSpeed) * 0.5
                continue
            totalTime += scaledDistance * GetConfig().mobilityConfig.passingSpeed
        totalTime = math.ceil(totalTime)
        return totalTime
    
    def FindCommonBorder(self, startingPosition : ServiceArea, endPosition : ServiceArea):
        startCell = startingPosition.cell
        endCell = endPosition.cell
        ps = []
        for borderpoint in startCell.borderpoints:
            containsPoint = any(map(lambda x : x[0] == borderpoint[0] and x[1] == borderpoint[1], endCell.borderpoints))
            if containsPoint:
                ps.append(borderpoint)
        if not len(ps) == 2:
            raise ValueError("Invalid border")
        return ps[0], ps[1]
    
    def CalculateMovementDuration(self, startPoint, endPoint, isLocalSpeed = False) -> int:
        distance = self.CalculateDistance(startPoint, endPoint)
        scaledDistance = distance * GetConfig().simConfig.SCALE
        if isLocalSpeed:
            return int(math.ceil(GetConfig().mobilityConfig.localSpeed * scaledDistance))
        return int(math.ceil(GetConfig().mobilityConfig.passingSpeed * scaledDistance))
    
    def CalculateTransitionPoint(self, point1, point2):
        return (point1[0] + point2[0] / 2.0), (point1[1] + point2[1] / 2.0)
        
global PATH_GENERATOR
PATH_GENERATOR = None

def SetPathGenerator(generator : PathGenerator):
    global PATH_GENERATOR
    PATH_GENERATOR = generator
    
def GetPathGenerator() -> PathGenerator:
    global PATH_GENERATOR
    if PATH_GENERATOR is None:
        raise ValueError("Path generator not initialized")
    return PATH_GENERATOR
            
        