from Configuration.Randoms import Randoms
from Configuration.UISettings import UISettings
class Config(object):
    
    def __init__(self) -> None:
        self.uiSettings = UISettings()
        self.GRIDSIZE = 7
        self.DENSITY_LEVEL = 500
        self.randoms = Randoms()