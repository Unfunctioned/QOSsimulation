from dataclasses import dataclass, field
from Simulation.NetworkEnvironment.ServiceRequirements.ServiceRequirement import ServiceRequirement

@dataclass(order=True)
class CapacityItem:
    t: int
    capacityChange: int=field(compare=False)
    
def SetQueue() -> list[CapacityItem]:
    queue = list()
    queue.append(CapacityItem(0, 5))
    queue.append(CapacityItem(12, 3))
    queue.append(CapacityItem(26, -5))
    queue.append(CapacityItem(36, 5))
    queue.append(CapacityItem(46, -5))
    queue.append(CapacityItem(48, -3))
    queue.append(CapacityItem(58, 5))
    queue.append(CapacityItem(68, -5))
    return sorted(queue, key=lambda x: x.t)

def SetServiceRequirements() -> list[ServiceRequirement]:
    requirements = list()
    requirements.append(ServiceRequirement(10, 5, 0.99, 0))
    return requirements
    
def GetDemand(serviceRequirements : list[ServiceRequirement]):
    demand = 0
    for requirement in serviceRequirements:
        demand += requirement.defaultCapacityDemand
    return demand

def main():
    print(FirstSufficientCapacity(0, 15, 10, SetServiceRequirements(), 10))

def FirstSufficientCapacity(currentTime : int, activationTime : int, expectedDuration : int, serviceRequirements : list[ServiceRequirement], totalCapacity : int):
    queue : list[CapacityItem]
    queue = SetQueue()
    demand = GetDemand(serviceRequirements)
    duration = 0
    time = activationTime
    for item in queue:
        if item.t > activationTime:
            if demand <= totalCapacity:
                duration = item.t - time
            else:
                duration = 0
            if duration >= expectedDuration:
                return time
            time = item.t
        demand += item.capacityChange
            

if __name__ == "__main__":
    main()