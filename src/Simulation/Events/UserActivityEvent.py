from Configuration.globals import CONFIG
from Simulation.PhysicalEnvironment.ServiceArea import ServiceArea
import math
'''Triggers a change of user activity in a service area'''
class UserActivityEvent(object):
    
    @staticmethod
    def generateEvent(currentTime, serviceArea):
        delayConfig = CONFIG.eventConfig.activityDelayRange
        delay = CONFIG.randoms.activityDelay.randint(delayConfig[0], delayConfig[1])
        eventTime = currentTime + delay
        return UserActivityEvent(eventTime, serviceArea)
    
    @staticmethod
    def generateFollowUp(previousEvent):
        delayConfig = CONFIG.eventConfig.activityDelayRange
        delay = CONFIG.randoms.activityDelay.randint(delayConfig[0], delayConfig[1])
        eventTime = previousEvent.t + delay
        newEvent = UserActivityEvent(eventTime, previousEvent.area)
        remainingBoostDuration = previousEvent.baseActivityDuration - delay
        if(remainingBoostDuration > 0):
            newEvent.baseActivityDuration = remainingBoostDuration
            newEvent.baseActivityBoost = previousEvent.baseActivityBoost
            if(remainingBoostDuration < delay):
                newEvent.t = previousEvent.t + remainingBoostDuration
        return newEvent
        
    def __init__(self, t, area : ServiceArea) -> None:
        self.t = t
        self.area = area
        self.baseActivityBoost = CONFIG.randoms.activitySimulation.random()
        durationConfig = CONFIG.simConfig.MAX_NETWORK_ACTIVITY_SPIKE_DURATION
        durationFactor = CONFIG.randoms.activitySimulation.random() * 1.2 - 0.2
        self.baseActivityDuration = math.floor(durationConfig * durationFactor)
        self.generateFollowUp = True        
        
    def trigger(self):
        modifier = 0.9 + CONFIG.randoms.activitySimulation.random()*0.2
        self.area.ChangeActivity(self.t, modifier, self.baseActivityBoost)