'''Stores data structures needed during Voronoi generation'''
class VoronoiBuilder(object):
    
    def __init__(self) -> None:
        self.sites = {}
        self.cells = []
        
    def addRegion(self, site, region):
        self.sites[site] = region