from collections.abc import Callable, Iterable, Mapping
from typing import Any
from Simulation.PhysicalEnvironment.ServiceArea import ServiceArea
from Simulation.NetworkEnvironment.NetworkSlice import NetworkSlice
from Simulation.NetworkEnvironment.ServiceRequirements.ServiceRequirement import ServiceRequirement
from Utilities.ItemTypes.ReservationItem import ReservationItem
import threading

class ExceptionCatcher(object):
    
    def __init__(self) -> None:
        self.lock = threading.Lock()
        self._exceptions = []
        
    def SetException(self, e : Exception):
        with self.lock:
            self._exceptions.append(e)
    
    def CheckForException(self):
        with self.lock:
            if len(self._exceptions) > 0:
                raise self._exceptions[0]
        
    

class ReservationResult(object):
    
    def __init__(self) -> None:
        self.lock = threading.Lock()
        self._failedArea = None
        self._failedReservation = None
        
    def SetFailureResult(self, area : ServiceArea, reservation : ReservationItem):
        with self.lock:
            if self._failedReservation is None:
                self._failedReservation = reservation
                self._failedArea = area
            elif self._failedReservation.activationTime > reservation.activationTime:
                self._failedReservation = reservation
                self._failedArea = area
    
    def IsSuccess(self):
        with self.lock:
            status = True
            if self._failedArea is None or self._failedReservation is None:
                status = False
            return status, (self._failedArea, self._failedReservation)

class Schedulable(threading.Thread):
    
    def __init__(self, area : ServiceArea, areaReservations : list[ReservationItem], results : ReservationResult,
                 exceptionCatcher : ExceptionCatcher, group: None = None, target: Callable[..., object] | None = None, name: str | None = None, args: Iterable[Any] = ..., kwargs: Mapping[str, Any] | None = None, *, daemon: bool | None = None) -> None:
        super().__init__(group, target, name, args, kwargs, daemon=daemon)
        self.area = area
        self.areaReservations = areaReservations
        self.results = results
        self.exceptionCatcher = exceptionCatcher
        
    def run(self):
        try:
            for reservation in self.areaReservations:
                serviceNetwork = self.area.GetLocalServiceNetwork()
                if not serviceNetwork.CanScheduleNetworkSlice(reservation):
                    self.results.SetFailureResult(self.area, reservation)
        except Exception as e:
            self.exceptionCatcher.SetException(e)

'''Used to manage the scheduling of business processes'''
class SchedulingManager(object):
    
    def __init__(self, serviceAreas : list[ServiceArea]) -> None:
        self.serviceAreas = serviceAreas
    
    def CanScheduleReservations(self, reservations : dict[ServiceArea, list[ReservationItem]]) -> tuple[bool, tuple[ServiceArea, ReservationItem]]:
        reservationResult = ReservationResult()
        exceptionCatcher = ExceptionCatcher()
        threads : list[Schedulable]
        threads = []
        for area in reservations:
            schedulable = Schedulable(area, reservations[area], reservationResult, exceptionCatcher)
            threads.append(schedulable)
            schedulable.start()
        for t in threads:
            t.join()
        exceptionCatcher.CheckForException()
        return reservationResult.IsSuccess()
            
    def ScheduleReservations(self, activationTime : int, reservations : dict[ServiceArea, list[ReservationItem]], networkSlice : NetworkSlice) -> None:
        nextActivationTime = activationTime
        for area in reservations:
            areaReservations : tuple[int, ServiceRequirement]
            areaReservations = reservations[area]
            for reservation in areaReservations:
                serviceNetwork = area.GetLocalServiceNetwork()
                serviceNetwork.ScheduleNetworkSlice(nextActivationTime, networkSlice, reservation)
                nextActivationTime = activationTime
                
    def FindFirstAvailability(self, activationTime : int, reservations : dict[ServiceArea, list[ReservationItem]]) -> tuple[int, dict[ServiceArea, list[ReservationItem]]]:
        firstArea = list(reservations.keys())[0]
        canSchedule = False
        candidateTime = activationTime
        attempts = 0
        while not canSchedule:
            self.UpdateActivationTimes(candidateTime, reservations)
            canSchedule = self.CanScheduleReservations(reservations)
            if not canSchedule:
                serviceNetwork = firstArea.GetLocalServiceNetwork()
                foundTime, candidateTime = serviceNetwork.TryFindNextPossibleAllocation(candidateTime + 1, reservations[firstArea])
                if not foundTime:
                    raise Exception("Unable to start process in given area")
            attempts += 1
            if attempts % 100 == 99:
                print("Failed to find candiate {count} times".format(count = attempts))
        return candidateTime, reservations
    
    def UpdateActivationTimes(self, candidateTime : int, reservations : dict[ServiceArea, list[ReservationItem]]):
        for area in reservations:
            for reservation in reservations[area]:
                if not reservation.activationTime == candidateTime:
                    reservation.activationTime == candidateTime
                    candidateTime += reservation.duration

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