'''Used to store temporary capacity demand data'''
class CapacityDemand(object):
    
    def __init__(self, privateDemand, publicMinimum, publicMaximum, capacity) -> None:
        self.private = privateDemand
        self.publicMinimum = publicMinimum
        self.publicMaximum = publicMaximum
        self.maximumCapacity = capacity