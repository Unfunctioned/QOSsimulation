import os
from Configuration.globals import GetConfig
import pandas
from pandas import DataFrame
from Evaluation.BaseAnalyzer import BaseAnalyzer
from dataclasses import dataclass

@dataclass
class QualityRangeItem:
    min: float
    max: float
'''Used to analyze the network performance of the local service networks'''
class NetworkAnalyzer(BaseAnalyzer):
    
    def __init__(self, dataPath, totalTime) -> None:
        self.totalTime = totalTime
        self.dataPath = dataPath
        self.networkData : dict[str, DataFrame]
        self.networkData = self.extractData()
        self.results = None
        self.qualityRange = QualityRangeItem(2.0, -1.0)
        
    def extractData(self):
        data = dict()
        networkPath = os.path.join(self.dataPath, "LocalServiceNetworks")
        for directory in os.listdir(networkPath):
            index = directory.split('#')[1]
            filePath = os.path.join(networkPath, directory, 'QualityHistory#' + index + '.txt')
            csv = open(filePath, 'r')
            data[index] = pandas.read_csv(csv, delimiter=" ")
        return data
    
    def analyze(self):
        qualityMap = dict()
        qualityRange = (2.0, -1.0)
        for key in self.networkData:
            totalViolationTime = 0
            data = self.networkData[key]
            for i in range(len(data)):
                currentRow = data.iloc[i]
                duration = 0
                if currentRow['Latency'] > GetConfig().serviceConfig.LATENCY_DEFAULT:
                    if not i < len(data) - 1:
                        duration = self.totalTime - currentRow['TIME']
                    else:
                        nextRow = data.iloc[i + 1]
                        duration = nextRow['TIME'] - currentRow['TIME']
                    totalViolationTime += duration
                    
            qualityValue = (self.totalTime - totalViolationTime) / self.totalTime
            qualityMap[key] = qualityValue
            if qualityValue < self.qualityRange.min:
                self.qualityRange.min = qualityValue
            if qualityValue > self.qualityRange.max:
                self.qualityRange.max = qualityValue 
        self.results = pandas.DataFrame.from_dict(qualityMap, orient='index')
        
    def printResults(self):
        print("Network quality range: " + str(self.qualityRange.min) + " - " + str(self.qualityRange.max))
                
                
                