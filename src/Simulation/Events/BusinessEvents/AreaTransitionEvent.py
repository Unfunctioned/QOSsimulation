from Simulation.Events.BusinessEvents.BusinessEvent import BusinessEvent
from Simulation.BusinessEnvironment.BusinessActivity import PathBasedActivity
from Simulation.PhysicalEnvironment.ServiceArea import ServiceArea
from Simulation.BusinessEnvironment.Company import Company
from Simulation.BusinessEnvironment.BusinessProcess import BusinessProcess
from Simulation.Events.BusinessEvents.BusinessEventType import BusinessEventType

'''Event to cause a transition between neigbouring service areas for a mobile unit'''
class AreaTransitionEvent(BusinessEvent):
    
    def __init__(self, eventTime, company : Company, businessProcess : BusinessProcess, 
                 currentActivity : PathBasedActivity, transitionPoint) -> None:
        super().__init__(eventTime, company, businessProcess)
        self.currentActivity = currentActivity
        self.transitionPoint = transitionPoint
        self.generateFollowUpEvent = True
        self.completed = False
        
    def trigger(self):
        serviceRequirement = self.currentActivity.serviceRequirement
        currentPosition = self.currentActivity.currentPosition
        path : list[ServiceArea]
        path = self.currentActivity.movementPath
        try:
            networkSlice = self.company.networkSlice
            path[currentPosition + 1].ActivateNetworkSlice(self.t, networkSlice, serviceRequirement)
            path[currentPosition].DeactivateNetworkSlice(self.t, networkSlice, serviceRequirement)
            if not self.businessProcess.activityHistory is None:
                self.businessProcess.activityHistory.record(self.t, [self.businessProcess.id, BusinessEventType.AREA_TRANSITION])
            self.currentActivity.currentPosition += 1
            if self.currentActivity.currentPosition == len(path) - 1:
                self.completed = True
        except Exception as e:
            e.add_note("In event of type:{eventType}".format(eventType = type(self)))
            raise