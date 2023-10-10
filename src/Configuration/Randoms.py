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
        self.latencySpikeSimulation = Random(0)
        self.latencyDelay = Random(0)
        self.workDurationSimulation = Random(0)
        self.businessProcessActivationSimulation = Random(0)
        self.companyLocationGeneration = Random(0)
        self.flowSelector = Random(0)
        self.customerLocationSelector = Random(0)
        
        #Probability that the latency will be stable at the 10 ms 
        self.LATENCY_PERCENTAGE_STABLE = 0.9