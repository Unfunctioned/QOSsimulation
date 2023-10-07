from Simulation.Events.Event import Event
from Simulation.BusinessEnvironment.Company import Company
'''Used to trigger the activation of business processes'''
class BusinessProcessActivationEvent(Event):
    
    def __init__(self, eventTime, company : Company) -> None:
        super().__init__(eventTime)
        self.company = company
        
    def trigger(self):
        self.company.ActivateBusinessProcess(self.t)