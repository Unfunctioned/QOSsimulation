from Simulation.NetworkEnvironment.ServiceRequirements.ServiceRequirement import ServiceRequirement
from Simulation.PhysicalEnvironment.ServiceArea import ServiceArea
from Simulation.NetworkEnvironment.NetworkSlice import NetworkSlice

'''Represents a business activity of a business process'''
class BusinessActivity(object):
    
    def __init__(self, expectedDuration) -> None:
        self.serviceRequirement = ServiceRequirement(10, 8, 0.95, 0)
        self.expectedDuration = expectedDuration
        
    def activate(self):
        pass
    
    def deactivate(self):
        pass
        
        
class AreaBasedActivity(BusinessActivity):
    
    def __init__(self, expectedDuration, serviceArea : ServiceArea) -> None:
        super().__init__(expectedDuration)
        self.location = serviceArea
        
    def activate(self, currentTime, networkSlice : NetworkSlice):
        self.serviceRequirement.lastUpdateTime = currentTime
        self.location.ActivateNetworkSlice(currentTime, networkSlice, self.serviceRequirement)
        
    def deactivate(self, currentTime, networkSlice : NetworkSlice):
        self.serviceRequirement.lastUpdateTime = currentTime
        self.location.DeactivateNetworkSlice(currentTime, networkSlice, self.serviceRequirement)
        
class PathBasedActivity(BusinessActivity):
    
    def __init__(self, startLocation, endLocation) -> None:
        expectedDuration = self.calculateExpectedDuration(startLocation, endLocation)
        super().__init__(expectedDuration)
        self.startLocation = startLocation
        self.endLocation = endLocation
        
    def calculateExpectedDuration(self, startLocation, endLocation):
        raise NotImplementedError()
        
        
class TrajectoryBasedActivity(PathBasedActivity):
    
    def __init__(self, movementPath) -> None:
        if(len(movementPath) < 2):
            raise ValueError("Invalid Path")
        super().__init__(movementPath[0], movementPath[-1])
        self.movementPath = movementPath
        