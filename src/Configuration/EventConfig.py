'''Stores configurations for event generation'''
class EventConfig(object):
    
    def __init__(self) -> None:
        self.activityEventDelayRange = (15,30)
        self.latencyEventDelayRange = (15,30)
        self.latencySpikeDelayRange = (300,1200)
        self.latencySpikeDurationRange = (1, 120)
        self.businessProcessActivationDelayRange = (0, 900)