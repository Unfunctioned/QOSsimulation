import os
from datetime import datetime
from Configuration.BaseConfig import BaseConfig
'''Configures file paths for data outputs'''
class FilePath(BaseConfig):
    
    def __init__(self) -> None:
        self.currentDirectory = os.getcwd()
        self.dateTime = datetime.now().strftime("%d-%m-%Y-%H-%M-%S")
        self.storagePath = os.path.join(self.currentDirectory, "Simulations")
        print(self.currentDirectory)
        if(not os.path.exists(self.storagePath)):
            os.mkdir(self.storagePath)
        self.simulationPath = os.path.join(self.storagePath, "Run-" + self.dateTime)
        if(not os.path.exists(self.simulationPath)):
            os.mkdir(self.simulationPath)
        self.serviceAreaPath = os.path.join(self.simulationPath, "ServiceAreas")
        if(not os.path.exists(self.serviceAreaPath)):
            os.mkdir(self.serviceAreaPath)
        self.localServiceNetworkPath = os.path.join(self.simulationPath, "LocalServiceNetworks")
        if(not os.path.exists(self.localServiceNetworkPath)):
            os.mkdir(self.localServiceNetworkPath)
        self.companyPath = os.path.join(self.simulationPath, "Companies")
        if(not os.path.exists(self.companyPath)):
            os.mkdir(self.companyPath)
        
    def jsonable(self):
        return self.__dict__
        
    def createInstanceOutputFolder(self, path, folderName, id):
        folderPath = os.path.join(path, folderName + "#" + str(id))
        os.mkdir(folderPath)
        return folderPath