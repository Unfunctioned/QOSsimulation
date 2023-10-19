import random
from Configuration.globals import GetConfig
from Configuration.globals import *

class SiteSpawner:
    
    @staticmethod
    def SpawnPoints():
        gridsize = GetConfig().simConfig.GRIDSIZE
        generator = GetConfig().randoms.siteGeneration
        cellsize = 1.0/gridsize
        points = []
        for i in range(0, gridsize):
            for j in range(0, gridsize):
                x = generator.random() * cellsize + i*cellsize
                y = generator.random() * cellsize + j*cellsize
                #x = 0.5 * cellsize + i*cellsize
                #y = 0.5 * cellsize + j*cellsize
                points.append((x,y))
        return points