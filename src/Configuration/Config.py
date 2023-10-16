from Configuration.Randoms import Randoms
from Configuration.UISettings import UISettings
from Configuration.SimConfig import SimConfig
from Configuration.EventConfig import EventConfig
from Configuration.FilePath import FilePath
from Configuration.MobilityConfig import MobilityConfig
from Configuration.ServiceConfig import ServiceConfig
from Configuration.BaseConfig import BaseConfig
class Config(BaseConfig):
    
    def __init__(self) -> None:
        self.uiSettings = UISettings()
        self.randoms = Randoms()
        self.simConfig = SimConfig()
        self.eventConfig = EventConfig()
        self.filePaths = FilePath()
        self.mobilityConfig = MobilityConfig()
        self.serviceConfig = ServiceConfig()
        
    def jsonable(self):
        jsonDict = self.__dict__.copy()
        for key in jsonDict:
            item : BaseConfig
            item =jsonDict[key]
            jsonItem = item.jsonable()
            jsonDict[key] = jsonItem
        return jsonDict