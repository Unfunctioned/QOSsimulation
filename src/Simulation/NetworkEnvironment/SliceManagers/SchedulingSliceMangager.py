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
        
    def addNetworkSlice(self, _ : int, activationTime: int, networkSlice: NetworkSlice):
        self._TryAddActivationTime(activationTime)
        self._TryAddActiveSlice(activationTime, networkSlice)
        reservations = self.sliceToReservation[networkSlice]
        for reservation in reservations:
            networkSlice.addServiceRequirement(self.serviceAreaId, reservation.serviceRequirement)
        
    def _TryAddActivationTime(self, activationTime : int):
        if not activationTime in self.activationKeys.queue:
            self.activationKeys.put(activationTime)
            return True
        return False

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
    
    #def _getReservations(self, key, networkSlice : NetworkSlice):
    #    reservations = list()
    #    for reservation in self.keysToReservation[key]:
    #        if reservation.networkSlice == networkSlice:
    #            reservations.append(reservation)
    #    return reservations
    
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
    
    def CheckForQoSViolation(self, serviceRequirement : ServiceRequirement, excessDemand : int, latency : int):
        if excessDemand > 0:
            violationType = ViolationStatusType.CAPACITY
            if excessDemand < serviceRequirement.defaultCapacityDemand:
                violationType = ViolationStatusType.PARTIAL_CAPACITY
            return violationType
                #adjustedDemand.private += serviceRequirement.defaultCapacityDemand - excessDemand
                #excessDemand -= serviceRequirement.defaultCapacityDemand
                #sliceViolations.append((serviceRequirement, violationType))
                #continue
        if serviceRequirement.latency is None:
            return None
        if serviceRequirement.latency < latency:
            return ViolationStatusType.LATENCY
            #sliceViolations.append((serviceRequirement, ViolationStatusType.LATENCY))
            #adjustedDemand.private += serviceRequirement.defaultCapacityDemand
    
    def UpdateViolations(self, sliceViolations: list, excessDemand : CapacityDemand, adjustedDemand : CapacityDemand,
                         latency : int, serviceRequirement : ServiceRequirement):
        violationType = self.CheckForQoSViolation(serviceRequirement, excessDemand, latency)
        if violationType is None:
            return sliceViolations, excessDemand, adjustedDemand
        if violationType == ViolationStatusType.CAPACITY or violationType == ViolationStatusType.PARTIAL_CAPACITY:
            if violationType == ViolationStatusType.PARTIAL_CAPACITY:
                adjustedDemand.private += serviceRequirement.defaultCapacityDemand - excessDemand
            excessDemand -= serviceRequirement.defaultCapacityDemand
            sliceViolations.append((serviceRequirement, violationType))
            if violationType == ViolationStatusType.LATENCY:
                sliceViolations.append((serviceRequirement, violationType))
                adjustedDemand.private += serviceRequirement.defaultCapacityDemand
        return sliceViolations, excessDemand, adjustedDemand

    def FindQoSViolations(self, currentTime: int, latency : int, capacityDemand: CapacityDemand):
        violations = {}
        adjustedDemand = CapacityDemand(0, capacityDemand.publicMinimum, 
                                        capacityDemand.publicMaximum, capacityDemand.maximumCapacity)
        excessDemand = max(0, capacityDemand.private + capacityDemand.publicMinimum - capacityDemand.maximumCapacity)
        
        activeReservations, unreservedActiveSlices = self.GetDemandPriorities()
        #if len(activeReservations) > 1:
        #    print(activeReservations)
        #   print(unreservedActiveSlices)
        #   print("Take a break")
          
        for item in unreservedActiveSlices:  
            networkSlice, _ = item
            serviceRequirements = networkSlice.GetServiceRequirement(self.serviceAreaId)
            sliceViolations = []
            for serviceRequirement in serviceRequirements:
                sliceViolations, excessDemand, adjustedDemand = self.UpdateViolations(
                    sliceViolations, excessDemand, adjustedDemand, latency, serviceRequirement)
                if(len(sliceViolations) > 0):
                    violations[networkSlice] = sliceViolations
                      
        for activeReservation in activeReservations:
            if not activeReservation.networkSlice in self.activeSlices:
                raise ValueError("Netork slice is not active")
            serviceRequirement = activeReservation.serviceRequirement
            sliceViolations, excessDemand, adjustedDemand = self.UpdateViolations(
                [], excessDemand, adjustedDemand, latency, serviceRequirement)
            if(len(sliceViolations) > 0):
                violations[activeReservation.networkSlice] = sliceViolations
            
        return violations, adjustedDemand
        
        #activationHistory = self.activationKeys.queue.copy()
        #activationHistory.reverse()
        #for key in activationHistory:
        #    if key > currentTime or not key in self.keysToReservation:
        #        continue
        #    reservations = self.keysToReservation[key]
        #    for reservation in reservations:
        #        networkSlice = reservation.networkSlice
        #        if not networkSlice in self.activeSlices:
        #            continue
        #        serviceRequirements = networkSlice.GetServiceRequirement(self.serviceAreaId)
        #        sliceViolations = []
        #        serviceRequirement : ServiceRequirement
        #        for serviceRequirement in serviceRequirements:
        #            if excessDemand > 0:
        #                violationType = ViolationStatusType.CAPACITY
        #                if excessDemand < serviceRequirement.defaultCapacityDemand:
        #                    violationType = ViolationStatusType.PARTIAL_CAPACITY
        #                    adjustedDemand.private += serviceRequirement.defaultCapacityDemand - excessDemand
        #                excessDemand -= serviceRequirement.defaultCapacityDemand
        #                sliceViolations.append((serviceRequirement, violationType))
        #                continue
        #            if serviceRequirement.latency is None:
        #                continue
        #            if serviceRequirement.latency < latency:
        #                sliceViolations.append((serviceRequirement, ViolationStatusType.LATENCY))
        #                adjustedDemand.private += serviceRequirement.defaultCapacityDemand
        #        if(len(sliceViolations) > 0):
        #            violations[networkSlice] = sliceViolations
        #return violations, adjustedDemand
    
    def GetDemandPriorities(self) -> tuple[list[ReservationItem], list[tuple[NetworkSlice, int]]]:
        reservations = list()
        sliceActivations = list()
        for networkSlice in self.activeSlices:
            if networkSlice in self.sliceToReservation:
                reservations.extend(self.sliceToReservation[networkSlice])
            else:
                if len(self.activeSlices[networkSlice]) > 1:
                    raise ValueError("Network slice has more than one activation key")
                sliceActivations.append((networkSlice, list(self.activeSlices[networkSlice])[0]))
        reservations.sort(key=lambda x : x.activationTime, reverse=True)
        sliceActivations.sort(key=lambda x : x[1], reverse=True)
        return reservations, sliceActivations
    
    def CanSchedule(self, reservation : ReservationItem, totalCapacity : int) -> bool:
        demand = reservation.GetDemand()
        duration = 0
        time = reservation.activationTime
        for item in iter(self.allocationQueue):
            if item.t < reservation.activationTime:
                demand += item.capacityChange
            else:
                if demand < totalCapacity:
                    duration += item.t - time
                    if duration >= reservation.duration:
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
        activationTime = reservationItem.activationTime
        self._TryAddActivationTime(activationTime)
        self._MapTimeToReservation(activationTime, reservationItem)
        self._MapSliceToReservation(reservationItem)
        #if not networkSlice in self.sliceToKey:
        #    self.sliceToKey[networkSlice] = set()
        #self.sliceToKey[networkSlice].add(activationTime)
    
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