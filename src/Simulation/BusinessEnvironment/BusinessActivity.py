from Simulation.NetworkEnvironment.ServiceRequirements.ServiceRequirement import ServiceRequirement
from Simulation.PhysicalEnvironment.ServiceArea import ServiceArea
from Simulation.NetworkEnvironment.NetworkSlice import NetworkSlice
from Utilities.PathGenerator import PathGenerator
from Configuration.globals import CONFIG

'''Represents a business activity of a business process'''
class BusinessActivity(object):
    
    def __init__(self, expectedDuration) -> None:
        self.serviceRequirement = ServiceRequirement(10, 8, 0.95, 0)
        self.expectedDuration = expectedDuration
        
    def activate(self, currentTime, networkSlice : NetworkSlice):
        raise AttributeError("Missing override method")
    
    def deactivate(self, currentTime, networkSlice):
        raise AttributeError("Missing override method")
        
        
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
        movementPath = PathGenerator.GenerateShortestPath(startLocation, endLocation)
        if(len(movementPath) < 2):
            raise ValueError("Invalid Path")
        expectedDuration = PathGenerator.calculateExpectedDuration(movementPath) 
        super().__init__(expectedDuration)
        self.movementPath = movementPath
        self.startLocation : ServiceArea
        self.startLocation = startLocation
        self.endLocation : ServiceArea
        self.endLocation = endLocation
        self.dynamicPath = True
        self.currentPosition = 0
        
    def activate(self, currentTime, networkSlice : NetworkSlice):
        self.serviceRequirement.lastUpdateTime = currentTime
        self.startLocation.ActivateNetworkSlice(currentTime, networkSlice, self.serviceRequirement)
        
    def deactivate(self, currentTime, networkSlice : NetworkSlice):
        self.serviceRequirement.lastUpdateTime = currentTime
        self.endLocation.DeactivateNetworkSlice(currentTime, networkSlice, self.serviceRequirement)
                
        
        
class TrajectoryBasedActivity(PathBasedActivity):
    
    def __init__(self, startLocation : ServiceArea, endLocation : ServiceArea) -> None:
        super().__init__(startLocation, endLocation)
        self.dynamicPath = False
        
        