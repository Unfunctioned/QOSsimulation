import numpy as np
from scipy.spatial import Voronoi as V, voronoi_plot_2d
import matplotlib.pyplot as plt
from VoronoiDiagram.Cell import *
from VoronoiDiagram.VoronoiBuilder import *

class Voronoi(object):
    
    def __init__(self, sites):
        self.sites = np.array(sites)
        self.voronoi = V(self.sites)
        self.builder = VoronoiBuilder()
        self.createVoronoi()
        self.cells = self.builder.cells
        
    def createVoronoi(self):
        self.defineCells()
        self.generateCell()
            
    def defineCells(self):
        for i in range(len(self.voronoi.point_region)):
            site, region = self.getSiteAndRegion(i)
            if(self.isInvalid(site, region)):
                continue
            self.builder.addRegion(site, region)
            
    def generateCell(self):
        for site in self.builder.sites:
            borderpoints = []
            region = self.builder.sites[site]
            for i in region:
                borderpoints.append(self.voronoi.vertices[i])
            cell = Cell(site, borderpoints)
            self.builder.cells.append(cell)
    
    def getSiteAndRegion(self, index):
        point_region = self.voronoi.point_region
        p = self.voronoi.points[index]
        site = (p[0], p[1])
        region = self.voronoi.regions[point_region[index]]
        return site, region
        
    def isInvalid(self, site, region):
        if(region == None or -1 in region):
            return True
        if(site in self.builder.sites):
            return True
        return False
    
    def draw(self, window):
        for cell in self.cells:
            cell.draw(window)
            