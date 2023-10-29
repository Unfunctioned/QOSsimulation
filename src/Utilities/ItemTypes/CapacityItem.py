from dataclasses import dataclass
from Simulation.NetworkEnvironment.NetworkSlice import NetworkSlice

@dataclass
class CapacityItem:
    t: int
    capacityChange: int
    networkSlice : NetworkSlice
    
    def __lt__(self, __value: object) -> bool:
        if not isinstance(__value, CapacityItem):
            raise TypeError("Expected an object of type {type}".format(type = CapacityItem))
        return self.t < __value.t