import numpy as np
from scipy.spatial import Voronoi as V
from Utilities.VoronoiDiagram.Cell import Cell
from Utilities.VoronoiDiagram.VoronoiBuilder import VoronoiBuilder
from Utilities.VoronoiDiagram.Edge import Edge
from Utilities.SiteSpawner import SiteSpawner
from typing import Any
from pygame import Surface

'''Wrapper class for scipy's voronoi - works as an adapter for the simulation data structures'''
class Voronoi(object):
    
    def __init__(self):
        self.sites = np.array(SiteSpawner.SpawnPoints())
        self.voronoi = V(self.sites)
        self.builder = VoronoiBuilder()
        self.createVoronoi()
        
    def getCells(self) -> list[Cell]:
        return list(self.builder.cells.values())
        
    def createVoronoi(self):
        self.defineCells()
        self.generateCell()
        self.addNeighbourRelations()        
            
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
            
    def addNeighbourRelations(self):
        for i in range(len(self.voronoi.ridge_points)):
            ridge = self.voronoi.ridge_points[i]
            siteA, siteB = self.getSite(ridge[0]), self.getSite(ridge[1])
            if(self.isValidNeighbour(siteA, siteB)):
                cellA, cellB = self.builder.cells[siteA], self.builder.cells[siteB]
                cellA.addNeighbour(cellB)
                cellB.addNeighbour(cellA)
                edge = Edge(cellA.site, cellB.site)
                self.builder.edges.append(edge)
    
    def getSiteAndRegion(self, index):
        point_region = self.voronoi.point_region
        site = self.getSite(index)
        region = self.voronoi.regions[point_region[index]]
        return site, region
    
    def getSite(self, index) -> tuple[Any, Any]:
        p = self.voronoi.points[index]
        return (p[0], p[1])
        
    def isInvalid(self, site, region):
        if(region == None or -1 in region):
            return True
        for index in region:
            if(index == -1):
                continue
            point = self.voronoi.vertices[index]
            if(point[0] < 0.0 or point[0] > 1.0 or point[1] < 0.0 or point[1] > 1.0):
                return True
        if(site in self.builder.sites):
            return True
        return False
    
    def isValidNeighbour(self, siteA, siteB):
        if(self.builder.containsSite(siteA) and self.builder.containsSite(siteB)):
            return True
        return False
    
    def draw(self, surface : Surface):
        for cell in self.builder.cells.values():
            cell.draw(surface)
        
    def drawEdges(self, surface : Surface):
        edge : Edge
        for edge in self.builder.edges:
            edge.draw(surface)