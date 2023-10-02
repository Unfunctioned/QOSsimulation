'''Used to represent the service requirements in different service areas'''
class ServiceRequirement(object):
    
    def __init__(self, capacity, latency) -> None:
        self.defaultCapacityDemand = capacity
        self.latency = latency
        
'''Used to define ServiceRequirements accept a range of tolerance wrt. to QoS'''
class DynamicServiceRequirement(ServiceRequirement):
    
    def __init__(self, userCapacities : (int, int), latency, users) -> None:
        self.users = users
        self.maxUserDemand = userCapacities[1]
        self.minUserDemand = userCapacities[0]
        self.maxCapacityDemand = self.users * self.maxUserDemand
        super().__init__(self.users * self.minUserDemand, latency)
        
    def UpdateUsers(self, newUserCount):
        self.users = newUserCount
        self.maxCapacityDemand = self.users * self.maxUserDemand
        self.defaultCapacityDemand = self.users * self.minUserDemand