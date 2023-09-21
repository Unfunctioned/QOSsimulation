from Simulation.PhysicalEnvironment.ServiceArea import ServiceArea
from Configuration.globals import CONFIG
from Simulation.PhysicalEnvironment.AreaType import AreaType
import math
'''Objects that represents the entire simulation environment'''
class World(object):
    
    def __init__(self) -> None:
        self.serviceArea = []
        
    def generateServiceAreas(self, cells):
        areaDefinitions = self.designateAreaTypes(cells)
        for (type, cell) in areaDefinitions:
            self.serviceArea.append(ServiceArea(cell, type))
            
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
            
    def printInfo(self):
        totalArea = 0.0
        for serviceArea in self.serviceArea:
            totalArea += serviceArea.cell.area
        print("Total area: {area}".format(area = totalArea))
            
    def draw(self, window):
        for serviceArea in self.serviceArea:
            serviceArea.draw(window)
            
    def drawInfo(self, window):
        for serviceArea in self.serviceArea:
            serviceArea.drawInfo(window)