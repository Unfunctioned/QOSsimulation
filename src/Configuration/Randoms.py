from random import Random
from Configuration.BaseConfig import BaseConfig
'''Stores the configurations for random variables'''
class Randoms(BaseConfig):
    
    def __init__(self, seeds = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]) -> None:
        if not len(seeds) == 13:
            raise ValueError("Invalid seed count")
        self.seeds = seeds
        self.siteGeneration = Random(seeds[0])
        self.pointGeneration = Random(seeds[1])
        self.activitySimulation = Random(seeds[2])
        self.activityDelay = Random(seeds[3])
        self.latencySimulation = Random(seeds[4])
        self.latencySpikeSimulation = Random(seeds[5])
        self.latencyDelay = Random(seeds[6])
        self.workDurationSimulation = Random(seeds[7])
        self.businessProcessActivationSimulation = Random(seeds[8])
        self.companyLocationGeneration = Random(seeds[9])
        self.flowSelector = Random(seeds[10])
        self.customerLocationSelector = Random(seeds[11])
        self.userActivitySpikeSimulation = Random(seeds[12])
        
    def jsonable(self):
        return self.seeds