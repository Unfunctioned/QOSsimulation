from pygame.draw import line
from pygame import Surface
from Configuration.globals import GetConfig

'''Represents a line connecting two neighbouring Voronoi sites'''
class Edge(object):
    
    def __init__(self, p1, p2) -> None:
        self.p1 = p1
        self.p2 = p2
        
    def draw(self, surface : Surface):
        resolution = GetConfig().appSettings.WINDOW_SIZE
        scaled_p1 = self.p1[0]*resolution[0], self.p1[1]*resolution[1]
        scaled_p2 = self.p2[0]*resolution[0], self.p2[1]*resolution[1]
        line(surface, (0, 0, 255), scaled_p1, scaled_p2, 5)