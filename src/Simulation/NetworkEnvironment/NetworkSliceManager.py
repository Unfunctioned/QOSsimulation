from queue import PriorityQueue
from Simulation.NetworkEnvironment.ServiceRequirements.ServiceRequirement import ServiceRequirement, DynamicServiceRequirement
from Simulation.NetworkEnvironment.PublicSlice import PublicSlice
from Simulation.NetworkEnvironment.NetworkSlice import NetworkSlice
from Simulation.NetworkEnvironment.CapacityDemand import CapacityDemand
from Simulation.NetworkEnvironment.ViolationStatusType import ViolationStatusType
from DataOutput.TimeDataRecorder import TimeDataRecorder
import traceback
'''Class used to manage the active network slices in a local service network'''
class NetworkSliceManager(object):
    
    def __init__(self) -> None:
        self.activationKeys = PriorityQueue()
        self.keysToSlice = dict()
        self.sliceToKey = dict()
        
    def addNetworkSlice(self, activationTime, networkSlice):
        if not activationTime in self.activationKeys.queue:
            self.activationKeys.put(activationTime)
        if networkSlice in self.sliceToKey:
            self.removeNetworkSlice(networkSlice)
        if activationTime in self.keysToSlice:
            self.keysToSlice[activationTime].append(networkSlice)
        else:
            self.keysToSlice[activationTime] = [networkSlice]
        self.sliceToKey[networkSlice] = activationTime
            
    def removeNetworkSlice(self, networkSlice : NetworkSlice):
        key = self._getKey(networkSlice)
        self.sliceToKey.pop(networkSlice)
        if (len(self.keysToSlice[key]) == 1):
            self.keysToSlice.pop(key)
            self.activationKeys.queue.remove(key)
            return
        self.keysToSlice[key].remove(networkSlice)
        
    def _getKey(self, networkSlice : NetworkSlice):
        key = -1
        if not networkSlice in self.sliceToKey:
            raise ValueError("Given Network slice could not be found")
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
    
    def GetAllNetworkSlices(self) -> list[NetworkSlice]:
        return list(self.sliceToKey.keys())
    
    def FindCapacityViolations(self, serviceArea, excessDemand):
        violations = {}
        activationHistory = self.activationKeys.queue.copy()
        activationHistory.reverse()
        for key in activationHistory:
            networkSlices = self.keysToSlice[key]
            for networkSlice in networkSlices:
                serviceRequirements = networkSlice.GetServiceRequirement(serviceArea)
                sliceViolations = []
                for serviceRequirement in serviceRequirements:
                    if excessDemand > 0:
                        excessDemand -= serviceRequirement.defaultCapacityDemand
                        sliceViolations.append(serviceRequirement)
                if len(sliceViolations) > 0:
                    violations[networkSlice] = sliceViolations
        return violations
    
    def FindLatencyViolations(self, serviceArea, currentLatency):
        violations = {}
        for key in self.activationKeys.queue:
            networkSlices = self.keysToSlice[key]
            networkSlice : NetworkSlice
            sliceViolations = []
            for networkSlice in networkSlices:
                serviceRequirements = networkSlice.GetServiceRequirement(serviceArea)
                serviceRequirement : ServiceRequirement
                for serviceRequirement in serviceRequirements:
                    if (serviceRequirement.latency < currentLatency):
                        sliceViolations.append(serviceRequirement)
                if len(sliceViolations) > 0:
                    violations[networkSlice] = sliceViolations
        return violations
    
    def FindQoSViolations(self, serviceArea, latency, capacityDemand : CapacityDemand):
        violations = {}
        excessDemand = max(0, capacityDemand.private + capacityDemand.publicMinimum - capacityDemand.maximumCapacity)
        activationHistory = self.activationKeys.queue.copy()
        activationHistory.reverse()
        for key in activationHistory:
            networkSlices = self.keysToSlice[key]
            networkSlice : NetworkSlice
            for networkSlice in networkSlices:
                serviceRequirements = networkSlice.GetServiceRequirement(serviceArea)
                sliceViolations = []
                serviceRequirement : ServiceRequirement
                for serviceRequirement in serviceRequirements:
                    if excessDemand > 0:
                        excessDemand -= serviceRequirement.defaultCapacityDemand
                        sliceViolations.append((serviceRequirement, ViolationStatusType.CAPACITY))
                        continue
                    if serviceRequirement.latency is None:
                        continue
                    if serviceRequirement.latency < latency:
                        sliceViolations.append((serviceRequirement, ViolationStatusType.LATENCY))
                if(len(sliceViolations) > 0):
                    violations[networkSlice] = sliceViolations
        return violations
                
            