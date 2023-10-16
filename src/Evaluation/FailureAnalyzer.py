from Evaluation.BaseAnalyzer import BaseAnalyzer
from Evaluation.DataStorer import DataStorer, DataType
from dataclasses import dataclass

@dataclass
class FailureTypeCount:
    capacity : int
    latency : int
    
'''Used to analyze QoS failures that occured in the simulation'''
class FailureAnalyzer(BaseAnalyzer):
    
    def __init__(self, dataStorage : DataStorer) -> None:
        self.storage = dataStorage
        self.failureCount = None
    
    def analyze(self):
        data = self.storage.GetData(DataType.FAILURE)
        capacityFailures = data.loc[data['FAILURE_CAUSE'] == 'CAPACITY']
        latencyFailures = data.loc[data['FAILURE_CAUSE'] == 'LATENCY']
        self.failureCount = FailureTypeCount(len(capacityFailures), len(latencyFailures))
        
    
    def printResults(self):
        print("Capacity Failures: " + str(self.failureCount.capacity))
        print("Latency Failures: " + str(self.failureCount.latency))