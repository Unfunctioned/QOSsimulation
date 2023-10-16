from Simulation.NetworkEnvironment.ViolationStatusType import ViolationStatusType
from Configuration.globals import GetConfig


'''Used to represent the service requirements in different service areas'''
class ServiceRequirement(object):
    
    @staticmethod
    def GenerateDefaultRequirements(currentTime):
        capacity = GetConfig().serviceConfig.CAPACITY_DEFAULT
        latency = GetConfig().serviceConfig.LATENCY_DEFAULT
        reliability = GetConfig().serviceConfig.RELIABILITY_DEFAULT
        return ServiceRequirement(capacity, latency, reliability, currentTime)
    
    def __init__(self, capacity, latency, reliability, creationTime) -> None:
        self.defaultCapacityDemand = capacity
        self.latency = latency
        #A value between 0.0 and 1.0 representing a percentage how available the network service must be
        self.reliability = reliability
        self.totalViolationTime = 0
        self.latencyViolationTime = 0
        self.capacityViolationTime = 0
        self.lastUpdateTime = creationTime
        self.activeViolations = dict()
        
    def UpdateQoSStatus(self, currentTime, serviceAreaId : int, violationType : ViolationStatusType):
        if serviceAreaId in self.activeViolations:                
            lastViolationType = self.activeViolations[serviceAreaId]
            violationTime = currentTime - self.lastUpdateTime
            if lastViolationType == ViolationStatusType.CAPACITY or lastViolationType == ViolationStatusType.PARTIAL_CAPACITY:
                self.capacityViolationTime = violationTime
            else:
                self.latencyViolationTime = violationTime
            match violationType:
                case ViolationStatusType.RECOVERY:
                    self.activeViolations.pop(serviceAreaId)
            self.totalViolationTime += currentTime - self.lastUpdateTime
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