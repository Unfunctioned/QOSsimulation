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
        points = self.pointSpawner.SpawnPoints(CONFIG.simConfig.WEIGHTS)
        self.matchPointsToCell(points)
        self.world = World()
        self.world.generateServiceAreas(self.voronoi.cells)
        self.world.printInfo()
        
        
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
        