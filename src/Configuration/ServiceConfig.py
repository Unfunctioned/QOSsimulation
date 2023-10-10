'''Stores configuration for service requirements'''
class ServiceConfig(object):
    
    def __init__(self) -> None:
        # Data rate default in mbps
        self.CAPACITY_DEFAULT = 10
        # Default latency in ms
        self.LATENCY_DEFAULT = 10
        # Default service availability in percent
        self.RELIABILITY_DEFAULT = 0.95