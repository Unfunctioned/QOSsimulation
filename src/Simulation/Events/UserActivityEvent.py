from Configuration.globals import CONFIG
from Simulation.PhysicalEnvironment.ServiceArea import ServiceArea
'''Triggers a change of user activity in a service area'''
class UserActivityEvent(object):
    
    @staticmethod
    def generateEvent(currentTime, serviceArea):
        delayConfig = CONFIG.eventConfig.activityDelayRange
        delay = CONFIG.randoms.activityDelay.randint(delayConfig[0], delayConfig[1])
        eventTime = currentTime + delay
        return UserActivityEvent(eventTime, serviceArea)
        
        
    def __init__(self, t, area : ServiceArea) -> None:
        self.t = t
        self.area = area
        self.generateFollowUp = True        
        
    def trigger(self):
        modifier = 0.9 + CONFIG.randoms.activitySimulation.random()*0.2
        self.area.ChangeActivity(modifier)