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
    
    def loadTimeResults() -> DataFrame:
        columns = ['WORLD', 'SEED', 'CASE_ID', 'TIME']
        timeData = []
        path = GetConfig().filePaths.storagePath
        for world in path.iterdir():
            i = 0
            for run in world.iterdir():
                path = run.joinpath("WorldActivity#-1.txt")
                if not path.exists():
                    continue
                data = pandas.read_csv(path, delimiter=" ")
                splits = str(path).split('#')
                last_row = data.iloc[-1]
                seed = splits[2].split('\\')[0]
                entry = [splits[1], seed, i, last_row['TIME']]
                timeData.append(entry)
                i += 1
        dataframe = DataFrame(timeData)
        dataframe.columns = columns
        return dataframe