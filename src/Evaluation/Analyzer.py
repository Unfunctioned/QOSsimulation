from pathlib import Path
from Configuration.globals import GetConfig
import pandas
from Evaluation.DataStorer import DataStorer, DataType
from Evaluation.QualityAnalyzer import QualityAnalyzer
from Evaluation.SimulationValidator import SimulationValidator
from Evaluation.NetworkAnalyzer import NetworkAnalyzer
from Evaluation.FailureAnalyzer import FailureAnalyzer
from Evaluation.BaseAnalyzer import BaseAnalyzer

'''Used to analyze simulation output'''
class Analyzer(BaseAnalyzer):
    
    def __init__(self, dataPath, totalTime) -> None:
        self.dataPath = dataPath
        self.totalTime = totalTime
        self.storage = DataStorer(self.collectSimulationData())
        self.extractData()
        self.validator = SimulationValidator(self.storage)
        self.qualityAnalyzer = QualityAnalyzer(self.storage)
        self.networkAnalyzer = NetworkAnalyzer(self.dataPath, self.totalTime)
        self.failureAnalyzer = FailureAnalyzer(self.storage)
        self.outputPath = Path.joinpath(GetConfig().filePaths.simulationPath, "Results.txt")
        
    def collectSimulationData(self):
        file = Path.joinpath(self.dataPath, "WorldActivity#-1.txt").open('r')
        return pandas.read_csv(file, delimiter=" ")
    
    def extractData(self):
        data = self.storage.GetData(DataType.ALL)
        self.storage.AddData(DataType.ACTIVATION, data.loc[data['STATUS'] == 'ACTIVATION'])
        self.storage.AddData(DataType.TERMINATION, data.loc[data['STATUS'] != 'ACTIVATION'])
        data = self.storage.GetData(DataType.TERMINATION)
        self.storage.AddData(DataType.SUCCESS, data[data['STATUS'].str.contains(r'.*SUCCESS.*', regex=True)])
        self.storage.AddData(DataType.FAILURE, data[data['STATUS'].str.contains(r'.*FAILURE.*', regex=True)])
        
        
    def printResults(self):
        print(self.dataPath)
        self.qualityAnalyzer.printResults()
        self.networkAnalyzer.printResults()
        self.failureAnalyzer.printResults()
        
    def writeData(self):
        with self.outputPath.open('w') as resultsFile:
            resultsFile.writelines(self.qualityAnalyzer.getResults())
        
        
    def analyze(self):
        try:
            self.validator.validate()
        except Exception as e:
            e.add_note("Invalid simulation ouput")
            raise e
        self.qualityAnalyzer.analyze()
        self.networkAnalyzer.analyze()
        self.failureAnalyzer.analyze()
        self.storage = None
        
    def get_analyzers(self):
        return self.networkAnalyzer, self.qualityAnalyzer, self.failureAnalyzer
        
        