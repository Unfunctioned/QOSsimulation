from Configuration.globals import GetConfig
from Simulation.PhysicalEnvironment.ServiceArea import ServiceArea
from Simulation.Events.Event import Event
import math
'''Triggers a change of user activity in a service area'''
class UserActivityEvent(Event):
    
    @staticmethod
    def generateEvent(currentTime, serviceArea):
        delayConfig = GetConfig().eventConfig.activityEventDelayRange
        delay = GetConfig().randoms.activityDelay.randint(delayConfig[0], delayConfig[1])
        eventTime = currentTime + delay
        return UserActivityEvent(eventTime, serviceArea)
    
    @staticmethod
    def generateFollowUp(previousEvent, eventTime):
        newEvent = UserActivityEvent(eventTime, previousEvent.area)
        return newEvent
        
    def __init__(self, eventTime, area : ServiceArea) -> None:
        super().__init__(eventTime)
        self.area = area
        #self.modifier = GetConfig().randoms.activitySimulation.random()
        self.modifier = 0.9 + GetConfig().randoms.activitySimulation.random()*0.2
        self.generateFollowUpEvent = True        
        
    def trigger(self):
        self.area.ChangeActivity(self.t, self.modifier)
        
'''Event used to trigger "busy hour" periods, with high user activities'''
class UserActivitySpikeEvent(UserActivityEvent):
    
    def __init__(self, eventTime, area: ServiceArea) -> None:
        super().__init__(eventTime, area)
        durationConfig = GetConfig().eventConfig.userActivitySpikeDurationRange
        self.activityBoostDuration = GetConfig().randoms.userActivitySpikeSimulation.randint(durationConfig[0], durationConfig[1])
        self.spike = GetConfig().randoms.userActivitySpikeSimulation.random() * (1 - self.area.default_activity)
    
    def SetSpike(self, spike, duration : int):
        self.spike = spike
        self.activityBoostDuration = duration
        
    def trigger(self):
        self.area.ChangeActivity(self.t, self.modifier, self.spike)