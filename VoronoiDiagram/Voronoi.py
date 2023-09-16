import numpy as np
from scipy.spatial import Voronoi as V, voronoi_plot_2d
import matplotlib.pyplot as plt
from VoronoiDiagram.Cell import *

class Voronoi(object):
    
    def __init__(self, sites):
        self.sites = np.array(sites)
        self.voronoi = V(self.sites)
        
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
        #valid_regions = self.selectClosedRegions()
        #cells = {}
        #ridgeDict = self.voronoi.ridge_dict
        #for key in ridgeDict:
        #    value = ridgeDict[key]
        #    if(-1 in key or -1 in value):
        #        continue
        #    cells = self.addCell(cells, key, value)
        return cells
        
    def addCell(self, cells, key, value):
        edge = self.createEdge(value)
        for i in key:
                if(not i in cells):
                    cells[i] = [edge]
                else:
                    cells[i].append(edge)
        return cells
        
    def createEdge(self, value):
        vertices = self.voronoi.vertices
        p1 = vertices[value[0]]
        p2 = vertices[value[1]]
        return Edge(p1, p2)
        
    def selectClosedRegions(self):
        valid_regions = []
        for region in self.voronoi.regions:
            if(region == None or region == []):
                continue
            if(-1 in region):
                continue
            valid_regions.append(region)
        return valid_regions