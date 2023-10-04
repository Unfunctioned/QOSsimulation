from random import Random
'''Stores the configurations for random variables'''
class Randoms(object):
    
    def __init__(self) -> None:
        self.siteGeneration = Random(0)
        self.colorGeneration = Random(0)
        self.pointGeneration = Random(0)
        self.areaTypeSelection = Random(0)
        self.activitySimulation = Random(0)
        self.activityDelay = Random(0)
        self.latencySimulation = Random(0)
        self.latencyDelay = Random(0)
        self.workDurationSimulation = Random(0)
        self.businessProcessActivationSimulation = Random(0)
        self.companyLocationGeneration = Random(0)