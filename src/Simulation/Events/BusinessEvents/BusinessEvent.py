from Simulation.Events.Event import Event
from Simulation.BusinessEnvironment.Company import Company
from Simulation.BusinessEnvironment.BusinessProcess import BusinessProcess
'''Base class defining business related events'''
class BusinessEvent(Event):
    
    def __init__(self, eventTime, company : Company, businessProcess : BusinessProcess) -> None:
        super().__init__(eventTime)
        self.company = company
        self.businessProcess = businessProcess