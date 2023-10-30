from Simulation.PhysicalEnvironment.ServiceArea import ServiceArea
from Simulation.NetworkEnvironment.NetworkSlice import NetworkSlice
from Simulation.NetworkEnvironment.ServiceRequirements.ServiceRequirement import ServiceRequirement
from Utilities.ItemTypes.ReservationItem import ReservationItem

'''Used to manage the scheduling of business processes'''
class SchedulingManager(object):
    
    def __init__(self, serviceAreas : list[ServiceArea]) -> None:
        self.serviceAreas = serviceAreas
    
    def CanScheduleReservations(self, activationTime : int, reservations : dict[ServiceArea, list[ReservationItem]]) -> tuple[bool, tuple[ServiceArea, ReservationItem]]:
        nextActivationTime = activationTime
        for area in reservations:
            areaReservations = reservations[area]
            for reservation in areaReservations:
                serviceNetwork = area.GetLocalServiceNetwork()
                if not serviceNetwork.CanScheduleNetworkSlice(nextActivationTime, reservation):
                    return False, (area, reservation)
                nextActivationTime += reservation.duration
        return True, (None, None)
            
    def ScheduleReservations(self, activationTime : int, reservations : dict[ServiceArea, list[ReservationItem]], networkSlice : NetworkSlice) -> None:
        nextActivationTime = activationTime
        for area in reservations:
            areaReservations : tuple[int, ServiceRequirement]
            areaReservations = reservations[area]
            for reservation in areaReservations:
                serviceNetwork = area.GetLocalServiceNetwork()
                serviceNetwork.ScheduleNetworkSlice(nextActivationTime, networkSlice, reservation)
                nextActivationTime = activationTime
                
    def FindFirstAvailability(self, activationTime : int, reservations : dict[ServiceArea, list[tuple[int, ServiceRequirement]]]) -> int:
        firstArea = list(reservations.keys())[0]
        canSchedule = False
        candidateTime = activationTime
        attempts = 0
        while not canSchedule:
            canSchedule = self.CanScheduleReservations(candidateTime, reservations)
            if not canSchedule:
                serviceNetwork = firstArea.GetLocalServiceNetwork()
                foundTime, candidateTime = serviceNetwork.TryFindNextPossibleAllocation(candidateTime + 1, reservations[firstArea])
                if not foundTime:
                    raise Exception("Unable to start process in given area")
            attempts += 1
            if attempts % 100 == 99:
                print("Failed to find candiate {count} times".format(count = attempts))
        return candidateTime

global SCHEDULING_MANAGER
SCHEDULING_MANAGER = None

def SetSchedulingManager(generator : SchedulingManager):
    global SCHEDULING_MANAGER
    SCHEDULING_MANAGER = generator
    
def GetSchedulingManager() -> SchedulingManager:
    global SCHEDULING_MANAGER
    if SCHEDULING_MANAGER is None:
        raise ValueError("Scheduling Manager not initialized")
    return SCHEDULING_MANAGER