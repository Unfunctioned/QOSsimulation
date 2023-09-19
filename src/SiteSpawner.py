import random
from Configuration.globals import CONFIG
from Configuration.globals import *

class SiteSpawner(object):
    
    def __init__(self) -> None:
        self.gridsize = CONFIG.GRIDSIZE
    
    def SpawnPoints(self):
        generator = CONFIG.randomConfig.siteGeneration
        cellsize = 1.0/self.gridsize
        points = []
        for i in range(0, self.gridsize):
            for j in range(0, self.gridsize):
                x = generator.random() * cellsize + i*cellsize
                y = generator.random() * cellsize + j*cellsize
                #x = 0.5 * cellsize + i*cellsize
                #y = 0.5 * cellsize + j*cellsize
                points.append((x,y))
        return points