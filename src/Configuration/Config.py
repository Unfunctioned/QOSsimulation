from Configuration.Randoms import Randoms
from Configuration.UISettings import UISettings
from Configuration.SimConfig import SimConfig
from Configuration.EventConfig import EventConfig
from Configuration.FilePath import FilePath
class Config(object):
    
    def __init__(self) -> None:
        self.uiSettings = UISettings()
        self.randoms = Randoms()
        self.simConfig = SimConfig()
        self.eventConfig = EventConfig()
        self.filePaths = FilePath()