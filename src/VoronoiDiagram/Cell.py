import pygame
from UI.Colors import *

class Cell(object):
    
    def __init__(self, site, borderpoints):
        self.site = site
        self.borderpoints = borderpoints
        self.neighbours = set()
        self.color = Colors.GetRandomColor()
        boundingBox = self.findBound()
        self.minBound = (boundingBox[0], boundingBox[1])
        self.maxBound = (boundingBox[2], boundingBox[3])
        
        
    def draw(self, window):
        scaledpoints = []
        for i in self.borderpoints:
            scaledpoint = i[0]*window.window_size[0],i[1]*window.window_size[1]
            scaledpoints.append(scaledpoint)
        scaled_site = self.site[0]*window.window_size[0], self.site[1]*window.window_size[1]
        scaled_minBound = self.minBound[0]*window.window_size[0], self.minBound[1]*window.window_size[1]
        scaled_maxBound = self.maxBound[0]*window.window_size[0], self.maxBound[1]*window.window_size[1]
        pygame.draw.polygon(window.screen, Colors.GetLightVariant(self.color), scaledpoints, 0)
        pygame.draw.polygon(window.screen, (0,0,0), scaledpoints, 3)
        pygame.draw.circle(window.screen, (0,0,255), scaled_site, 3)
        pygame.draw.rect(window.screen, (133,8,120),
                         pygame.Rect(scaled_minBound[0], scaled_minBound[1],
                                     scaled_maxBound[0]-scaled_minBound[0], scaled_maxBound[1]-scaled_minBound[1]), 1)
        
    def addNeighbour(self, cell):
        self.neighbours.add(cell)
        
    def findBound(self):
        bound = [self.borderpoints[0][0],self.borderpoints[0][1],self.borderpoints[0][0],self.borderpoints[0][1]]
        for i in range(1, len(self.borderpoints)):
            point = self.borderpoints[i]
            if(point[0] < bound[0]):
                bound[0] = point[0]
            if (point[1] < bound[1]):
                bound[1] = point[1]
            if (point[0] > bound[2]):
                bound[2] = point[0]
            if (point[1] > bound[3]):
                bound[3] = point[1]
        return bound