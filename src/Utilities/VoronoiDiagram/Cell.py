import pygame
from UI.Colors import *
from pygame.font import Font
from pygame import Surface

class Cell(object):
    
    def __init__(self, site, borderpoints):
        self.site = site
        self.borderpoints = borderpoints
        self.neighbours = set()
        self.area = self.calculateSize()
        self.colorcode = ColorCode.WHITE
        boundingBox = self.findBound()
        self.minBound = (boundingBox[0], boundingBox[1])
        self.maxBound = (boundingBox[2], boundingBox[3])
        self.weight = 0
        
    def Terminate(self):
        self.neighbours = None
        
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
    
    def calculateSize(self):
        area = 0.0
        for i in range(len(self.borderpoints)):
            p1 = self.borderpoints[i-1]
            p2 = self.borderpoints[i]
            area += self.calculateTriangleArea(p1, p2, self.site)
        return area
        
    def calculateTriangleArea(self, p1, p2, p3):
        return 0.5*abs(p1[0]*(p2[1]-p3[1])+p2[0]*(p3[1]-p1[1])+p3[0]*(p1[1]-p2[1]))
    
    #Uses the winding numbers algorihm by Dan Sunday presented in
    # http://profs.ic.uff.br/~anselmo/cursos/CGI/slidesNovos/Inclusion%20of%20a%20Point%20in%20a%20Polygon.pdf
    def isPointinCell(self, point):
        if(not (point[0] > self.minBound[0] and point[1] > self.minBound[1]
           and point[0] < self.maxBound[0] and point[1] < self.maxBound[1])):
            return False
        
        windingNumber = 0
        
        for i in range(-1, len(self.borderpoints)-1):
            p1, p2 = self.borderpoints[i], self.borderpoints[i+1]
            isLeft = self.isLeft(p1, p2, point)
            if(p1[1] <= point[1]):
                if(p2[1] > point[1] and isLeft > 0.0):
                    windingNumber += 1
            elif(p2[1] <= point[1] and isLeft < 0.0):
                windingNumber -= 1
        
        if(windingNumber == 0):
            return False
        return True
        
    def isLeft(self, p1, p2, pTest):
        return (p2[0] - p1[0]) * (pTest[1] - p1[1]) - (pTest[0] - p1[0]) * (p2[1] - p1[1])
    
    def draw(self, screen : Surface):
        scaledpoints = []
        resolution = GetConfig().appSettings.WINDOW_SIZE
        for i in self.borderpoints:
            scaledpoint = i[0]*resolution[0],i[1]*resolution[1]
            scaledpoints.append(scaledpoint)
        scaled_site = self.site[0]*resolution[0], self.site[1]*resolution[1]
        pygame.draw.polygon(screen, Colors.GetLightVariant(self.colorcode), scaledpoints, 0)
        pygame.draw.polygon(screen, (0,0,0), scaledpoints, 3)
        pygame.draw.circle(screen, (0,0,255), scaled_site, 3)

    def drawInfo(self, screen : Surface, font : Font):
        resolution = GetConfig().appSettings.WINDOW_SIZE
        scaled_site = self.site[0]*resolution[0], self.site[1]*resolution[1]
        textSurface = font.render('{area}'.format(area = round(self.area, 4)), False, (0, 0, 0))
        screen.blit(textSurface, scaled_site)