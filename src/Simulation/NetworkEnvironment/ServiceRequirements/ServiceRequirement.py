from Simulation.NetworkEnvironment.ViolationStatusType import ViolationStatusType
from Configuration.globals import CONFIG


'''Used to represent the service requirements in different service areas'''
class ServiceRequirement(object):
    
    @staticmethod
    def GenerateDefaultRequirements(currentTime):
        capacity = CONFIG.serviceConfig.CAPACITY_DEFAULT
        latency = CONFIG.serviceConfig.LATENCY_DEFAULT
        reliability = CONFIG.serviceConfig.RELIABILITY_DEFAULT
        return ServiceRequirement(capacity, latency, reliability, currentTime)
    
    def __init__(self, capacity, latency, reliability, creationTime) -> None:
        self.defaultCapacityDemand = capacity
        self.latency = latency
        #A value between 0.0 and 1.0 representing a percentage how available the network service must be
        self.reliability = reliability
        self.accumulatedViolationTime = 0
        self.lastUpdateTime = creationTime
        self.activeViolations = dict()
        
    def UpdateQoSStatus(self, currentTime, serviceAreaId : int, violationType : ViolationStatusType):
        match violationType:
            case ViolationStatusType.RECOVERY:
                self.activeViolations.pop(serviceAreaId)
                self.accumulatedViolationTime += currentTime - self.lastUpdateTime
            case _ :
                if serviceAreaId in self.activeViolations:
                    self.accumulatedViolationTime += currentTime - self.lastUpdateTime
                self.activeViolations[serviceAreaId] = violationType
        self.lastUpdateTime = currentTime
        
        
'''Used to define ServiceRequirements accept a range of tolerance wrt. to QoS'''
class DynamicServiceRequirement(ServiceRequirement):
    
    def __init__(self, userCapacities : (int, int), latency, users, reliability, creationTime) -> None:
        self.users = users
        self.maxUserDemand = userCapacities[1]
        self.minUserDemand = userCapacities[0]
        self.maxCapacityDemand = self.users * self.maxUserDemand
        super().__init__(self.users * self.minUserDemand, latency, reliability, creationTime)
        
    def UpdateUsers(self, newUserCount):
        self.users = newUserCount
        self.maxCapacityDemand = self.users * self.maxUserDemand
        self.defaultCapacityDemand = self.users * self.minUserDemand