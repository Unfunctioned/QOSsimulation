from pygame import Surface
from pygame.draw import circle
from Configuration.globals import GetConfig

'''Represent a visual point on the UI'''
class UIPoint(object):
    
    def __init__(self, position) -> None:
        self.position = position
        self.color = (0, 0, 0)
        
    def draw(self, surface : Surface):
        resolution = GetConfig().appSettings.WINDOW_SIZE
        scaled_position = self.position[0]*resolution[0], self.position[1]*resolution[1]
        circle(surface, self.color, scaled_position, 3)
        