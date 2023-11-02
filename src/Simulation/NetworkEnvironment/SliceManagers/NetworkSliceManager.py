from queue import PriorityQueue
from Simulation.NetworkEnvironment.PublicSlice import PublicSlice
from Simulation.NetworkEnvironment.NetworkSlice import NetworkSlice
from Simulation.NetworkEnvironment.CapacityDemand import CapacityDemand
from Simulation.NetworkEnvironment.ServiceRequirements.ServiceRequirement import ServiceRequirement
from Simulation.NetworkEnvironment.ViolationStatusType import ViolationStatusType

'''Class used to manage the active network slices in a local service network'''
class NetworkSliceManager(object):
    
    def __init__(self, serviceAreaId : int) -> None:
        self.activationKeys = PriorityQueue()
        self.serviceAreaId = serviceAreaId
        
    def addNetworkSlice(self, activationTime : int, networkSlice : NetworkSlice):
        raise AttributeError("Method needs to be overridden")
            
    def removeNetworkSlice(self, currentTime : int , networkSlice : NetworkSlice):
        raise AttributeError("Method needs to be overridden")
    
    def GetPrivateDemand(self, currentTime : int):
        raise AttributeError("Method needs to be overridden")
    
    def FindQoSViolations(self, currentTime : int, latency, capacityDemand : CapacityDemand) -> tuple[dict[NetworkSlice, list[tuple[ServiceRequirement, ViolationStatusType]]], CapacityDemand]:
        raise AttributeError("Method needs to be overridden")
                
            