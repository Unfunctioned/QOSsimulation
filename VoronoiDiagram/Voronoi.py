import numpy as np
from scipy.spatial import Voronoi as V, voronoi_plot_2d
import matplotlib.pyplot as plt
from VoronoiDiagram.Cell import *

class Voronoi(object):
    
    def __init__(self, sites):
        self.sites = np.array(sites)
        self.voronoi = V(self.sites)
        self.cells = self.createVoronoi()
        
    def createVoronoi(self):
        sites = {}
        cells = []
        point_region = self.voronoi.point_region
        for i in range(len(point_region)):
            p = self.voronoi.points[i]
            region = self.voronoi.regions[point_region[i]]
            if(region == None or -1 in region):
                continue
            site = (p[0], p[1])
            if(not site in sites):
                sites[site] = region
        for site in sites:
            borderpoints = []
            region = sites[site]
            for i in region:
                borderpoints.append(self.voronoi.vertices[i])
            cell = Cell(site, borderpoints)
            cells.append(cell)
        return cells
    
    def draw(self, window):
        for cell in self.cells:
            cell.draw(window)
            