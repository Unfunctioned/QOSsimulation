from RandomPointSpawner import *
from SiteSpawner import *
from VoronoiDiagram.Voronoi import *
from Configuration.globals import *

'''Responsible for generating the simulation environment'''
class WorldGenerator(object):
    
    def __init__(self) -> None:
        self.pointSpawner = RandomPointSpawner()
        self.siteSpawner = SiteSpawner()
        self.voronoi = Voronoi(self.siteSpawner.SpawnPoints())
        self.points = self.pointSpawner.SpawnPoints(CONFIG.DENSITY_LEVEL)
        