from Configuration.BaseConfig import BaseConfig
'''Stores configurations for event generation'''
class EventConfig(BaseConfig):
    
    def __init__(self) -> None:
        self.activityEventDelayRange = (15,30)
        self.latencyEventDelayRange = (15,30)
        self.latencySpikeDelayRange = (0,2400)
        self.latencySpikeDurationRange = (1, 2)
        self.businessProcessActivationDelayRange = (0, 900)
        self.userActivitySpikeDurationRange = (900, 1800)
        self.userActivitypikeDelayRange = (0, 1800)
        #Probability that the latency will be stable at the 10 ms 
        #self.LATENCY_PERCENTAGE_STABLE = 0.9
        
    def jsonable(self):
        return self.__dict__