import os
from datetime import datetime
'''Configures file paths for data outputs'''
class FilePath(object):
    
    def __init__(self) -> None:
        self.currentDirectory = os.getcwd()
        self.dateTime = datetime.now().strftime("%d-%m-%Y-%H-%M-%S")
        self.storagePath = os.path.join(self.currentDirectory, "Simulations")
        print(self.currentDirectory)
        if(not os.path.exists(self.storagePath)):
            os.mkdir(os.path.join(self.storagePath))
        self.simulationPath = os.path.join(self.storagePath, "Run-" + self.dateTime)
        os.mkdir(self.simulationPath)
        self.serviceAreaPath = os.path.join(self.simulationPath, "ServiceAreas")
        os.mkdir(self.serviceAreaPath)
        self.localServiceNetworkPath = os.path.join(self.simulationPath, "LocalServiceNetworks")
        os.mkdir(self.localServiceNetworkPath)
        self.companyPath = os.path.join(self.simulationPath, "Companies")
        os.mkdir(self.companyPath)
        
    def createInstanceOutputFolder(self, path, folderName, id):
        folderPath = os.path.join(path, folderName + "#" + str(id))
        os.mkdir(folderPath)
        return folderPath