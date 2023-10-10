from Configuration.globals import CONFIG
from Simulation.Events.Event import Event
from Simulation.NetworkEnvironment.LocalServiceNetwork import LocalServiceNetwork
'''Event to change the latency in a service area'''
class LatencyEvent(Event):
    
    @staticmethod
    def generateEvent(currentTime, serviceArea):
        delayConfig = CONFIG.eventConfig.latencyEventDelayRange
        delay = CONFIG.randoms.latencyDelay.randint(delayConfig[0], delayConfig[1])
        eventTime = currentTime + delay
        return LatencyEvent(eventTime, serviceArea.localServiceNetwork)
    
    @staticmethod
    def generateFollowUp(previousEvent, eventTime):
        newEvent = LatencyEvent(eventTime, previousEvent.network)
        return newEvent
    
    def __init__(self, eventTime, network : LocalServiceNetwork) -> None:
        super().__init__(eventTime)
        self.network = network
        self.generateFollowUpEvent = True
        
    def trigger(self):
        modifier = 0.95 + CONFIG.randoms.latencySimulation.random()*0.1
        self.network.UpdateLatency(self.t, modifier, 0)
        

class LatencySpikeEvent(LatencyEvent):
    
    def __init__(self, eventTime, network : LocalServiceNetwork) -> None:
        super().__init__(eventTime, network)
        self.generateFollowUpEvent = True
        durationConfig = CONFIG.eventConfig.latencySpikeDurationRange
        self.spikeDuration = CONFIG.randoms.latencySpikeSimulation.randint(durationConfig[0], durationConfig[1])
        
    def SetSpikeDuration(self, duration : int):
        self.spikeDuration = duration
    
    def trigger(self):
        #Latency spikes stay below the double of the default latency
        defaultLatency = CONFIG.simConfig.DEFAULT_LATENCY
        spikeValue = CONFIG.randoms.latencySpikeSimulation.random() * defaultLatency
        modifier = 0.95 + CONFIG.randoms.latencySimulation.random()*0.1
        self.network.UpdateLatency(self.t, modifier, spikeValue)