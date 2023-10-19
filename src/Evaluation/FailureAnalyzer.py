from Evaluation.BaseAnalyzer import BaseAnalyzer
from Evaluation.DataStorer import DataStorer, DataType
from dataclasses import dataclass

@dataclass
class FailureTypeCount:
    capacity : int
    latency : int
    
@dataclass
class ActivityTypeFailureCount:
    area: int
    path: int
    trajectory: int
    total: int
    
'''Used to analyze QoS failures that occured in the simulation'''
class FailureAnalyzer(BaseAnalyzer):
    
    def __init__(self, dataStorage : DataStorer) -> None:
        self.data = dataStorage.GetData(DataType.FAILURE)
        self.failureCount = None
        self.acitivityFailureCount = None
    
    def analyze(self):
        data = self.data
        capacityFailures = data.loc[data['FAILURE_CAUSE'] == 'CAPACITY']
        latencyFailures = data.loc[data['FAILURE_CAUSE'] == 'LATENCY']
        self.failureCount = FailureTypeCount(len(capacityFailures), len(latencyFailures))
        areaActivityFailures = data.loc[data['ACTIVITY_TYPE'] == 'AREA']
        pathActivityFailures = data.loc[data['ACTIVITY_TYPE'] == 'PATH']
        trajectoryActivityFailures = data.loc[data['ACTIVITY_TYPE'] == 'TRAJECTORY']
        if not len(data) == len(areaActivityFailures) + len(pathActivityFailures) + len(trajectoryActivityFailures):
            raise ValueError("Inconsistent failure distribution")
        self.acitivityFailureCount = ActivityTypeFailureCount(
                len(areaActivityFailures), len(pathActivityFailures),
                len(trajectoryActivityFailures), len(data)
            )
        
    
    def printResults(self):
        print("Capacity Failures: " + str(self.failureCount.capacity))
        print("Latency Failures: " + str(self.failureCount.latency))