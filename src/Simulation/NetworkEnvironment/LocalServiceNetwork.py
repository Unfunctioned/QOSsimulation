from Configuration.globals import CONFIG
from DataOutput.TimeDataRecorder import TimeDataRecorder
from Simulation.NetworkEnvironment.NetworkSliceManager import NetworkSliceManager
from Simulation.NetworkEnvironment.PublicSlice import PublicSlice
from Simulation.NetworkEnvironment.ViolationStatusType import ViolationStatusType
from Simulation.NetworkEnvironment.ActivationType import ActivationType
from Simulation.NetworkEnvironment.NetworkSlice import NetworkSlice
from Simulation.NetworkEnvironment.ServiceRequirements.ServiceRequirement import ServiceRequirement
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
        self._defaultLatency = 10
        #Current network latency
        self.latency = self._defaultLatency
        #Network slices operating in the network
        self.publicSlice = publicSlice
        self.sliceManager = NetworkSliceManager()
        self.sliceManager.addNetworkSlice(0, publicSlice)
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
        #Network Slices with capacity violations in the last update
        self.currentCapacityViolations = []
        #Network Slices with latency violations in the last update
        self.currentLatencyViolations = []
        #Last update time
        self.lastUpdateTime = 0
                
    def UpdateActivity(self, currentTime, basicUserCount):
        self.basicUsers = basicUserCount
        privateDemand, minDemand = self.GetCurrentDemand()
        serviceRequirements = self.publicSlice.GetServiceAreaRequirements(self.serviceArea)
        if not len(serviceRequirements) == 1:
            raise ValueError("Invalid requirements")
        list(serviceRequirements)[0].UpdateUsers(basicUserCount)

        #Baseline capacity update
        #Calculate the demand of private network slices (belonging to companies)
        capacityRecoveries = self.FindAndValidateCapacityRequirements(currentTime, privateDemand, minDemand)
        self.MaxDataRatePerUser = self.publicSlice.GetMaxDataRate(self.serviceArea, self.totalTrafficCapacity - privateDemand)
        #self.MaxDataRatePerUser = self.totalTrafficCapacity / max(1, self.basicUsers)
        self.networkCapacityHistory.record(currentTime, [self.totalTrafficCapacity, self.MaxDataRatePerUser])
        
    def FindAndValidateCapacityRequirements(self, currentTime, privateDemand, minDemand):
        capacityViolations = self.GetCapacityViolations(privateDemand, minDemand)
        capacityRecoveries = []
        if not capacityViolations is None:
            capacityRecoveries = self.ValidateCapacityRequirements(currentTime, capacityViolations)
            self.currentCapacityViolations = capacityViolations.keys()
        return capacityRecoveries
            
        #latencyViolations = self.GetLatencyViolations()
        #latencyRecoveries = []
        #if not latencyViolations is None:
        #    latencyRecoveries = self.ValidateLatencyRequirements(currentTime, latencyViolations)
            
    
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
        (minDemand, _) = self.sliceManager.GetPublicDemandRange(self.serviceArea, self.publicSlice)
        return privateDemand, minDemand
        
    def ValidateCapacityRequirements(self, currentTime, violations):
        for networkSlice in violations:
            print("QoS Violation! {id}".format(id = networkSlice.companyId))
            networkSlice.AddViolation(currentTime, self.serviceArea.id, ViolationStatusType.CAPACITY)
        return self.UpdateAccumulatedViolationTime(currentTime, violations)
        
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
    
    def ValidateLatencyRequirements(self, currentTime, violations):
        serviceRecoveries = []
        for networkSlice in self.currentLatencyViolations:
            serviceRecovery = True
    #        if networkSlice in violations.keys():
        
    def UpdateLatency(self, currentTime, modifier):
        self.latency = self._defaultLatency * modifier
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
        