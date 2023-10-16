from Configuration.BaseConfig import BaseConfig
'''Configures mobility of mobile units'''
class MobilityConfig(BaseConfig):
    
    def __init__(self) -> None:
        #Velocity in m/s (50 km/h = 13.89 m/s)
        self.localSpeed = 13.89
        #Velocity on highways in m/s (assuming vehicle is a truck) (80 km/h = 22.22)
        self.passingSpeed = 22.22
        
    def jsonable(self):
        return self.__dict__