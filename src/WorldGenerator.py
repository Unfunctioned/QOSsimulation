from RandomPointSpawner import *
from SiteSpawner import *
from VoronoiDiagram.Voronoi import *

'''Responsible for generating the simulation environment'''
class WorldGenerator(object):
    
    def __init__(self, config) -> None:
        self.pointSpawner = RandomPointSpawner()
        self.siteSpawner = SiteSpawner(config)
        self.voronoi = Voronoi(self.siteSpawner.SpawnPoints())
        #self.points = pointSpawner.SpawnPoints(self.config.DENSITY_LEVEL)
        