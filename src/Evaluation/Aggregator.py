from pathlib import Path
from Configuration.globals import GetConfig
from datetime import datetime
import pandas
from pandas import DataFrame
from DataOutput.BasicDataRecorder import BasicDataRecorder
from Evaluation.DataLoader import DataLoader

'''Used to aggregate analysis results'''
class Aggregator(object):
    
    def __init__(self) -> None:
        self.latencyResults = DataLoader.loadLatencyResults()
        self.failureCounts = DataLoader.loadFailureCounts()
        self.filePaths : dict[str, Path]
        self.filePaths = dict()
        
    def aggregate(self):
        self._aggregateSuccessRates()
        
    def _aggregateSuccessRates(self):
        recorder = BasicDataRecorder(0, ["CASE_NO", "SUCCESS_RATE"])
        recorder.createFileOutput(GetConfig().filePaths.aggregationPath, 'AggregatedSuccessRates', withOverride=True)
        
        for i in self.latencyResults['MAX_LATENCY_SPIKE_DURATION'].unique():
            data : DataFrame
            data = self.latencyResults.loc[self.latencyResults['MAX_LATENCY_SPIKE_DURATION'] == i]
        
        