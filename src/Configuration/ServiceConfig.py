from Configuration.BaseConfig import BaseConfig
'''Stores configuration for service requirements'''
class ServiceConfig(BaseConfig):
    
    def __init__(self) -> None:
        # Data rate default in mbps
        self.CAPACITY_DEFAULT = 10
        # Default latency in ms
        self.LATENCY_DEFAULT = 10
        # Default service availability in percent
        self.RELIABILITY_DEFAULT = 0.99
        
    def jsonable(self):
        return self.__dict__