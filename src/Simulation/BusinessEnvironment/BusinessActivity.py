from Simulation.NetworkEnvironment.ServiceRequirements.ServiceRequirement import ServiceRequirement
from Simulation.PhysicalEnvironment.ServiceArea import ServiceArea
from Simulation.NetworkEnvironment.NetworkSlice import NetworkSlice
from Utilities.PathGenerator import PathGenerator
from Configuration.globals import CONFIG
from DataOutput.TimeDataRecorder import TimeDataRecorder

'''Represents a business activity of a business process'''
class BusinessActivity(object):
    
    def __init__(self, processId, currentTime, expectedDuration, executionHistory : TimeDataRecorder) -> None:
        self.processId = processId
        self.serviceRequirement = ServiceRequirement.GenerateDefaultRequirements(currentTime)
        self.expectedDuration = expectedDuration
        self.activationTime = -1
        self.executionHistory = executionHistory
        
    def activate(self, currentTime, networkSlice : NetworkSlice):
        self.activationTime = currentTime
        self.executionHistory.record(currentTime, [self.processId, "ACTIVATION"])
    
    def deactivate(self, currentTime, networkSlice : NetworkSlice):
        result = "SUCCESS"
        if self.IsInvalid(currentTime):
            result = "FAILURE"
        self.executionHistory.record(currentTime, [self.processId,"TERMINATION({r})".format(r = result)])
        
    def IsInvalid(self, terminationTime) -> bool:
        requiredReliability = self.serviceRequirement.reliability
        toleratedFailureTime = (terminationTime - self.activationTime) * requiredReliability
        actualFailureTime = self.serviceRequirement.accumulatedViolationTime
        if (actualFailureTime > toleratedFailureTime):
            return True
        return False
        
        
class AreaBasedActivity(BusinessActivity):
    
    def __init__(self, processId, currentTime, history : TimeDataRecorder, expectedDuration, serviceArea : ServiceArea) -> None:
        super().__init__(processId, currentTime, expectedDuration, history)
        self.location = serviceArea
        
    def activate(self, currentTime, networkSlice : NetworkSlice):
        super().activate(currentTime, networkSlice)
        self.serviceRequirement.lastUpdateTime = currentTime
        self.location.ActivateNetworkSlice(currentTime, networkSlice, self.serviceRequirement)
        
    def deactivate(self, currentTime, networkSlice : NetworkSlice):
        super().deactivate(currentTime, networkSlice)
        self.serviceRequirement.lastUpdateTime = currentTime
        self.location.DeactivateNetworkSlice(currentTime, networkSlice, self.serviceRequirement)
        
class PathBasedActivity(BusinessActivity):
    
    def __init__(self, processId, currentTime, history : TimeDataRecorder, startLocation, endLocation) -> None:
        movementPath = PathGenerator.GenerateShortestPath(startLocation, endLocation)
        if(len(movementPath) < 2):
            raise ValueError("Invalid Path")
        expectedDuration = PathGenerator.calculateExpectedDuration(movementPath) 
        super().__init__(processId, currentTime, expectedDuration, history)
        self.movementPath = movementPath
        self.startLocation : ServiceArea
        self.startLocation = startLocation
        self.endLocation : ServiceArea
        self.endLocation = endLocation
        self.dynamicPath = True
        self.currentPosition = 0
        
    def activate(self, currentTime, networkSlice : NetworkSlice):
        super().activate(currentTime, networkSlice)
        self.serviceRequirement.lastUpdateTime = currentTime
        self.startLocation.ActivateNetworkSlice(currentTime, networkSlice, self.serviceRequirement)
        
    def deactivate(self, currentTime, networkSlice : NetworkSlice):
        super().deactivate(currentTime, networkSlice)
        self.serviceRequirement.lastUpdateTime = currentTime
        self.endLocation.DeactivateNetworkSlice(currentTime, networkSlice, self.serviceRequirement)
        
class TrajectoryBasedActivity(PathBasedActivity):
    
    def __init__(self, processId, currentTime, history : TimeDataRecorder, startLocation : ServiceArea, endLocation : ServiceArea) -> None:
        super().__init__(processId, currentTime, history, startLocation, endLocation)
        self.dynamicPath = False
        
        