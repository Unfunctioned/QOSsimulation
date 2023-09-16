import pygame

class Cell(object):
    
    def __init__(self, site, borderpoints):
        self.site = site
        self.borderpoints = borderpoints
        self.neighbours = set()
        
        
    def draw(self, window):
        scaledpoints = []
        for i in self.borderpoints:
            scaledpoint = i[0]*window.window_size[0],i[1]*window.window_size[1]
            scaledpoints.append(scaledpoint)
        scaled_site = self.site[0]*window.window_size[0], self.site[1]*window.window_size[1]
        pygame.draw.polygon(window.screen, (0,0,0), scaledpoints, 3)
        pygame.draw.circle(window.screen, (0,0,255), scaled_site, 3)
        
    def addNeighbour(self, cell):
        self.neighbours.add(cell)