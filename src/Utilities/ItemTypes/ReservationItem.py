from Simulation.NetworkEnvironment.NetworkSlice import NetworkSlice
from Simulation.NetworkEnvironment.ServiceRequirements.ServiceRequirement import ServiceRequirement
'''Class used to represent network resource reservations in the SchedulingSliceManager'''
class ReservationItem(object):
    
    def __init__(self, activationTime : int, duration : int, networkSlice : NetworkSlice, serviceRequirement : ServiceRequirement) -> None:
        self.activationTime = activationTime
        self.duration = duration
        self.networkSlice = networkSlice
        self.serviceRequirement = serviceRequirement
        
    def GetDemand(self):
        return self.serviceRequirement.defaultCapacityDemand
    
    def __eq__(self, __value: object) -> bool:
        if not isinstance(__value, ReservationItem):
            return False
        if not self.duration == __value.duration:
            return False
        if not self.networkSlice == __value.networkSlice:
            return False
        return True
    
    def __hash__(self) -> int:
        return super().__hash__()