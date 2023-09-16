import random

class SiteSpawner(object):
    
    def __init__(self, config) -> None:
        self.gridsize = config.GRIDSIZE
    
    def SpawnPoints(self):
        cellsize = 1.0/self.gridsize
        points = []
        for i in range(0, self.gridsize):
            for j in range(0, self.gridsize):
                x = random.random() * cellsize + i*cellsize
                y = random.random() * cellsize + j*cellsize
                #x = 0.5 * cellsize + i*cellsize
                #y = 0.5 * cellsize + j*cellsize
                points.append((x,y))
        return points