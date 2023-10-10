from Simulation.BusinessEnvironment.BusinessProcess import BusinessProcess
from Simulation.BusinessEnvironment.Company import Company
from Simulation.Events.BusinessEvents.BusinessEvent import BusinessEvent
from Simulation.Events.BusinessEvents.BusinessEventType import BusinessEventType
'''Triggers a change of business activities in a running business process'''
class ActivityChangeEvent(BusinessEvent):
    
    def __init__(self, eventTime, company: Company, businessProcess: BusinessProcess) -> None:
        super().__init__(eventTime, company, businessProcess)
        self.activatedActivity = None
        self.generateFollowUpEvent = True
        
    def trigger(self):
        try:
            self.activatedActivity = self.businessProcess.ExecuteNext(self.t, self.company.networkSlice)
            if self.activatedActivity is None:
                self.generateFollowUpEvent = False
            self.businessProcess.activityHistory.record(self.t, [self.businessProcess.id, BusinessEventType.ACTIVITY_CHANGE.name])
        except Exception as e:
            e.add_note("In event of type:{eventType}".format(eventType = type(self)))
            raise