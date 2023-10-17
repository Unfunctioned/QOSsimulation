from Simulation.NetworkEnvironment.NetworkSlice import NetworkSlice
from Simulation.BusinessEnvironment.BusinessProcess import BusinessProcess
from Configuration.globals import GetConfig
from DataOutput.BasicDataRecorder import BasicDataRecorder
from Simulation.BusinessEnvironment.ActivityType import ActivityType
from Simulation.BusinessEnvironment.BusinessProcessFactory import BuisnessProcessFactory
from DataOutput.TimeDataRecorder import TimeDataRecorder
'''Defines a company entity. Companies execute mobile business processes in the simulation'''
class Company(object):
    
    def __init__(self, id, location, businessProcessFlow : list[ActivityType],
                 activityExecutionHistory : TimeDataRecorder) -> None:
        self.folderPath = None
        self.id = id
        self.location = location
        self.businessProcessFlow = businessProcessFlow
        self.networkSlice = NetworkSlice(self.id, self.folderPath)
        self.businessProcessActivations = 0
        self.activityExecutionHistory = activityExecutionHistory
        self.businessActivityHistory = self._initializeBusinessActivityHistory()
        self.storeInfo()
        
    def _initializeBusinessActivityHistory(self):
        if GetConfig().appSettings.tracingEnabled:
            path = GetConfig().filePaths.companyPath
            self.folderPath = GetConfig().filePaths.createInstanceOutputFolder(path, "Company", id)
            history = TimeDataRecorder(self.id, ["PROCESS_ID", "EVENTTYPE"])
            history.createFileOutput(self.folderPath, "ActivityHistory")
            return history
        return None
        
    def ActivateBusinessProcess(self, currentTime):
        processId = str(self.id) + "-{activations}".format(activations = self.businessProcessActivations)
        businessProcessFlow = BuisnessProcessFactory.CreateBusinessActivities(processId, currentTime, self.location, self.businessProcessFlow, self.activityExecutionHistory)
        businessProcess = BusinessProcess(processId, businessProcessFlow, self.folderPath, self.businessActivityHistory)
        self.businessProcessActivations += 1
        businessProcess.Execute(currentTime, self.networkSlice)
        return businessProcess
    
    def storeInfo(self):
        if GetConfig().appSettings.tracingEnabled:
            companyInfo = BasicDataRecorder(self.id, ["ID", "LOCATION_ID"])
            companyInfo.createFileOutput(self.folderPath, "CompanyInfo")
            companyInfo.record((self.id, self.location.id))
            companyInfo.terminate()
    
    def terminate(self):
        self.businessActivityHistory.terminate()
        self.activityExecutionHistory.terminate()
        self.networkSlice.terminate()
        
        