from Simulation.NetworkEnvironment.CapacityDemand import CapacityDemand
from Simulation.NetworkEnvironment.NetworkSlice import NetworkSlice
from Simulation.NetworkEnvironment.PublicSlice import PublicSlice
from Simulation.NetworkEnvironment.SliceManagers.NetworkSliceManager import NetworkSliceManager
from Simulation.NetworkEnvironment.ServiceRequirements.ServiceRequirement import ServiceRequirement, DynamicServiceRequirement
from queue import PriorityQueue
from Utilities.ItemTypes.ReservationItem import ReservationItem
from Simulation.NetworkEnvironment.ViolationStatusType import ViolationStatusType
from Utilities.AllocationQueue import AllocationQueue
from Utilities.ItemTypes.CapacityItem import CapacityItem
    

'''Network slice manager to handle the scheduling scenario'''
class SchedulingSliceManager(NetworkSliceManager):
    
    def __init__(self, serviceAreaId : int) -> None:
        self.serviceAreaId = serviceAreaId
        
        self.activationKeys = PriorityQueue()
        self.allocationQueue = AllocationQueue()
        
        #SLice currently active in the network
        self.activeSlices : dict[NetworkSlice, set[int]]
        self.activeSlices = dict()
        
        #Map of activation times to scheduled reservation
        self.keysToReservation : dict[int, set[ReservationItem]]
        self.keysToReservation = dict()
        
        #Map of network slices to associated reservations
        self.sliceToReservation : dict[NetworkSlice, set[ReservationItem]]
        self.sliceToReservation = dict()
        
        #self.keysToSlice : dict[int, set[NetworkSlice]]
        #self.keysToSlice = dict()
        #self.sliceToKey : dict[NetworkSlice, set[int]]
        #self.sliceToKey = dict()
        
    def addNetworkSlice(self, activationTime: int, networkSlice: NetworkSlice):
        if networkSlice.companyId == 1245 and activationTime == 655:
            print("Take a break")
        self._TryAddActivationTime(activationTime)
        self._TryAddActiveSlice(activationTime, networkSlice)
        reservations = self.sliceToReservation[networkSlice]
        for reservation in reservations:
            networkSlice.addServiceRequirement(self.serviceAreaId, reservation.serviceRequirement)
        
        #if not activationTime in self.keysToSlice:
        #    self.keysToSlice[activationTime] = set()
        #self.keysToSlice[activationTime].add(networkSlice)
        #if not networkSlice in self.sliceToKey:
        #    self.sliceToKey[networkSlice] = set()
        #self.sliceToKey[networkSlice].add(activationTime)
        
    def _TryAddActiveSlice(self, activationTime : int, networkSlice : NetworkSlice):
        if not activationTime in self.activeSlices:
            self.activeSlices[networkSlice] = set()
        self.activeSlices[networkSlice].add(activationTime)
        
    def removeNetworkSlice(self, currentTime : int, networkSlice: NetworkSlice):
        reservations = self._getKey(networkSlice)
        hasUnfinishedReservations = False
        unfinishedReservations = set()
        for reservation in reservations:
            if reservation.activationTime + reservation.duration < currentTime:
                hasUnfinishedReservations = True
                unfinishedReservations.add(reservation)
        deactivations = reservations.difference(unfinishedReservations)
        self.activeSlices.pop(networkSlice)
        if not hasUnfinishedReservations:
            deactivations = self.sliceToReservation.pop(networkSlice)
        else:
            self.sliceToReservation[networkSlice] = self.sliceToReservation[networkSlice].intersection(unfinishedReservations)
        for deactivation in deactivations:
            self.keysToReservation[deactivation.activationTime].remove(deactivation)
            
            
            
        #if not networkSlice in self.activeSlices:
        #    raise ValueError("Given network slice could not be found")
        #keys = self.activeSlices.pop(networkSlice)
        #for key in keys:
        #    reservations = self._getReservations(key, networkSlice)
        #    for reservation in reservations:
        #        if (len(self.keysToReservation[key]) == 1):
        #            self.keysToReservation.pop(key)
        #            self.activationKeys.queue.remove(key)
        #            return
        #        self.keysToReservation[key].remove(reservation)
        
    def _getKey(self, networkSlice: NetworkSlice) -> set[ReservationItem]:
        if not networkSlice in self.sliceToReservation:
            raise ValueError("Given Network slice could not be found")
        return self.sliceToReservation[networkSlice]
    
    def _getReservations(self, key, networkSlice : NetworkSlice):
        reservations = list()
        for reservation in self.keysToReservation[key]:
            if reservation.networkSlice == networkSlice:
                reservations.append(reservation)
        return reservations
    
    def GetPrivateDemand(self, currentTime: int):
        demand = 0
        for i in range(1, len(self.activationKeys.queue)):
            key = self.activationKeys.queue[i]
            if key > currentTime or not key in self.keysToReservation:
                continue
            reservations = self.keysToReservation[key]
            reservation : ReservationItem
            for reservation in reservations:
                alreadyEnded = reservation.activationTime + reservation.duration < currentTime
                inactive = not reservation.networkSlice in self.activeSlices
                if alreadyEnded or inactive:
                    continue
                networkSlice = reservation.networkSlice
                if (isinstance(networkSlice, PublicSlice)):
                    continue
                serviceRequirements = networkSlice.GetServiceRequirement(self.serviceAreaId)
                for serviceRequirement in serviceRequirements:
                    if(isinstance(serviceRequirement, DynamicServiceRequirement)):
                        raise ValueError("Invalid private slice")
                    if(isinstance(serviceRequirement, ServiceRequirement)):
                        demand += serviceRequirement.defaultCapacityDemand
        return demand
    
    def FindQoSViolations(self, currentTime: int, latency, capacityDemand: CapacityDemand):
        violations = {}
        adjustedDemand = CapacityDemand(0, capacityDemand.publicMinimum, 
                                        capacityDemand.publicMaximum, capacityDemand.maximumCapacity)
        excessDemand = max(0, capacityDemand.private + capacityDemand.publicMinimum - capacityDemand.maximumCapacity)
        activationHistory = self.activationKeys.queue.copy()
        activationHistory.reverse()
        for key in activationHistory:
            if key > currentTime or not key in self.keysToReservation:
                continue
            reservations = self.keysToReservation[key]
            for reservation in reservations:
                networkSlice = reservation.networkSlice
                if not networkSlice in self.activeSlices:
                    continue
                serviceRequirements = networkSlice.GetServiceRequirement(self.serviceAreaId)
                sliceViolations = []
                serviceRequirement : ServiceRequirement
                for serviceRequirement in serviceRequirements:
                    if excessDemand > 0:
                        violationType = ViolationStatusType.CAPACITY
                        if excessDemand < serviceRequirement.defaultCapacityDemand:
                            violationType = ViolationStatusType.PARTIAL_CAPACITY
                            adjustedDemand.private += serviceRequirement.defaultCapacityDemand - excessDemand
                        excessDemand -= serviceRequirement.defaultCapacityDemand
                        sliceViolations.append((serviceRequirement, violationType))
                        continue
                    if serviceRequirement.latency is None:
                        continue
                    if serviceRequirement.latency < latency:
                        sliceViolations.append((serviceRequirement, ViolationStatusType.LATENCY))
                        adjustedDemand.private += serviceRequirement.defaultCapacityDemand
                if(len(sliceViolations) > 0):
                    violations[networkSlice] = sliceViolations
        return violations, adjustedDemand
    
    def CanSchedule(self, activationTime : int, reservation : ReservationItem, totalCapacity : int) -> bool:
        demand = reservation.GetDemand()
        duration = 0
        time = activationTime
        for item in iter(self.allocationQueue):
            if item.t < activationTime:
                demand += item.capacityChange
            else:
                if demand < totalCapacity:
                    duration += item.t - time
                    if duration >= reservation.activationTime:
                        break
                else:
                    return False
                time = item.t
                demand += item.capacityChange
        return True
    
    def Schedule(self, activationTime : int, reservation : ReservationItem, networkSlice : NetworkSlice):
        requirement = reservation.serviceRequirement
        self.AddReservation(reservation)
        self.allocationQueue.Put(CapacityItem(activationTime, requirement.defaultCapacityDemand, networkSlice))
        if not isinstance(networkSlice, PublicSlice):
            self.allocationQueue.Put(CapacityItem(activationTime + reservation.duration, -requirement.defaultCapacityDemand, networkSlice))
      
    def AddReservation(self, reservationItem : ReservationItem):
        if reservationItem.networkSlice.companyId == 1245 and reservationItem.activationTime == 655:
            print("Take a break")
        activationTime = reservationItem.activationTime
        self._TryAddActivationTime(activationTime)
        self._MapTimeToReservation(activationTime, reservationItem)
        self._MapSliceToReservation(reservationItem)
        #if not networkSlice in self.sliceToKey:
        #    self.sliceToKey[networkSlice] = set()
        #self.sliceToKey[networkSlice].add(activationTime)
        
    def _TryAddActivationTime(self, activationTime : int):
        if not activationTime in self.activationKeys.queue:
            self.activationKeys.put(activationTime)
            return True
        return False
    
    def _MapTimeToReservation(self, activationTime : int, reservation : ReservationItem):
        if not activationTime in self.keysToReservation:
            self.keysToReservation[activationTime] = set()
        self.keysToReservation[activationTime].add(reservation)
        
    def _MapSliceToReservation(self, reservation : ReservationItem):
        if not reservation.networkSlice in self.sliceToReservation:
            self.sliceToReservation[reservation.networkSlice] = set()
        self.sliceToReservation[reservation.networkSlice].add(reservation)
                         
    def FirstSufficientCapacity(self, activationTime : int, expectedDuration : int, serviceRequirements : list[ServiceRequirement], totalCapacity : int) -> tuple[bool, int]:
        demand = self._GetRequirementDemand(serviceRequirements)
        duration = 0
        time = activationTime
        for item in iter(self.allocationQueue):
            if item.t > activationTime:
                if demand <= totalCapacity:
                    duration = item.t - time
                else:
                    duration = 0
                if duration >= expectedDuration:
                    return True, time
                time = item.t
            demand += item.capacityChange
    
    def TryFindNextPossibleAllocation(self, candidateTime: int, reservations : list[tuple[int, ServiceRequirement]], totalCapacity : int) -> tuple[bool, int]:
        currentIndex = 0
        time = candidateTime
        demand = reservations[currentIndex][1].defaultCapacityDemand
        for item in self.allocationQueue:
            if item.t > candidateTime:
                if demand <= totalCapacity:
                    duration = item.t - time
                else:
                    duration = 0
                if duration >= reservations[currentIndex][0]:
                    if currentIndex == len(reservations) -1:
                        return True, time
                    else:
                        duration -= reservations[currentIndex][0]
                        currentIndex += 1
                        demand = reservations[currentIndex][1].defaultCapacityDemand
                time = item.t
            demand += item.capacityChange
        if demand < totalCapacity:
            return True, time
        return False, -1
    
    def _GetRequirementDemand(serviceRequirements : list[ServiceRequirement]):
        demand = 0
        for requirement in serviceRequirements:
            demand += requirement.defaultCapacityDemand
        return demand