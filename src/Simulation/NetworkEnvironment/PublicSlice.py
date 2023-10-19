from Simulation.NetworkEnvironment.NetworkSlice import NetworkSlice
from Simulation.NetworkEnvironment.ServiceRequirements.ServiceRequirement import DynamicServiceRequirement

'''Network slice representing the public network activity'''
class PublicSlice(NetworkSlice):
    
    def __init__(self, folderPath) -> None:
        super().__init__(-1, folderPath)
        
    def GetServiceAreaRequirements(self, serviceAreaId : int) -> set[DynamicServiceRequirement]:
        if serviceAreaId in self.ServiceAreaRequirements:
            return self.ServiceAreaRequirements[serviceAreaId]
        
    def GetMaxDataRate(self, serviceArea, demandLimitation):
        serviceAreaRequirements = list(self.GetServiceAreaRequirements(serviceArea))
        if(not len(serviceAreaRequirements) == 1):
            raise ValueError("Invalid requirments")
        serviceAreaRequirement : DynamicServiceRequirement
        serviceAreaRequirement = serviceAreaRequirements[0]
        if(demandLimitation < serviceAreaRequirement.defaultCapacityDemand):
            return serviceAreaRequirement.minUserDemand
        datarate = float(demandLimitation / max(serviceAreaRequirement.users, 1))
        if (datarate < serviceAreaRequirement.minUserDemand):
            raise ValueError("Invalid datarate result")
        return datarate