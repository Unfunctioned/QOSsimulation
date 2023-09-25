from Configuration.globals import CONFIG
from DataOutput.DataRecorder import DataRecorder
'''Represents the local service network providing services in a service area'''
class LocalServiceNetwork(object):
    
    def __init__(self, id, areaSize, areaType) -> None:
        self.totalTrafficCapacity = areaSize * CONFIG.simConfig.get_traffic_capacity(areaType)
        # Amount of non-MBP network users active in the area
        self.basicUsers = 0
        self.availableTrafficCapacity = self.totalTrafficCapacity
        self.utilization = 1 - (self.availableTrafficCapacity / self.totalTrafficCapacity)
        #For equally distributed data rates
        self.MaxDataRatePerUser = self.totalTrafficCapacity / max(1, self.basicUsers)
        self.networkCapacityHistory = DataRecorder(id, 3, ["TotalCapacity", "AvailableCapacity", "Utilization", "MaxDataRate"])
        self.networkCapacityHistory.createFileOutput(CONFIG.filePaths.localServiceNetworkPath, "LocalServiceNetwork")
        self.networkCapacityHistory.record(0, [self.totalTrafficCapacity, self.availableTrafficCapacity, self.utilization, self.MaxDataRatePerUser])
        
    def UpdateActivity(self, currentTime, basicUserCount):
        self.basicUsers = basicUserCount
        basicUserDemand = self.basicUsers * CONFIG.simConfig.BASIC_DATA_RATE_DEMAND
        self.availableTrafficCapacity = self.totalTrafficCapacity - basicUserDemand
        self.utilization = 1 - (self.availableTrafficCapacity / self.totalTrafficCapacity)
        self.MaxDataRatePerUser = self.totalTrafficCapacity / max(1, self.basicUsers)
        self.networkCapacityHistory.record(currentTime, [self.totalTrafficCapacity, self.availableTrafficCapacity, self.utilization, self.MaxDataRatePerUser])
        