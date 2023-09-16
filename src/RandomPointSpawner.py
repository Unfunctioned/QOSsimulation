import random
class RandomPointSpawner(object):
    
    def __init__(self) -> None:
        pass
    
    def SpawnPoints(self, count):
        points = []
        for _ in range(0,count):
            x = random.random()
            y = random.random()
            points.append((x,y))
        return points
        