from DataOutput.TimeDataRecorder import TimeDataRecorder
from Simulation.NetworkEnvironment.ViolationStatusType import ViolationStatusType
from Configuration.globals import GetConfig
'''Defines the class representing network slices in the simulation'''
class NetworkSlice(object):
    
    def __init__(self, companyId, folderPath) -> None:
        self.companyId = companyId
        self.ServiceAreaRequirements = dict()
        self.activeServiceAreas = set()
        self.violationHistory = self._initializeViolationHistory(folderPath)
            
    def _initializeViolationHistory(self, folderPath):
        if GetConfig().appSettings.tracingEnabled:
            violationHistory = TimeDataRecorder(self.companyId, ["ServiceArea", "ViolationStatusType"])
            violationHistory.createFileOutput(folderPath, "NetworkSlice")
            return violationHistory
        return None
        
    def addServiceRequirement(self, serviceArea, serviceRequirement):
        if not serviceArea in self.ServiceAreaRequirements:
            self.ServiceAreaRequirements[serviceArea] = set([serviceRequirement])
        else:
            self.ServiceAreaRequirements[serviceArea].add(serviceRequirement)
            
    def removeServiceRequirement(self, serviceArea, serviceRequirement):
        if serviceArea in self.ServiceAreaRequirements:
            self.ServiceAreaRequirements[serviceArea].remove(serviceRequirement)
            if len(self.ServiceAreaRequirements[serviceArea]) == 0:
                self.ServiceAreaRequirements.pop(serviceArea)
                          
    def hasActiveRequirements(self, serviceArea):
        if serviceArea in self.ServiceAreaRequirements:
            return True
        return False
    
    def GetServiceRequirement(self, serviceArea):
        if serviceArea in self.ServiceAreaRequirements:
            return self.ServiceAreaRequirements[serviceArea]
        raise KeyError("No requirements for given service area exist")
    
    def UpdateViolationStatus(self, currentTime, serviceAreaID, violationType : ViolationStatusType):
        if not self.violationHistory is None:
            self.violationHistory.record(currentTime, [serviceAreaID, violationType.value[0]])
        
    def terminate(self):
        self.violationHistory.terminate()