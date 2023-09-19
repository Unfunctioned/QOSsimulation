import random
from UI.UIPoint import UIPoint
from Configuration.globals import CONFIG
class RandomPointSpawner(object):
    
    def __init__(self) -> None:
        pass
    
    def SpawnPoints(self, count):
        points = []
        for _ in range(0,count):
            x = CONFIG.randomConfig.pointGeneration.random()
            y = CONFIG.randomConfig.pointGeneration.random()
            points.append(UIPoint((x,y)))
        return points
        