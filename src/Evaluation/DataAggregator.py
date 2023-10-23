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
        self.failureCounts = self._loadFailureCounts()
        self.filePaths : dict[str, Path]
        self.filePaths = dict()
        
    def aggregate(self):
        self._aggregateSuccessRates()
        self._aggregateNetworkQualities()
        self._aggregateFailureCounts()
        self._aggregateConfigurations()
        
    def _aggregateSuccessRates(self):
        recorder = BasicDataRecorder(0, ['MIN_SUCCESS_RATE', 'MEAN_SUCCESS_RATE', 'MAX_SUCCESS_RATE', 'MAX_LATENCY_SPIKE_DURATION', 'SAMPLE_SIZE'])
        recorder.createFileOutput(GetConfig().filePaths.aggregationPath, 'AggregatedLatencyResults', withOverride=True)
        results = None
        for i in self.latencyResults['MAX_LATENCY_SPIKE_DURATION'].unique():
            data  : DataFrame
            data = self.latencyResults.loc[self.latencyResults['MAX_LATENCY_SPIKE_DURATION'] == i]
            for world in data['WORLD'].unique():
                worldData : DataFrame
                worldData = data.loc[data['WORLD'] == world]
                for seed in worldData['SEED'].unique():
                    sample : DataFrame
                    sample = data.loc[data['SEED'] == seed]
                    entry = [
                        sample['SUCCESS_RATE'].min(),
                        sample['SUCCESS_RATE'].mean(),
                        sample['SUCCESS_RATE'].max(),
                        sample['MAX_LATENCY_SPIKE_DURATION'].min(),
                        len(self.latencyResults['MAX_LATENCY_SPIKE_DURATION'].unique())
                    ]
                    if results is None:
                        results = DataFrame([entry], columns=['MIN_SUCCESS_RATE', 'MEAN_SUCCESS_RATE', 'MAX_SUCCESS_RATE', 'MAX_LATENCY_SPIKE_DURATION', 'SAMPLE_SIZE'])
                    else:
                        results.loc[len(results.index)] = entry
        for duration in results['MAX_LATENCY_SPIKE_DURATION'].unique():
            sample = results.loc[results['MAX_LATENCY_SPIKE_DURATION'] == duration]
            entry = [
                sample['MIN_SUCCESS_RATE'].mean(),
                sample['MEAN_SUCCESS_RATE'].mean(),
                sample['MAX_SUCCESS_RATE'].mean(),
                duration,
                sample['SAMPLE_SIZE'].min()
            ]
            recorder.record(entry)
        recorder.terminate()
        self.filePaths['SUCCESS_RATE'] = recorder.filePath
        
    def _aggregateNetworkQualities(self):
        recorder = BasicDataRecorder(0, ['MAX_LATENCY_SPIKE_DURATION', 'MIN_NETWORK_QUALITY', 'MAX_NETWORK_QUALITY'])
        recorder.createFileOutput(GetConfig().filePaths.aggregationPath, 'AggregatedNetworkQualityResults', withOverride=True)
        networkQualities = self.latencyResults[['MAX_LATENCY_SPIKE_DURATION', 'MIN_NETWORK_QUALITY', 'MAX_NETWORK_QUALITY']]
        for i in networkQualities['MAX_LATENCY_SPIKE_DURATION'].unique():
            data : DataFrame
            data = networkQualities[networkQualities['MAX_LATENCY_SPIKE_DURATION'] == i]
            min = data['MIN_NETWORK_QUALITY'].mean()
            max = data['MAX_NETWORK_QUALITY'].mean()
            recorder.record([i, min, max])
        recorder.terminate()
        self.filePaths['NETWORK_QUALITY'] = recorder.filePath
        
    def _aggregateFailureCounts(self):
        recorder = BasicDataRecorder(0, ["CASE","AREA_FAILS", "PATH_FAILS", "TRAJECTORY_FAILS", "TOTAL_FAILS"])
        recorder.createFileOutput(GetConfig().filePaths.aggregationPath, 'AggregatedFailureCountsResults', withOverride=True)
        recorder2 = BasicDataRecorder(0, ['CASE', 'CAPACITY_FAILS', 'LATENCY_FAILS', 'TOTAL_FAILS'])
        recorder2.createFileOutput(GetConfig().filePaths.aggregationPath, 'AggregatedFailureTypeCountResults', withOverride=True)
        for i in self.failureCounts['CASE'].unique():
            data : DataFrame
            data = self.failureCounts[self.failureCounts['CASE'] == i]
            area = data['AREA_FAILS'].mean()
            path = data['PATH_FAILS'].mean()
            trajectory = data['TRAJECTORY_FAILS'].mean()
            capacity = data['CAPACITY_FAILS'].mean()
            latency = data['LATENCY_FAILS'].mean()
            total = area + path + trajectory
            total2 = capacity + latency
            recorder.record([i, area, path, trajectory, total])
            recorder2.record([i, capacity, latency, total2])
        recorder.terminate()
        recorder2.terminate()
        self.filePaths['ABSOlUTE_ACTIVITY_FAILS'] = recorder.filePath
        self.filePaths['ABSOLUTE_ACTIVITY_TYPE_FAILS'] = recorder2.filePath
        
    def _aggregateConfigurations(self):
        recorder = BasicDataRecorder(0, ['CASE', 'MAX_LATENCY_SPIKE_DURATION'])
        recorder.createFileOutput(GetConfig().filePaths.aggregationPath, 'AggregatedConfigurationResults', withOverride=True)
        for i in self.latencyResults['CASE'].unique():
            data : DataFrame
            data = self.latencyResults[self.latencyResults['CASE'] == i]
            if not len(data['MAX_LATENCY_SPIKE_DURATION'].unique()) == 1:
                raise ValueError("Invalid configuration count")
            recorder.record([i, list(data['MAX_LATENCY_SPIKE_DURATION'].unique())[0]])
        recorder.terminate()
        self.filePaths['CONFIGURATION'] = recorder.filePath
    
    
    def _loadLatencyResults(self) -> DataFrame:
        latencyResults = None
        for file in GetConfig().filePaths.analysisPath.glob('*'):
            if file.match('*LatencyResults*'): #and not file.match('Aggregated*'):
                id = file.name.split('#')[1].split('.')[0]
                if not id.isdigit():
                    raise ValueError("Pattern mismatch: {pattern} should be a number".format(pattern = id))
                worldId = int(id)
                data = pandas.read_csv(file, delimiter=" ")
                data = data.assign(WORLD=worldId)
                if latencyResults is None:
                    latencyResults = data
                else:
                    latencyResults = pandas.concat([latencyResults, data])
        return latencyResults
    
    def _loadFailureCounts(self) -> DataFrame:
        failureCounts = None
        for file in GetConfig().filePaths.analysisPath.glob('*'):
            if file.match('*FailureResults*'):
                id = file.name.split('#')[1].split('.')[0]
                if not id.isdigit():
                    raise ValueError("Pattern mismatch: {pattern} should be a number".format(pattern = id))
                data = pandas.read_csv(file, delimiter=" ")
                if failureCounts is None:
                    failureCounts = data
                else:
                    failureCounts = pandas.concat([failureCounts, data])
        return failureCounts