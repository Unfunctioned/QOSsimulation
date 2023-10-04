'''Used to represent the service requirements in different service areas'''
class ServiceRequirement(object):
    
    def __init__(self, capacity, latency, reliability, creationTime) -> None:
        self.defaultCapacityDemand = capacity
        self.latency = latency
        #A value between 0.0 and 1.0 representing a percentage how available the network service must be
        self.reliability = reliability
        self.accumulatedViolationTime = 0
        self.lastUpdateTime = creationTime
        
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