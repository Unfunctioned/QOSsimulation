from Simulation.NetworkEnvironment.NetworkSlice import NetworkSlice
from Simulation.BusinessEnvironment.BusinessProcess import BusinessProcess
from Configuration.globals import CONFIG
from DataOutput.BasicDataRecorder import BasicDataRecorder
from Simulation.BusinessEnvironment.ActivityType import ActivityType
from Simulation.BusinessEnvironment.BusinessProcessFactory import BuisnessProcessFactory
'''Defines a company entity. Companies execute mobile business processes in the simulation'''
class Company(object):
    
    def __init__(self, id, location, businessProcessFlow : list[ActivityType]) -> None:
        path = CONFIG.filePaths.companyPath
        self.folderPath = CONFIG.filePaths.createInstanceOutputFolder(path, "Company", id)
        self.id = id
        self.location = location
        self.businessProcessFlow = businessProcessFlow
        self.networkSlice = NetworkSlice(self.id, self.folderPath)
        self.businessProcessActivations = 0
        companyInfo = BasicDataRecorder(self.id, 2, ["ID", "LOCATION_ID"])
        companyInfo.createFileOutput(self.folderPath, "CompanyInfo")
        companyInfo.record((self.id, self.location.id))
        companyInfo.terminate()
        
    def ActivateBusinessProcess(self, currentTime):
        businessProcessFlow = BuisnessProcessFactory.CreateBusinessActivities(self.location, self.businessProcessFlow)
        businessProcess = BusinessProcess(str(self.id) + "-{activations}".format(activations = self.businessProcessActivations)
                                          , businessProcessFlow, self.folderPath)
        self.businessProcessActivations += 1
        businessProcess.Execute(currentTime, self.networkSlice)
        return businessProcess
        
        