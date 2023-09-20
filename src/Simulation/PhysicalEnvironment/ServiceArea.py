from Configuration.globals import CONFIG
from Simulation.PhysicalEnvironment.AreaType import AreaType
from UI.Colors import Colors
'''Represents the service area in the simulation'''
class ServiceArea(object):
    
    def __init__(self, cell) -> None:
        self.areaType = CONFIG.randoms.areaTypeSelection.choice(list(AreaType))
        self.cell = cell
        cell.colorcode = Colors.GetColorCodeByAreaType(self.areaType)
        
    def draw(self, window):
        self.cell.draw(window)
        
    def drawInfo(self, window):
        self.cell.drawInfo(window)