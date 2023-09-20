from Simulation.PhysicalEnvironment.ServiceArea import ServiceArea
'''Objects that represents the entire simulation environment'''
class World(object):
    
    def __init__(self) -> None:
        self.serviceArea = []
        
    def generateServiceAreas(self, cells):
        for cell in cells:
            self.serviceArea.append(ServiceArea(cell))
            
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