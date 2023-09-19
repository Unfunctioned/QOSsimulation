'''Stores data structures needed during Voronoi generation'''
class VoronoiBuilder(object):
    
    def __init__(self) -> None:
        self.sites = {}
        self.cells = {}
        self.edges = []
        
    def addRegion(self, site, region):
        self.sites[site] = region
        
    def addCell(self, site, cell):
        if(not site in self.cells):
            self.cells[site] = cell
        else:
            ValueError("Key with value {site} already exists")
            
    def containsSite(self, site):
        if(site in self.sites):
            return True
        return False