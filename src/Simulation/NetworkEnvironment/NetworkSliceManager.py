from queue import PriorityQueue
from Simulation.NetworkEnvironment.ServiceRequirements.ServiceRequirement import ServiceRequirement, DynamicServiceRequirement
from Simulation.NetworkEnvironment.PublicSlice import PublicSlice
'''Class used to manage the active network slices in a local service network'''
class NetworkSliceManager(object):
    
    def __init__(self) -> None:
        self.activationKeys = PriorityQueue()
        self.keysToSlice = dict()
        self.sliceToKey = dict()
        
    def addNetworkSlice(self, activationTime, networkSlice):
        self.activationKeys.put(activationTime)
        if activationTime in self.keysToSlice:
            self.keysToSlice[activationTime].append(networkSlice)
        else:
            self.keysToSlice[activationTime] = [networkSlice]
        self.sliceToKey[networkSlice] = activationTime
            
    def removeNetworkSlice(self, networkSlice):
        key = self._getKey(networkSlice)
        self.sliceToKey.pop(networkSlice)
        if (len(self.keysToSlice[key]) == 1):
            self.keysToSlice.pop(key)
            return
        self.keysToSlice[key].remove(networkSlice)
        
    def _getKey(self, networkSlice):
        key = -1
        if not networkSlice in self.sliceToKey:
            raise ValueError("Given nNetwork slice could not be found")
        return self.sliceToKey[networkSlice]
    
    def GetPrivateDemand(self, serviceArea):
        demand = 0
        for i in range(1, len(self.activationKeys.queue)):
            key = self.activationKeys.queue[i]
            networkSlices = self.keysToSlice[key]
            for networkSlice in networkSlices:
                if (isinstance(networkSlice, PublicSlice)):
                    continue
                serviceRequirements = networkSlice.GetServiceRequirement(serviceArea)
                for serviceRequirement in serviceRequirements:
                    if(isinstance(serviceRequirement, DynamicServiceRequirement)):
                        raise ValueError("Invalid private slice")
                    if(isinstance(serviceRequirement, ServiceRequirement)):
                        demand += serviceRequirement.defaultCapacityDemand
        return demand
    
    def GetPublicDemandRange(self, serviceArea, publicSlice):
        serviceRequirements = list(publicSlice.GetServiceRequirement(serviceArea))
        if (not len(serviceRequirements) == 1):
            raise ValueError("Invalid public slice requirements")
        serviceRequirement = serviceRequirements[0]
        if (not isinstance(serviceRequirement, DynamicServiceRequirement)):
            raise TypeError("Wrong network slice")
        
        return serviceRequirement.defaultCapacityDemand, serviceRequirement.maxCapacityDemand
    
    def GetAllNetworkSlices(self):
        return list(self.sliceToKey.keys())