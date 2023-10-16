from Evaluation.DataStorer import DataStorer, DataType
from dataclasses import dataclass
from Evaluation.BaseAnalyzer import BaseAnalyzer

@dataclass
class CountItem:
    '''Used to store histogram data'''
    total: int
    success : int
    failure : int
    
@dataclass
class RateItem:
    '''Used to store activity rate data'''
    success : float
    failure : float

'''Used to analyze the overall QoS during the simulation'''
class QualityAnalyzer(BaseAnalyzer):
    
    def __init__(self, dataStorage : DataStorer) -> None:
        self.storage = dataStorage
        self.counts = CountItem(None, None, None)
        self.rates = RateItem(None, None)
    
    def analyze(self):
        self.counts.total = len(self.storage.GetData(DataType.TERMINATION))
        self.counts.success = len(self.storage.GetData(DataType.SUCCESS))
        self.counts.failure = len(self.storage.GetData(DataType.FAILURE))
        self.rates.success = self.counts.success / self.counts.total
        self.rates.failure = self.counts.failure / self.counts.total
        
    def getResults(self) -> list[str]:
        results = []
        results.append('Activity Count: ' + str(self.counts.total) + "\n")
        results.append('Succeeded: ' + str(self.counts.success) + "\n")
        results.append('Failed: ' + str(self.counts.failure) + "\n")
        results.append('Rate of success: ' + str(self.rates.success * 100) + '%\n')
        results.append('Rate of failure: ' + str(self.rates.failure * 100) + '%\n')
        return results
    
    def printResults(self):
        print(self.counts.total)
        print('Succeeded: ' + str(self.counts.success) + " | Failed: " + str(self.counts.failure))
        print('Rate of success: ' + str(self.rates.success * 100) + '%')
        print('Rate of failure: ' + str(self.rates.failure * 100) + '%')