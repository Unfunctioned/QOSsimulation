from Configuration.globals import CONFIG
from DataOutput.TimeDataRecorder import TimeDataRecorder
from Simulation.NetworkEnvironment.NetworkSliceManager import NetworkSliceManager
from Simulation.NetworkEnvironment.PublicSlice import PublicSlice
from Simulation.NetworkEnvironment.ViolationType import ViolationType
from Simulation.NetworkEnvironment.ActivationType import ActivationType
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
        
    def UpdateActivity(self, currentTime, basicUserCount):
        self.basicUsers = basicUserCount
        serviceRequirements = self.publicSlice.GetServiceAreaRequirements(self.serviceArea)
        if not len(serviceRequirements) == 1:
            raise ValueError("Invalid requirements")
        list(serviceRequirements)[0].UpdateUsers(basicUserCount)

        #Baseline capacity update
        #Calculate the demand of private network slices (belonging to companies)
        privateDemand = self.sliceManager.GetPrivateDemand(self.serviceArea)
        (minDemand, maxDemand) = self.sliceManager.GetPublicDemandRange(self.serviceArea, self.publicSlice)
        if(self.totalTrafficCapacity < privateDemand + minDemand):
            excessDemand = privateDemand - (self.totalTrafficCapacity - minDemand)
            #Record Capacity violation for slices, whose capcity demand cannot be met
            violatedSlices = self.sliceManager.FindViolatedSlices(self.serviceArea, excessDemand)
            for networkSlice in violatedSlices:
                print("QoS Violation! {id}".format(id = networkSlice.companyId))
                networkSlice.AddViolation(currentTime, self.serviceArea.id, ViolationType.CAPACITY)
        self.MaxDataRatePerUser = self.totalTrafficCapacity / max(1, self.basicUsers)
        self.networkCapacityHistory.record(currentTime, [self.totalTrafficCapacity, self.MaxDataRatePerUser])
        
    def UpdateLatency(self, currentTime, modifier):
        self.latency = self._defaultLatency * modifier
        self.networkQualityHistory.record(currentTime, [self.latency])
        
    def ActivateNetworkSlice(self, currentTime, networkSlice):
        self.sliceManager.addNetworkSlice(currentTime, networkSlice)
        self.sliceActivationHistory.record(currentTime, [networkSlice.companyId, ActivationType.ACTIVATION.value[0]])
        
    def DeactivateNetworkSlice(self, currentTime, networkSlice):
        self.sliceManager.removeNetworkSlice(networkSlice)
        self.sliceActivationHistory.record(currentTime, [networkSlice.companyId, ActivationType.DEACTIVATION.value[0]])
        
    def terminate(self):
        self.networkCapacityHistory.terminate()
        self.networkQualityHistory.terminate()
        self.sliceActivationHistory.terminate()
        