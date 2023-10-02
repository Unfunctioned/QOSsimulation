from Simulation.NetworkEnvironment.NetworkSlice import NetworkSlice
from Simulation.NetworkEnvironment.ServiceRequirements.ServiceRequirement import DynamicServiceRequirement

'''Network slice representing the public network activity'''
class PublicSlice(NetworkSlice):
    
    def __init__(self, folderPath) -> None:
        super().__init__(-1, folderPath)
        
    def GetServiceAreaRequirements(self, serviceArea) -> DynamicServiceRequirement:
        if serviceArea in self.ServiceAreaRequirements:
            return self.ServiceAreaRequirements[serviceArea]