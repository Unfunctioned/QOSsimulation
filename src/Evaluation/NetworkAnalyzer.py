from pathlib import Path
from Configuration.globals import GetConfig
import pandas
from pandas import DataFrame, Series
from Evaluation.BaseAnalyzer import BaseAnalyzer
from dataclasses import dataclass

@dataclass
class QualityRangeItem:
    min: float
    max: float
'''Used to analyze the network performance of the local service networks'''
class NetworkAnalyzer(BaseAnalyzer):
    
    def __init__(self, dataPath : Path, totalTime) -> None:
        self.totalTime = totalTime
        self.dataPath = dataPath
        self.networkData : dict[str, DataFrame]
        self.networkData = self.extractData()
        self.results = None
        self.qualityRange = QualityRangeItem(2.0, -1.0)
        
    def extractData(self):
        data = dict()
        networkPath = self.dataPath.joinpath("LocalServiceNetworks")
        for directory in networkPath.glob('*'):
            index = directory.name.split('#')[1]
            filePath = networkPath.joinpath(directory, 'QualityHistory#' + index + '.txt')
            csv = open(filePath, 'r')
            data[index] = pandas.read_csv(csv, delimiter=" ")
        return data
    
    def analyze(self):
        qualityMap = dict()
        for key in self.networkData:
            totalViolationTime = 0
            data = self.networkData[key]
            rowCount = len(data)
            altData = data.loc[data['Latency'] > GetConfig().serviceConfig.LATENCY_DEFAULT]
            violationTimeData = altData.apply(lambda x : self.Duration(rowCount, x, data), axis=1)
            totalViolationTime = violationTimeData.sum()       
            qualityValue = (self.totalTime - totalViolationTime) / self.totalTime
            qualityMap[key] = qualityValue
            if qualityValue < self.qualityRange.min:
                self.qualityRange.min = qualityValue
            if qualityValue > self.qualityRange.max:
                self.qualityRange.max = qualityValue 
        self.results = pandas.DataFrame.from_dict(qualityMap, orient='index')
        
    def Duration(self, rowCount : int, currentRow : Series, data : DataFrame) -> int:
        data.reset_index()
        duration = 0
        currentTime = currentRow['TIME']
        if not currentRow.name < rowCount - 1:
            duration = self.totalTime - currentTime
        else:
            nextIndex = currentRow.name + 1
            nextRow = data.loc[nextIndex]
            nextTime = nextRow['TIME']
            duration = nextTime - currentTime
        return duration
        
    def printResults(self):
        print("Network quality range: " + str(self.qualityRange.min) + " - " + str(self.qualityRange.max))
                
                
                