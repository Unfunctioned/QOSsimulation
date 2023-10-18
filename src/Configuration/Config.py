from Configuration.Randoms import Randoms
from Configuration.AppSettings import AppSettings
from Configuration.SimConfig import SimConfig
from Configuration.EventConfig import EventConfig
from Configuration.FilePath import FilePath
from Configuration.MobilityConfig import MobilityConfig
from Configuration.ServiceConfig import ServiceConfig
from Configuration.BaseConfig import BaseConfig
class Config(BaseConfig):
    
    def __init__(self, worldId = 0, seedId = 0) -> None:
        self.appSettings = AppSettings()
        self.randoms = Randoms()
        self.simConfig = SimConfig()
        self.eventConfig = EventConfig()
        self.filePaths = FilePath(worldId, seedId)
        self.mobilityConfig = MobilityConfig()
        self.serviceConfig = ServiceConfig()
        
    def setSeeds(self, seeds : list[int]):
        self.randoms = Randoms(seeds)
        
    def jsonable(self):
        jsonDict = self.__dict__.copy()
        for key in jsonDict:
            item : BaseConfig
            item =jsonDict[key]
            jsonItem = item.jsonable()
            jsonDict[key] = jsonItem
        return jsonDict