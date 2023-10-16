from pathlib import Path
from datetime import datetime
from Configuration.BaseConfig import BaseConfig
'''Configures file paths for data outputs'''
class FilePath(BaseConfig):
    
    def __init__(self) -> None:
        self.currentDirectory = Path().cwd()
        self.dateTime = datetime.now().strftime("%d-%m-%Y-%H-%M-%S")
        self.storagePath = Path.joinpath(self.currentDirectory, "Simulations")
        if not Path.exists(self.storagePath):
            Path.mkdir(self.storagePath)
        self.simulationPath = Path.joinpath(self.storagePath, "Run-" + self.dateTime)
        if not Path.exists(self.simulationPath):
            Path.mkdir(self.simulationPath)
        self.serviceAreaPath = Path.joinpath(self.simulationPath, "ServiceAreas")
        if not Path.exists(self.serviceAreaPath):
            Path.mkdir(self.serviceAreaPath)
        self.localServiceNetworkPath = Path.joinpath(self.simulationPath, "LocalServiceNetworks")
        if not Path.exists(self.localServiceNetworkPath):
            Path.mkdir(self.localServiceNetworkPath)
        self.companyPath = Path.joinpath(self.simulationPath, "Companies")
        if not Path.exists(self.companyPath):
            Path.mkdir(self.companyPath)
        self.plotPath = self.currentDirectory.joinpath('Plots')
        if not Path.exists(self.plotPath):
            Path.mkdir(self.plotPath)
        
    def jsonable(self):
        jsonDict = self.__dict__.copy()
        jsonDict = dict()
        for key in self.__dict__:
            item = self.__dict__[key]
            if isinstance(item, Path):
                jsonDict[key] = item.name
            else:
                jsonDict[key] = item
        return jsonDict
        
    def createInstanceOutputFolder(self, path : Path, folderName, id):
        folderPath = path.joinpath(folderName + "#" + str(id))
        Path.mkdir(folderPath)
        return folderPath