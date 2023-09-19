import pygame

'''Represent a visual point on the UI'''
class UIPoint(object):
    
    def __init__(self, position) -> None:
        self.position = position
        self.color = (0, 0, 0)
        
    def draw(self, window):
        scaled_position = self.position[0]*window.window_size[0], self.position[1]*window.window_size[1]
        pygame.draw.circle(window.screen, self.color, scaled_position, 3)
        