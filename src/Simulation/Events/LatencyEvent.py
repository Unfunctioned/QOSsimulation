from Configuration.globals import GetConfig
from Simulation.Events.Event import Event
from Simulation.NetworkEnvironment.LocalServiceNetwork import LocalServiceNetwork
'''Event to change the latency in a service area'''
class LatencyEvent(Event):
    
    @staticmethod
    def generateEvent(currentTime, serviceArea):
        delayConfig = GetConfig().eventConfig.latencyEventDelayRange
        delay = GetConfig().randoms.latencyDelay.randint(delayConfig[0], delayConfig[1])
        eventTime = currentTime + delay
        return LatencyEvent(eventTime, serviceArea.localServiceNetwork)
    
    @staticmethod
    def generateFollowUp(previousEvent, eventTime):
        newEvent = LatencyEvent(eventTime, previousEvent.network)
        return newEvent
    
    def __init__(self, eventTime, network : LocalServiceNetwork) -> None:
        super().__init__(eventTime)
        self.network = network
        self.modifier = 0.95 + GetConfig().randoms.latencySimulation.random()*0.1
        self.generateFollowUpEvent = True
        
    def trigger(self):
        self.network.UpdateLatency(self.t, self.modifier, 0)
        

class LatencySpikeEvent(LatencyEvent):
    
    def __init__(self, eventTime, network : LocalServiceNetwork) -> None:
        super().__init__(eventTime, network)
        durationConfig = GetConfig().eventConfig.latencySpikeDurationRange
        self.spikeDuration = GetConfig().randoms.latencySpikeSimulation.randint(durationConfig[0], durationConfig[1])
        defaultLatency = GetConfig().simConfig.DEFAULT_LATENCY
        self.spike = GetConfig().randoms.latencySpikeSimulation.random() * defaultLatency
        
    def SetSpike(self, spikeValue, duration : int):
        self.spike = spikeValue
        self.spikeDuration = duration
    
    def trigger(self):
        #Latency spikes stay below the double of the default latency
        self.network.UpdateLatency(self.t, self.modifier, self.spike)