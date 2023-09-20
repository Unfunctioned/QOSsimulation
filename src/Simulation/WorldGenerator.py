from Utilities.RandomPointSpawner import *
from Utilities.SiteSpawner import *
from Utilities.VoronoiDiagram.Voronoi import *
from Configuration.globals import *
from Simulation.World import World

'''Responsible for generating the simulation environment'''
class WorldGenerator(object):
    
    def __init__(self) -> None:
        self.pointSpawner = RandomPointSpawner()
        self.siteSpawner = SiteSpawner()
        self.voronoi = Voronoi(self.siteSpawner.SpawnPoints())
        self.world = World()
        self.world.generateServiceAreas(self.voronoi.cells)
        self.world.printInfo()
        #self.points = self.pointSpawner.SpawnPoints(CONFIG.DENSITY_LEVEL)
        #self.matchPointsToCell()
        
        
    def matchPointsToCell(self):
        for point in self.points:
            for cell in self.voronoi.cells:
                if(cell.isPointinCell(point.position)):
                    point.color = Colors.GetColor(cell.colorcode)
                    
    def draw(self, window):
        self.world.draw(window)
        self.world.drawInfo(window)
        #self.voronoi.drawEdges(window)
        #for point in self.points:
        #    point.draw(window)
        