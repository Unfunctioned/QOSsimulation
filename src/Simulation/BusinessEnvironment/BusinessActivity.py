from Simulation.NetworkEnvironment.ServiceRequirements.ServiceRequirement import ServiceRequirement
from Simulation.PhysicalEnvironment.ServiceArea import ServiceArea
from Simulation.NetworkEnvironment.NetworkSlice import NetworkSlice
from Utilities.PathGenerator import PathGenerator, GetPathGenerator
from Simulation.BusinessEnvironment.ActivityType import ActivityType
from DataOutput.TimeDataRecorder import TimeDataRecorder
from Simulation.NetworkEnvironment.ViolationStatusType import ViolationStatusType

'''Represents a business activity of a business process'''
class BusinessActivity(object):
    
    def __init__(self, processId, currentTime, expectedDuration : int, executionHistory : TimeDataRecorder) -> None:
        if not isinstance(expectedDuration, int):
            raise TypeError("Value should be of type int")
        self.processId = processId
        self.expectedDuration = expectedDuration
        self.serviceRequirement = ServiceRequirement.GenerateDefaultRequirements(currentTime, expectedDuration)
        self.activationTime = -1
        self.executionHistory = executionHistory
        self.totalTime = -1
        self.activityType = None
        self.activated = False
        
    def getTypeName(self):
        return self.activityType
        
    def activate(self, currentTime):
        self.activationTime = currentTime
        self.executionHistory.record(currentTime, [self.processId, "ACTIVATION", self.getTypeName(), -1, "N/A", -1, -1])
        self.activated = True
    
    def deactivate(self, currentTime):
        self.totalTime = currentTime - self.activationTime
        QoSrate = (self.totalTime - self.serviceRequirement.totalViolationTime) / self.totalTime
        result = "SUCCESS"
        cause = "N/A"
        if self.IsInvalid():
            result = "FAILURE"
            cause = ViolationStatusType.CAPACITY.name if self.serviceRequirement.capacityViolationTime > self.serviceRequirement.latencyViolationTime else ViolationStatusType.LATENCY.name
            
        self.executionHistory.record(currentTime, [self.processId,"TERMINATION({r})".format(r = result),
                                                   self.getTypeName(), QoSrate, cause, self.serviceRequirement.capacityViolationTime, self.serviceRequirement.latencyViolationTime])
        
    def IsInvalid(self) -> bool:
        requiredReliability = self.serviceRequirement.reliability
        toleratedFailureTime = self.totalTime * (1 - requiredReliability)
        actualFailureTime = self.serviceRequirement.totalViolationTime
        if (actualFailureTime > toleratedFailureTime):
            return True
        return False
        
        
class AreaBasedActivity(BusinessActivity):
    
    def __init__(self, processId, currentTime, history : TimeDataRecorder, expectedDuration, serviceArea : ServiceArea) -> None:
        super().__init__(processId, currentTime, expectedDuration, history)
        self.location = serviceArea
        self.activityType = ActivityType.AREA
        
    def getTypeName(self):
        return self.activityType.name
        
    def activate(self, currentTime, networkSlice : NetworkSlice):
        super().activate(currentTime)
        self.serviceRequirement.lastUpdateTime = currentTime
        network = self.location.GetLocalServiceNetwork()
        network.ActivateNetworkSlice(currentTime, networkSlice, self.serviceRequirement)
        
    def deactivate(self, currentTime, networkSlice : NetworkSlice):
        super().deactivate(currentTime)
        self.serviceRequirement.lastUpdateTime = currentTime
        network = self.location.GetLocalServiceNetwork()
        network.DeactivateNetworkSlice(currentTime, networkSlice, self.serviceRequirement)
        
class PathBasedActivity(BusinessActivity):
    
    def __init__(self, processId, currentTime, history : TimeDataRecorder, startLocation, endLocation) -> None:
        movementPath = GetPathGenerator().GenerateShortestPath(startLocation, endLocation)
        if(len(movementPath) < 2):
            raise ValueError("Invalid Path")
        expectedDuration = GetPathGenerator().calculateExpectedDuration(movementPath) 
        super().__init__(processId, currentTime, expectedDuration, history)
        self.movementPath = movementPath
        self.startLocation : ServiceArea
        self.startLocation = startLocation
        self.endLocation : ServiceArea
        self.endLocation = endLocation
        self.dynamicPath = True
        self.currentPosition = 0
        self.activityType = ActivityType.PATH
    
    def getTypeName(self):
        return self.activityType.name
        
    def activate(self, currentTime, networkSlice : NetworkSlice):
        super().activate(currentTime)
        self.serviceRequirement.lastUpdateTime = currentTime
        network = self.startLocation.GetLocalServiceNetwork()
        network.ActivateNetworkSlice(currentTime, networkSlice, self.serviceRequirement)
        
    def deactivate(self, currentTime, networkSlice : NetworkSlice):
        super().deactivate(currentTime)
        self.serviceRequirement.lastUpdateTime = currentTime
        network = self.endLocation.GetLocalServiceNetwork()
        network.DeactivateNetworkSlice(currentTime, networkSlice, self.serviceRequirement)
        
class TrajectoryBasedActivity(PathBasedActivity):
    
    def __init__(self, processId, currentTime, history : TimeDataRecorder, startLocation : ServiceArea, endLocation : ServiceArea) -> None:
        super().__init__(processId, currentTime, history, startLocation, endLocation)
        self.dynamicPath = False
        self.activityType = ActivityType.TRAJECTORY
        
        