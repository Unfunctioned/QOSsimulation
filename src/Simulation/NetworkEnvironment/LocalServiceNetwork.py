from Configuration.globals import GetConfig
from DataOutput.TimeDataRecorder import TimeDataRecorder
from Simulation.NetworkEnvironment.NetworkSliceManager import NetworkSliceManager
from Simulation.NetworkEnvironment.PublicSlice import PublicSlice
from Simulation.NetworkEnvironment.ViolationStatusType import ViolationStatusType
from Simulation.NetworkEnvironment.ActivationType import ActivationType
from Simulation.NetworkEnvironment.NetworkSlice import NetworkSlice
from Simulation.NetworkEnvironment.ServiceRequirements.ServiceRequirement import ServiceRequirement
from Simulation.NetworkEnvironment.CapacityDemand import CapacityDemand
from Simulation.NetworkEnvironment.NetworkSlice import NetworkSlice
from pathlib import Path

'''Represents the local service network providing services in a service area'''
class LocalServiceNetwork(object):
    
    @staticmethod
    def InitializeOutputFolder(id):
        path = GetConfig().filePaths.localServiceNetworkPath
        folderPath = GetConfig().filePaths.createInstanceOutputFolder(path, "LocalServiceNetwork", id)
        return folderPath
    
    def __init__(self, serviceAreaId : int, folderPath : Path, trafficCapacity, publicSlice : PublicSlice) -> None:
        self.serviceAreaId = serviceAreaId
        self.totalTrafficCapacity = trafficCapacity
        # Amount of non-MBP network users active in the area
        self.basicUsers = 0
        #For equally distributed data rates
        self.MaxDataRatePerUser = self.totalTrafficCapacity / max(1, self.basicUsers)
        #Default network Latency in ms
        self._defaultLatency = GetConfig().simConfig.DEFAULT_LATENCY
        #Current network latency
        self.latency = self._defaultLatency
        #Latency induced by network spikes
        self.spikeLatency = 0
        #Network slices operating in the network
        self.publicSlice = publicSlice
        self.sliceManager = NetworkSliceManager()
        # Inititalize recording of network capacity changes
        self.networkCapacityHistory = TimeDataRecorder(serviceAreaId, ["TotalCapacity", "MaxDataRate"])
        self.networkCapacityHistory.createFileOutput(folderPath, "CapacityHistory")
        self.networkCapacityHistory.record(0, [self.totalTrafficCapacity, self.MaxDataRatePerUser])
        #Initialize recording of network quality changes
        self.networkQualityHistory = TimeDataRecorder(serviceAreaId, ["Latency"])
        self.networkQualityHistory.createFileOutput(folderPath, "QualityHistory")
        self.networkQualityHistory.record(0, [self.latency])
        #Initialize slice activation history
        self.sliceActivationHistory = TimeDataRecorder(serviceAreaId, ["CompanyID", "ActivationType"])
        self.sliceActivationHistory.createFileOutput(folderPath, "SliceActivationHistory")
        #Network Slices with, whose service requirements were violated in the last activity update
        self.activeSliceViolations = dict()
        #Last update time
        self.lastUpdateTime = 0
                
    def UpdateActivity(self, currentTime, basicUserCount):
        self.basicUsers = basicUserCount
        capacityDemand = self.GetCurrentDemand()
        serviceRequirements = self.publicSlice.GetServiceAreaRequirements(self.serviceAreaId)
        if not len(serviceRequirements) == 1:
            raise ValueError("Invalid requirements")
        requirement = list(serviceRequirements)[0]
        requirement.UpdateUsers(basicUserCount)

        #Baseline QoS Validation
        violations : dict[NetworkSlice, list[tuple[ServiceRequirement, ViolationStatusType]]]
        violations, adjustedDemand = self.sliceManager.FindQoSViolations(self.serviceAreaId, self.latency, capacityDemand)
        self.UpdateRecoveredQoSRequirements(currentTime, violations)
        self.UpdateViolatedQoSRequirements(currentTime, violations)
        self.activeSliceViolations = violations
        self.MaxDataRatePerUser = (self.totalTrafficCapacity - adjustedDemand.private) / max(1,self.basicUsers)
        self.networkCapacityHistory.record(currentTime, [self.totalTrafficCapacity, self.MaxDataRatePerUser])
        self.lastUpdateTime = currentTime
        
    def UpdateRecoveredQoSRequirements(self, currentTime, currentViolations):        
        networkSlice : NetworkSlice
        for networkSlice in self.activeSliceViolations:
            if(not networkSlice in currentViolations):
                networkSlice.UpdateViolationStatus(currentTime, self.serviceAreaId, ViolationStatusType.RECOVERY)
            activeViolations = self.activeSliceViolations[networkSlice]
            serviceRequirement : ServiceRequirement
            for (serviceRequirement, _) in activeViolations:
                if(not networkSlice in currentViolations):
                    serviceRequirement.UpdateQoSStatus(currentTime, self.serviceAreaId, ViolationStatusType.RECOVERY)
                    continue
                violatedRequirements = currentViolations[networkSlice]
                if filter(lambda x,_ : x == serviceRequirement, violatedRequirements) == []:
                    serviceRequirement.UpdateQoSStatus(currentTime, self.serviceAreaId, ViolationStatusType.RECOVERY)
                    
    def UpdateViolatedQoSRequirements(self, currentTime, currentViolations):
        networkSlice : NetworkSlice
        for networkSlice in currentViolations:
            serviceRequirement : ServiceRequirement
            violationType : ViolationStatusType
            hasCapacityViolation = False
            for (serviceRequirement, violationType) in currentViolations[networkSlice]:
                if violationType == ViolationStatusType.CAPACITY:
                    hasCapacityViolation = True
                serviceRequirement.UpdateQoSStatus(currentTime, self.serviceAreaId, violationType)
            violationType = ViolationStatusType.CAPACITY if hasCapacityViolation else ViolationStatusType.LATENCY
            networkSlice.UpdateViolationStatus(currentTime, self.serviceAreaId, violationType)
            
    def GetCurrentDemand(self):
        privateDemand = self.sliceManager.GetPrivateDemand(self.serviceAreaId)
        (minDemand, maxDemand) = self.sliceManager.GetPublicDemandRange(self.serviceAreaId, self.publicSlice)
        return CapacityDemand(privateDemand, minDemand, maxDemand, self.totalTrafficCapacity)
        
    def UpdateLatency(self, currentTime, modifier, spikeValue = 0):
        self.latency = self._defaultLatency * modifier + spikeValue
        if self.latency > 20:
            raise ValueError("Latency is going out of control")
        self.networkQualityHistory.record(currentTime, [self.latency])
        
    def ActivateNetworkSlice(self, currentTime, networkSlice : NetworkSlice):
        self.sliceManager.addNetworkSlice(currentTime, networkSlice)
        self.sliceActivationHistory.record(currentTime, [networkSlice.companyId, ActivationType.ACTIVATION])
        self.UpdateActivity(currentTime, self.basicUsers)
        
    def DeactivateNetworkSlice(self, currentTime, networkSlice : NetworkSlice):
        self.sliceManager.removeNetworkSlice(networkSlice)
        self.sliceActivationHistory.record(currentTime, [networkSlice.companyId, ActivationType.DEACTIVATION])
        self.UpdateActivity(currentTime, self.basicUsers)
        
    def terminate(self):
        self.networkCapacityHistory.terminate()
        self.networkQualityHistory.terminate()
        self.sliceActivationHistory.terminate()
        self.serviceArea = None
        