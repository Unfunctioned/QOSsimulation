from Configuration.globals import CONFIG
from DataOutput.TimeDataRecorder import TimeDataRecorder
from Simulation.NetworkEnvironment.NetworkSliceManager import NetworkSliceManager
from Simulation.NetworkEnvironment.PublicSlice import PublicSlice
from Simulation.NetworkEnvironment.ViolationStatusType import ViolationStatusType
from Simulation.NetworkEnvironment.ActivationType import ActivationType
from Simulation.NetworkEnvironment.NetworkSlice import NetworkSlice
from Simulation.NetworkEnvironment.ServiceRequirements.ServiceRequirement import ServiceRequirement
from Simulation.NetworkEnvironment.CapacityDemand import CapacityDemand
'''Represents the local service network providing services in a service area'''
class LocalServiceNetwork(object):
    
    @staticmethod
    def InitializeOutputFolder(id):
        path = CONFIG.filePaths.localServiceNetworkPath
        folderPath = CONFIG.filePaths.createInstanceOutputFolder(path, "LocalServiceNetwork", id)
        return folderPath
    
    def __init__(self, serviceArea, folderPath, trafficCapacity, publicSlice : PublicSlice) -> None:
        self.serviceArea = serviceArea
        self.totalTrafficCapacity = trafficCapacity
        # Amount of non-MBP network users active in the area
        self.basicUsers = 0
        #For equally distributed data rates
        self.MaxDataRatePerUser = self.totalTrafficCapacity / max(1, self.basicUsers)
        #Default network Latency in ms
        self._defaultLatency = CONFIG.simConfig.DEFAULT_LATENCY
        #Current network latency
        self.latency = self._defaultLatency
        #Latency induced by network spikes
        self.spikeLatency = 0
        #Network slices operating in the network
        self.publicSlice = publicSlice
        self.sliceManager = NetworkSliceManager()
        # Inititalize recording of network capacity changes
        self.networkCapacityHistory = TimeDataRecorder(serviceArea.id, 2, ["TotalCapacity", "MaxDataRate"])
        self.networkCapacityHistory.createFileOutput(folderPath, "CapacityHistory")
        self.networkCapacityHistory.record(0, [self.totalTrafficCapacity, self.MaxDataRatePerUser])
        #Initialize recording of network quality changes
        self.networkQualityHistory = TimeDataRecorder(serviceArea.id, 1, ["Latency"])
        self.networkQualityHistory.createFileOutput(folderPath, "QualityHistory")
        self.networkQualityHistory.record(0, [self.latency])
        #Initialize slice activation history
        self.sliceActivationHistory = TimeDataRecorder(serviceArea.id, 2, ["CompanyID", "ActivationType"])
        self.sliceActivationHistory.createFileOutput(folderPath, "SliceActivationHistory")
        #Network Slices with, whose service requirements were violated in the last activity update
        self.activeSliceViolations = dict()
        #Last update time
        self.lastUpdateTime = 0
                
    def UpdateActivity(self, currentTime, basicUserCount):
        self.basicUsers = basicUserCount
        capacityDemand = self.GetCurrentDemand()
        serviceRequirements = self.publicSlice.GetServiceAreaRequirements(self.serviceArea)
        if not len(serviceRequirements) == 1:
            raise ValueError("Invalid requirements")
        requirement = list(serviceRequirements)[0]
        requirement.UpdateUsers(basicUserCount)

        #Baseline QoS Validation
        violations : dict[NetworkSlice, list[tuple[ServiceRequirement, ViolationStatusType]]]
        violations = self.sliceManager.FindQoSViolations(self.serviceArea, self.latency, capacityDemand)
        self.UpdateRecoveredQoSRequirements(currentTime, violations)
        self.UpdateViolatedQoSRequirements(currentTime, violations)
        self.activeSliceViolations = violations
        
        self.networkCapacityHistory.record(currentTime, [self.totalTrafficCapacity, self.MaxDataRatePerUser])
        self.lastUpdateTime = currentTime
        #latencyViolations = self.FindAndValidateLatencyRequirements()
        
    def UpdateRecoveredQoSRequirements(self, currentTime, currentViolations):        
        networkSlice : NetworkSlice
        for networkSlice in self.activeSliceViolations:
            if(not networkSlice in currentViolations):
                networkSlice.UpdateViolationStatus(currentTime, self.serviceArea.id, ViolationStatusType.RECOVERY)
            activeViolations = self.activeSliceViolations[networkSlice]
            serviceRequirement : ServiceRequirement
            for (serviceRequirement, _) in activeViolations:
                if(not networkSlice in currentViolations):
                    serviceRequirement.UpdateQoSStatus(currentTime, self.serviceArea.id, ViolationStatusType.RECOVERY)
                    continue
                violatedRequirements = currentViolations[networkSlice]
                if filter(lambda x,_ : x == serviceRequirement, violatedRequirements) == []:
                    serviceRequirement.UpdateQoSStatus(currentTime, self.serviceArea.id, ViolationStatusType.RECOVERY)
                    
    def UpdateViolatedQoSRequirements(self, currentTime, currentViolations):
        networkSlice : NetworkSlice
        for networkSlice in currentViolations:
            serviceRequirement : ServiceRequirement
            violationType : ViolationStatusType
            hasCapacityViolation = False
            for (serviceRequirement, violationType) in currentViolations[networkSlice]:
                if violationType == ViolationStatusType.CAPACITY:
                    hasCapacityViolation = True
                serviceRequirement.UpdateQoSStatus(currentTime, self.serviceArea.id, violationType)
            violationType = ViolationStatusType.CAPACITY if hasCapacityViolation else ViolationStatusType.LATENCY
            networkSlice.UpdateViolationStatus(currentTime, self.serviceArea.id, violationType)
                    
                
        
    def FindAndValidateCapacityRequirements(self, currentTime, privateDemand, minDemand):
        capacityViolations = self.GetCapacityViolations(privateDemand, minDemand)
        capacityRecoveries = []
        if not capacityViolations is None:
            capacityRecoveries = self.RegisterCapacityViolations(currentTime, capacityViolations)
            capacityRecoveries = self.UpdateAccumulatedViolationTime(currentTime, capacityViolations)
            self.currentCapacityViolations = capacityViolations.keys()
        return capacityRecoveries
    
    def FindAndValidateLatencyRequirements(self, currentTime):     
        latencyViolations = self.GetLatencyViolations()
        latencyRecoveries = []
        if not latencyViolations is None:
            latencyRecoveries = self.RegisterLatencyViolations(currentTime, latencyViolations)
            self.currentLatencyViolations = latencyViolations.keys()
        return latencyRecoveries
            
    
    def GetCapacityViolations(self, privateDemand, minDemand):
        if(self.totalTrafficCapacity < privateDemand + minDemand):
            excessDemand = privateDemand - (self.totalTrafficCapacity - minDemand)
            return self.sliceManager.FindCapacityViolations(self.serviceArea, excessDemand)
        return None
    
    def GetLatencyViolations(self):
        latencyViolations = self.sliceManager.FindLatencyViolations(self.serviceArea, self.latency)
        if (len(latencyViolations) > 0):
            return latencyViolations
        return None
            
    def GetCurrentDemand(self):
        privateDemand = self.sliceManager.GetPrivateDemand(self.serviceArea)
        (minDemand, maxDemand) = self.sliceManager.GetPublicDemandRange(self.serviceArea, self.publicSlice)
        return CapacityDemand(privateDemand, minDemand, maxDemand, self.totalTrafficCapacity)
        
    def RegisterCapacityViolations(self, currentTime, violations):
        for networkSlice in violations:
            print("Capacity QoS Violation! {id}".format(id = networkSlice.companyId))
            networkSlice.AddViolation(currentTime, self.serviceArea.id, ViolationStatusType.CAPACITY)
    
    def RegisterLatencyViolations(self, currentTime, violations):
        for networkSlice in violations:
            print("Latency QOS Violation {id}".format(id = networkSlice.companyId))
            networkSlice.AddViolation(currentTime, self.serviceArea.id, ViolationStatusType.LATENCY)
        
    def UpdateAccumulatedViolationTime(self, currentTime, violations : dict[NetworkSlice, ServiceRequirement]):
        serviceRecoveries = []
        for networkSlice in self.currentCapacityViolations:
            serviceRecovery = True
            if networkSlice in violations.keys():
                serviceRecovery = False
                serviceRequirements = networkSlice.GetServiceRequirement(self.serviceArea)
                violatedRequirements = violations[networkSlice]
                requirement : ServiceRequirement
                for requirement in serviceRequirements:
                    if (requirement in violatedRequirements and not requirement.lastUpdateTime == currentTime):
                        requirement.accumulatedViolationTime += currentTime - self.lastUpdateTime
                        requirement.lastUpdateTime = currentTime
                        serviceRecovery = False
            if serviceRecovery:
                   serviceRecoveries.append(networkSlice)
        return serviceRecoveries
        
    def UpdateLatency(self, currentTime, modifier, spikeValue = 0):
        self.latency = self._defaultLatency * modifier + spikeValue
        if self.latency > 20:
            raise ValueError("Latency is going out of control")
        self.networkQualityHistory.record(currentTime, [self.latency])
        
    def ActivateNetworkSlice(self, currentTime, networkSlice):
        self.sliceManager.addNetworkSlice(currentTime, networkSlice)
        self.sliceActivationHistory.record(currentTime, [networkSlice.companyId, ActivationType.ACTIVATION])
        self.UpdateActivity(currentTime, self.basicUsers)
        
    def DeactivateNetworkSlice(self, currentTime, networkSlice):
        self.sliceManager.removeNetworkSlice(networkSlice)
        self.sliceActivationHistory.record(currentTime, [networkSlice.companyId, ActivationType.DEACTIVATION])
        self.UpdateActivity(currentTime, self.basicUsers)
        
    def terminate(self):
        self.networkCapacityHistory.terminate()
        self.networkQualityHistory.terminate()
        self.sliceActivationHistory.terminate()
        