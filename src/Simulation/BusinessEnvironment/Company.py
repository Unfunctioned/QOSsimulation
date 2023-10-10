from Simulation.NetworkEnvironment.NetworkSlice import NetworkSlice
from Simulation.BusinessEnvironment.BusinessProcess import BusinessProcess
from Configuration.globals import CONFIG
from DataOutput.BasicDataRecorder import BasicDataRecorder
from Simulation.BusinessEnvironment.ActivityType import ActivityType
from Simulation.BusinessEnvironment.BusinessProcessFactory import BuisnessProcessFactory
from DataOutput.TimeDataRecorder import TimeDataRecorder
'''Defines a company entity. Companies execute mobile business processes in the simulation'''
class Company(object):
    
    def __init__(self, id, location, businessProcessFlow : list[ActivityType],
                 activityExecutionHistory : TimeDataRecorder) -> None:
        path = CONFIG.filePaths.companyPath
        self.folderPath = CONFIG.filePaths.createInstanceOutputFolder(path, "Company", id)
        self.id = id
        self.location = location
        self.businessProcessFlow = businessProcessFlow
        self.networkSlice = NetworkSlice(self.id, self.folderPath)
        self.businessProcessActivations = 0
        self.businessActivityHistory = TimeDataRecorder(self.id, 2, ["PROCESS_ID", "EVENTTYPE"])
        self.businessActivityHistory.createFileOutput(self.folderPath, "ActivityHistory")
        self.activityExecutionHistory = activityExecutionHistory
        companyInfo = BasicDataRecorder(self.id, 2, ["ID", "LOCATION_ID"])
        companyInfo.createFileOutput(self.folderPath, "CompanyInfo")
        companyInfo.record((self.id, self.location.id))
        companyInfo.terminate()
        
    def ActivateBusinessProcess(self, currentTime):
        processId = str(self.id) + "-{activations}".format(activations = self.businessProcessActivations)
        businessProcessFlow = BuisnessProcessFactory.CreateBusinessActivities(processId, currentTime, self.location, self.businessProcessFlow, self.activityExecutionHistory)
        businessProcess = BusinessProcess(processId, businessProcessFlow, self.folderPath, self.businessActivityHistory)
        self.businessProcessActivations += 1
        businessProcess.Execute(currentTime, self.networkSlice)
        return businessProcess
        
        