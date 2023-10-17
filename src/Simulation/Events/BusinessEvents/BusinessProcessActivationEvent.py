from Simulation.Events.BusinessEvents.BusinessEvent import BusinessEvent
from Simulation.BusinessEnvironment.Company import Company
from Simulation.BusinessEnvironment.BusinessProcess import BusinessProcess
from Simulation.Events.BusinessEvents.BusinessEventType import BusinessEventType
'''Used to trigger the activation of business processes'''
class BusinessProcessActivationEvent(BusinessEvent):
    
    def __init__(self, eventTime, company : Company) -> None:
        super().__init__(eventTime, company, None)
        self.company = company
        self.generateFollowUpEvent = True
        
    def trigger(self):
        self.businessProcess = self.company.ActivateBusinessProcess(self.t)
        if not self.businessProcess.activityHistory is None:
            self.businessProcess.activityHistory.record(self.t, [self.businessProcess.id, BusinessEventType.PROCESS_ACTIVATION.name])