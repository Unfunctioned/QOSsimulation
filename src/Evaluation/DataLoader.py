import pandas
from pandas import DataFrame
from Configuration.globals import GetConfig

'''class used to load data from files'''
class DataLoader:
    
    def loadLatencyResults() -> DataFrame:
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
    
    def loadFailureCounts() -> DataFrame:
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