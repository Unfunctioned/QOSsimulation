from Simulation.NetworkEnvironment.NetworkSlice import NetworkSlice
from Simulation.BusinessEnvironment.BusinessProcess import BusinessProcess
from Configuration.globals import CONFIG
from DataOutput.BasicDataRecorder import BasicDataRecorder
'''Defines a company entity. Companies execute mobile business processes in the simulation'''
class Company(object):
    
    def __init__(self, id, location) -> None:
        path = CONFIG.filePaths.companyPath
        folderPath = CONFIG.filePaths.createInstanceOutputFolder(path, "Company", id)
        self.id = id
        self.location = location
        self.businessProcess = BusinessProcess(self.id, self.location, folderPath)
        self.networkSlice = NetworkSlice(self.id, folderPath)
        companyInfo = BasicDataRecorder(self.id, 2, ["ID", "LOCATION_ID"])
        companyInfo.createFileOutput(folderPath, "CompanyInfo")
        companyInfo.record((self.id, self.location.id))
        companyInfo.terminate()
        
    def ActivateBusinessProcess(self, currentTime):
        self.businessProcess.Execute(currentTime, self.networkSlice)
        
        