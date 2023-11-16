from Simulation.BusinessEnvironment.Company import Company
from Simulation.Events.BusinessEvents.BusinessProcessActivationEvent import BusinessProcessActivationEvent
from Simulation.Events.BusinessEvents.BusinessEventType import BusinessEventType
from Simulation.BusinessEnvironment.BusinessActivity import BusinessActivity, AreaBasedActivity, PathBasedActivity, TrajectoryBasedActivity
from Simulation.PhysicalEnvironment.ServiceArea import ServiceArea
from Utilities.PathGenerator import GetPathGenerator
from Utilities.SchedulingManager import GetSchedulingManager
from Simulation.NetworkEnvironment.ServiceRequirements.ServiceRequirement import ServiceRequirement
from Simulation.BusinessEnvironment.BusinessProcess import BusinessProcess
from Utilities.ItemTypes.ReservationItem import ReservationItem

'''Event to trigger activation of business processes for scheduled processes'''
class ScheduledBusinessProcessActivationEvent(BusinessProcessActivationEvent):
    
    def __init__(self, eventTime, activationTime, company: Company, businessProcess = None) -> None:
        super().__init__(eventTime, company)
        self.activationTime = activationTime
        self.businessProcess : BusinessProcess
        self.businessProcess = self.company.GenerateBusinessProcessProcess(self.activationTime) if businessProcess is None else businessProcess
        self.generateFollowUpEvent = True
        
    def trigger(self):
        reservations : dict[ServiceArea, list[ReservationItem]]
        reservations = self.CalculateReservations()
        canSchedule, (failedArea, reservation) = GetSchedulingManager().CanScheduleReservations(reservations)
        if canSchedule:
            GetSchedulingManager().ScheduleReservations(self.activationTime, reservations, self.company.networkSlice)
        else:
            time, updatedReservations = GetSchedulingManager().FindFirstAvailability(self.activationTime, reservations)
            GetSchedulingManager().ScheduleReservations(time, updatedReservations, self.company.networkSlice)

    def CalculateReservations(self) -> dict[ServiceArea, list[ReservationItem]]:
        reservations = dict()
        activationTime = self.activationTime
        activity : BusinessActivity
        for activity in self.businessProcess.activities:
            if isinstance(activity, AreaBasedActivity):
                reservation = ReservationItem(activationTime, activity.expectedDuration, self.company.networkSlice, activity.serviceRequirement)
                reservations = self._addReservation(reservations, reservation, activity.location)
                activationTime += reservation.duration
            elif isinstance(activity, PathBasedActivity):
                for i in range(len(activity.movementPath) - 1):
                    isLocalSpeed = self._setLocalSpeeds(i, len(activity.movementPath) - 2)
                    start, end = activity.movementPath[i], activity.movementPath[i+1]
                    p1, p2 = GetPathGenerator().FindCommonBorder(start, end)
                    transition = GetPathGenerator().CalculateTransitionPoint(p1, p2)
                    
                    startReservation = self._generatePathReservation(activationTime, start.cell.site, transition, activity.serviceRequirement, isLocalSpeed[0])
                    reservations = self._addReservation(reservations, startReservation, start)
                    activationTime += startReservation.duration
                    
                    endReservation = self._generatePathReservation(activationTime, transition, end.cell.site, activity.serviceRequirement, isLocalSpeed[1])
                    reservations = self._addReservation(reservations, endReservation, end)
                    activationTime += endReservation.duration
            else:
                raise TypeError("Activity does not match any type, found {type}".format(type=type(activity)))
        return reservations
    
    def _addReservation(self, reservations : dict[ServiceArea, list[ReservationItem]],
                        reservation : ReservationItem,
                        area : ServiceArea):
        if area in reservations:
            reservations[area].append(reservation)
        else:
            reservations[area] = [reservation]
        return reservations
    
    def _addExecutionOrder(self, order : list[ServiceArea], newArea):
        if len(order > 0) and order[-1] == newArea:
            return order
        else:
            order.append(newArea)
        return order
    
    def _generatePathReservation(self, activationTime : int, startSite, endSite, serviceRequirement : ServiceRequirement, isLocalSpeed = False) -> ReservationItem:
        duration = GetPathGenerator().CalculateMovementDuration(startSite, endSite, isLocalSpeed)
        return ReservationItem(activationTime, duration, self.company.networkSlice, serviceRequirement)
    
    def _setLocalSpeeds(self, i, maxI) -> tuple[bool, bool]:
        if i == 0:
            return (True, False)
        elif i == maxI:
            return (False, True)
        else:
            return (False, False) 