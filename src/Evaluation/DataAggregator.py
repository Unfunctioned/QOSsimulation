from pathlib import Path
from Configuration.globals import GetConfig
from datetime import datetime
import pandas
from pandas import DataFrame
from DataOutput.BasicDataRecorder import BasicDataRecorder

'''Used to aggregate analysis results'''
class DataAggregator(object):
    
    def __init__(self) -> None:
        self.latencyResults = self._loadLatencyResults()
        self.filePaths : dict[str, Path]
        self.filePaths = dict()
        
    def aggregate(self):
        self._aggregateSuccessRates()
        
    def _aggregateSuccessRates(self):
        recorder = BasicDataRecorder(0, ['MIN_SUCCESS_RATE', 'MEAN_SUCCESS_RATE', 'MAX_SUCCESS_RATE', 'MAX_LATENCY_SPIKE_DURATION', 'SAMPLE_SIZE'])
        recorder.createFileOutput(GetConfig().filePaths.aggregationPath, 'AggregatedLatencyResults', withOverride=True)
        for i in range(int(self.latencyResults['RUN_NO'].max()) + 1):
            data = self.latencyResults.loc[self.latencyResults['RUN_NO'] == i]
            results = [
                data['SUCCESS_RATE'].min(),
                data['SUCCESS_RATE'].mean(),
                data['SUCCESS_RATE'].max(),
                data['MAX_LATENCY_SPIKE_DURATION'].min(),
                pandas.unique(data['MAX_LATENCY_SPIKE_DURATION'])[0]
            ]
            recorder.record(results)
        recorder.terminate()
        self.filePaths['SUCCESS_RATE'] = recorder.filePath
        
    
    
    def _loadLatencyResults(self) -> DataFrame:
        latencyResults = None
        for file in GetConfig().filePaths.analysisPath.glob('*'):
            if file.match('*LatencyResults*') and not file.match('Aggregated*'):
                id = file.name.split('#')[1].split('.')[0]
                if not id.isdigit():
                    raise ValueError("Pattern mismatch: {pattern} should be a number".format(pattern = id))
                data = pandas.read_csv(file, delimiter=" ")
                data = data.assign(WORLD=id)
                if latencyResults is None:
                    latencyResults = data
                else:
                    latencyResults = pandas.concat([latencyResults, data])
        return latencyResults