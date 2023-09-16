import pygame

'''Represents a line connecting two neighbouring Voronoi sites'''
class Edge(object):
    
    def __init__(self, p1, p2) -> None:
        self.p1 = p1
        self.p2 = p2
        
    def draw(self, window):
        scaled_p1 = self.p1[0]*window.window_size[0], self.p1[1]*window.window_size[1]
        scaled_p2 = self.p2[0]*window.window_size[0], self.p2[1]*window.window_size[1]
        pygame.draw.line(window.screen, (0, 0, 255), scaled_p1, scaled_p2, 5)