from Simulation.Events.BusinessEvents.BusinessEvent import BusinessEvent
from Simulation.BusinessEnvironment.BusinessActivity import PathBasedActivity
from Simulation.PhysicalEnvironment.ServiceArea import ServiceArea
from Simulation.BusinessEnvironment.Company import Company
from Simulation.BusinessEnvironment.BusinessProcess import BusinessProcess

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
        if currentPosition == len(path) - 1:
            self.completed = True
            return
        try:
            networkSlice = self.company.networkSlice
            path[currentPosition + 1].ActivateNetworkSlice(self.t, networkSlice, serviceRequirement)
            path[currentPosition].DeactivateNetworkSlice(self.t, networkSlice, serviceRequirement)
        except Exception as e:
            e.add_note("In event of type:{eventType}".format(eventType = type(self)))
            raise