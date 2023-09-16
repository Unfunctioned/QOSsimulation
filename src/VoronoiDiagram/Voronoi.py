import numpy as np
from scipy.spatial import Voronoi as V
from VoronoiDiagram.Cell import *
from VoronoiDiagram.VoronoiBuilder import *
from VoronoiDiagram.Edge import *

class Voronoi(object):
    
    def __init__(self, sites):
        self.sites = np.array(sites)
        self.voronoi = V(self.sites)
        self.builder = VoronoiBuilder()
        self.createVoronoi()
        self.cells = self.builder.cells.values()
        self.edges = self.builder.edges
        
    def createVoronoi(self):
        self.defineCells()
        self.generateCell()
        for i in range(len(self.voronoi.ridge_points)):
            ridge = self.voronoi.ridge_points[i]
            siteA, siteB = self.getSite(ridge[0]), self.getSite(ridge[1])
            if(self.builder.containsSite(siteA) and self.builder.containsSite(siteB)):
                cellA, cellB = self.builder.cells[siteA], self.builder.cells[siteB]
                cellA.addNeighbour(cellB)
                cellB.addNeighbour(cellA)
                edge = Edge(cellA.site, cellB.site)
                self.builder.edges.append(edge)
        print("Take a break!")
            
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
            self.builder.addCell(site, cell)
    
    def getSiteAndRegion(self, index):
        point_region = self.voronoi.point_region
        site = self.getSite(index)
        region = self.voronoi.regions[point_region[index]]
        return site, region
    
    def getSite(self, index):
        p = self.voronoi.points[index]
        return (p[0], p[1])
        
    def isInvalid(self, site, region):
        if(region == None or -1 in region):
            return True
        if(site in self.builder.sites):
            return True
        return False
    
    def draw(self, window):
        for cell in self.cells:
            cell.draw(window)
        for edge in self.edges:
            edge.draw(window)
            