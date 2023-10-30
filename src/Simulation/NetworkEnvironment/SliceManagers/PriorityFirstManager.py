from Simulation.NetworkEnvironment.CapacityDemand import CapacityDemand
from Simulation.NetworkEnvironment.SliceManagers.NetworkSliceManager import NetworkSliceManager
from Simulation.NetworkEnvironment.NetworkSlice import NetworkSlice
from Simulation.NetworkEnvironment.PublicSlice import PublicSlice
from Simulation.NetworkEnvironment.ServiceRequirements.ServiceRequirement import ServiceRequirement, DynamicServiceRequirement
from Simulation.NetworkEnvironment.ViolationStatusType import ViolationStatusType

'''Network slice manager prioritizing network slices by slice activation time'''
class PriorityFirstManager(NetworkSliceManager):
    
    def __init__(self, serviceAreaId: int) -> None:
        super().__init__(serviceAreaId)
        self.keysToSlice : dict[int, list[NetworkSlice]]
        self.keysToSlice = dict()
        self.sliceToKey = dict()
        
    def addNetworkSlice(self, activationTime: int, networkSlice: NetworkSlice):
        if not activationTime in self.activationKeys.queue:
            self.activationKeys.put(activationTime)
        if networkSlice in self.sliceToKey:
            self.removeNetworkSlice(activationTime, networkSlice)
        if activationTime in self.keysToSlice:
            self.keysToSlice[activationTime].append(networkSlice)
        else:
            self.keysToSlice[activationTime] = [networkSlice]
        self.sliceToKey[networkSlice] = activationTime
        
    def removeNetworkSlice(self, _ : int, networkSlice: NetworkSlice):
        key = self._getKey(networkSlice)
        self.sliceToKey.pop(networkSlice)
        if (len(self.keysToSlice[key]) == 1):
            self.keysToSlice.pop(key)
            self.activationKeys.queue.remove(key)
            return
        self.keysToSlice[key].remove(networkSlice)
        
    def _getKey(self, networkSlice: NetworkSlice):
        if not networkSlice in self.sliceToKey:
            raise ValueError("Given Network slice could not be found")
        return self.sliceToKey[networkSlice]
    
    def GetPrivateDemand(self, currentTime: int):
        demand = 0
        for i in range(1, len(self.activationKeys.queue)):
            key = self.activationKeys.queue[i]
            if key > currentTime:
                continue
            networkSlices = self.keysToSlice[key]
            networkSlice : NetworkSlice
            for networkSlice in networkSlices:
                if (isinstance(networkSlice, PublicSlice)):
                    continue
                serviceRequirements = networkSlice.GetServiceRequirement(self.serviceAreaId)
                for serviceRequirement in serviceRequirements:
                    if(isinstance(serviceRequirement, DynamicServiceRequirement)):
                        raise ValueError("Invalid private slice")
                    if(isinstance(serviceRequirement, ServiceRequirement)):
                        demand += serviceRequirement.defaultCapacityDemand
        return demand
    
    def FindQoSViolations(self, currentTime: int, latency, capacityDemand: CapacityDemand):
        violations = {}
        adjustedDemand = CapacityDemand(0, capacityDemand.publicMinimum, 
                                        capacityDemand.publicMaximum, capacityDemand.maximumCapacity)
        excessDemand = max(0, capacityDemand.private + capacityDemand.publicMinimum - capacityDemand.maximumCapacity)
        activationHistory = self.activationKeys.queue.copy()
        activationHistory.reverse()
        for key in activationHistory:
            if key > currentTime:
                continue
            networkSlices = self.keysToSlice[key]
            networkSlice : NetworkSlice
            for networkSlice in networkSlices:
                serviceRequirements = networkSlice.GetServiceRequirement(self.serviceAreaId)
                sliceViolations = []
                serviceRequirement : ServiceRequirement
                for serviceRequirement in serviceRequirements:
                    if excessDemand > 0:
                        violationType = ViolationStatusType.CAPACITY
                        if excessDemand < serviceRequirement.defaultCapacityDemand:
                            violationType = ViolationStatusType.PARTIAL_CAPACITY
                            adjustedDemand.private += serviceRequirement.defaultCapacityDemand - excessDemand
                        excessDemand -= serviceRequirement.defaultCapacityDemand
                        sliceViolations.append((serviceRequirement, violationType))
                        continue
                    if serviceRequirement.latency is None:
                        continue
                    if serviceRequirement.latency < latency:
                        sliceViolations.append((serviceRequirement, ViolationStatusType.LATENCY))
                        adjustedDemand.private += serviceRequirement.defaultCapacityDemand
                if(len(sliceViolations) > 0):
                    violations[networkSlice] = sliceViolations
        return violations, adjustedDemand