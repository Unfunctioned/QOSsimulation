import random
from UI.UIPoint import UIPoint
from Configuration.globals import GetConfig
class RandomPointSpawner:
    
    @staticmethod
    def SpawnPoints(count):
        points = []
        for _ in range(0,count):
            x = GetConfig().randoms.pointGeneration.random()
            y = GetConfig().randoms.pointGeneration.random()
            points.append(UIPoint((x,y)))
        return points
        