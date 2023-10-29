from Simulation.Events.BusinessEvents.BusinessEvent import BusinessEvent
from Simulation.BusinessEnvironment.Company import Company
from Simulation.Events.BusinessEvents.BusinessEventType import BusinessEventType
from Simulation.BusinessEnvironment.BusinessProcess import BusinessProcess
'''Used to trigger the activation of business processes'''
class BusinessProcessActivationEvent(BusinessEvent):
    
    def __init__(self, eventTime, company : Company, businessProcess = None) -> None:
        super().__init__(eventTime, company, None)
        self.company = company
        self.businessProcess : BusinessProcess
        self.businessProcess = self.company.GenerateBusinessProcessProcess(eventTime) if businessProcess is None else businessProcess
        self.generateFollowUpEvent = True
        
    def trigger(self):
        if self.company.id == 1245:
            print("Take a break")
        self.businessProcess = self.company.ActivateBusinessProcess(self.t, self.businessProcess)
        if not self.businessProcess.activityHistory is None:
            self.businessProcess.activityHistory.record(self.t, [self.businessProcess.id, BusinessEventType.PROCESS_ACTIVATION.name])