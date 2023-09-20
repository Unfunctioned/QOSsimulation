from Configuration.Randoms import Randoms
from Configuration.UISettings import UISettings
from Configuration.SimConfig import SimConfig
class Config(object):
    
    def __init__(self) -> None:
        self.uiSettings = UISettings()
        self.randoms = Randoms()
        self.simConfig = SimConfig()