from random import Random
from Configuration.BaseConfig import BaseConfig
'''Stores the configurations for random variables'''
class Randoms(BaseConfig):
    
    def __init__(self, seeds = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]) -> None:
        self.seeds = seeds
        self.siteGeneration = Random(seeds[0])
        self.colorGeneration = Random(seeds[1])
        self.pointGeneration = Random(seeds[2])
        self.areaTypeSelection = Random(seeds[3])
        self.activitySimulation = Random(seeds[4])
        self.activityDelay = Random(seeds[5])
        self.latencySimulation = Random(seeds[6])
        self.latencySpikeSimulation = Random(seeds[7])
        self.latencyDelay = Random(seeds[8])
        self.workDurationSimulation = Random(seeds[9])
        self.businessProcessActivationSimulation = Random(seeds[10])
        self.companyLocationGeneration = Random(seeds[11])
        self.flowSelector = Random(seeds[12])
        self.customerLocationSelector = Random(seeds[13])
        self.userActivitySpikeSimulation = Random(seeds[14])
        
    def jsonable(self):
        return self.seeds