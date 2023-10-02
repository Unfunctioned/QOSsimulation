from Configuration.globals import CONFIG
from Simulation.Events.Event import Event
'''Event to change the latency in a service area'''
class LatencyEvent(Event):
    
    @staticmethod
    def generateEvent(currentTime, serviceArea):
        delayConfig = CONFIG.eventConfig.latencyEventDelayRange
        delay = CONFIG.randoms.latencyDelay.randint(delayConfig[0], delayConfig[1])
        eventTime = currentTime + delay
        return LatencyEvent(eventTime, serviceArea.localServiceNetwork)
    
    @staticmethod
    def generateFollowUp(previousEvent):
        delayConfig = CONFIG.eventConfig.latencyEventDelayRange
        delay = CONFIG.randoms.activityDelay.randint(delayConfig[0], delayConfig[1])
        eventTime = previousEvent.t + delay
        newEvent = LatencyEvent(eventTime, previousEvent.network)
        return newEvent
    
    def __init__(self, eventTime, network) -> None:
        super().__init__(eventTime)
        self.network = network
        self.generateFollowUpEvent = True
        
    def trigger(self):
        modifier = 0.9 + CONFIG.randoms.latencySimulation.random()*0.2
        self.network.UpdateLatency(self.t, modifier)