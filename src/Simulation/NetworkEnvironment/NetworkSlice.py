from DataOutput.TimeDataRecorder import TimeDataRecorder
from Simulation.NetworkEnvironment.ViolationStatusType import ViolationStatusType
from Simulation.NetworkEnvironment.ServiceRequirements.ServiceRequirement import ServiceRequirement
from Configuration.globals import GetConfig
'''Defines the class representing network slices in the simulation'''
class NetworkSlice(object):
    
    def __init__(self, companyId, folderPath) -> None:
        self.companyId = companyId
        self.ServiceAreaRequirements : dict[int, set[ServiceRequirement]]
        self.ServiceAreaRequirements = dict()
        self.activeServiceAreas = set()
        self.violationHistory = self._initializeViolationHistory(folderPath)
            
    def _initializeViolationHistory(self, folderPath):
        if GetConfig().appSettings.tracingEnabled:
            violationHistory = TimeDataRecorder(self.companyId, ["ServiceArea", "ViolationStatusType"])
            violationHistory.createFileOutput(folderPath, "NetworkSlice")
            return violationHistory
        return None
        
    def addServiceRequirement(self, serviceAreaId : int, serviceRequirement : ServiceRequirement):
        if not  serviceAreaId in self.ServiceAreaRequirements:
            self.ServiceAreaRequirements[serviceAreaId] = set([serviceRequirement])
        else:
            self.ServiceAreaRequirements[serviceAreaId].add(serviceRequirement)
            
    def removeServiceRequirement(self, serviceAreaId : int, serviceRequirement : ServiceRequirement):
        if serviceAreaId in self.ServiceAreaRequirements:
            self.ServiceAreaRequirements[serviceAreaId].remove(serviceRequirement)
            if len(self.ServiceAreaRequirements[serviceAreaId]) == 0:
                self.ServiceAreaRequirements.pop(serviceAreaId)
                          
    def hasActiveRequirements(self, serviceAreaId : int):
        if serviceAreaId in self.ServiceAreaRequirements:
            return True
        return False
    
    def GetServiceRequirement(self, serviceAreaId : int):
        if serviceAreaId in self.ServiceAreaRequirements:
            return self.ServiceAreaRequirements[serviceAreaId]
        raise KeyError("No requirements for given service area exist")
    
    def UpdateViolationStatus(self, currentTime : int, serviceAreaID : int, violationType : ViolationStatusType):
        if not self.violationHistory is None:
            self.violationHistory.record(currentTime, [serviceAreaID, violationType.value[0]])
        
    def terminate(self):
        self.violationHistory.terminate()