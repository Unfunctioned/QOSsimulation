import random
from UI.UIPoint import UIPoint
from Configuration.globals import GetConfig
class RandomPointSpawner(object):
    
    def __init__(self) -> None:
        pass
    
    def SpawnPoints(self, count):
        points = []
        for _ in range(0,count):
            x = GetConfig().randoms.pointGeneration.random()
            y = GetConfig().randoms.pointGeneration.random()
            points.append(UIPoint((x,y)))
        return points
        