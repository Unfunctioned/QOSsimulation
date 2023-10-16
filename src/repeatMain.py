from UI.Window import *
from Evaluation.Analyzer import Analyzer
import json
from Configuration.globals import GetConfig
from Configuration.ConfigurationEncoder import ConfigurationEncoder
import os
from datetime import datetime
from DataOutput.BasicDataRecorder import BasicDataRecorder
import Configuration.globals as globals
import matplotlib.pyplot as plt
import pandas
MAX_SPIKE_DURATIONS = [1,2,3,4,5,6,7,8,9,10,12,14,16,20,25,30]
ANALYSIS_PATH = os.path.join(os.getcwd(), "Analysis")
BASE_NAME = os.path.join(ANALYSIS_PATH, "AnalysisResults-" + datetime.now().strftime("%d-%m-%Y-%H-%M-%S"))
RECORDER = BasicDataRecorder(0, ["RUN_NO", "MIN_LATENXY_SPIKE_DURATION", "MAX_LATENCY_SPIKE_DURATION",
                                    "SUCCESS_RATE", "MIN_NETWORK_QUALITY", "MAX_NETWORK_QUALITY"])

def setup():
    if(not os.path.exists(ANALYSIS_PATH)):
        os.mkdir(ANALYSIS_PATH)
    RECORDER.createFileOutput(ANALYSIS_PATH, BASE_NAME)


def main():
    for i in range(len(MAX_SPIKE_DURATIONS)):
        config = Config()
        config.eventConfig.latencySpikeDurationRange = (1, MAX_SPIKE_DURATIONS[i])
        globals.UpdateConfig(config)
        jsonConfig = json.dumps(GetConfig(), cls=ConfigurationEncoder, indent=4)
        with open(os.path.join(GetConfig().filePaths.simulationPath, "Configuration.json"), 'w') as configFile:
            configFile.write(jsonConfig)
        window = Window()
        print(GetConfig().filePaths.simulationPath)
        analyzer = Analyzer(GetConfig().filePaths.simulationPath, window.GetSimulationTime())
        analyzer.analyze()
        analyzer.printResults()
        analyzer.writeData()
        RECORDER.record([i, 1, MAX_SPIKE_DURATIONS[i], analyzer.qualityAnalyzer.rates.success,
                         analyzer.networkAnalyzer.qualityRange.min, 
                         analyzer.networkAnalyzer.qualityRange.max])
    RECORDER.terminate()
    plotDataPath = RECORDER.filePath
    data = pandas.read_csv(plotDataPath)
    plt.plot(data['RUN_NO'], data['SUCCESS_RATE'])
    

if __name__ == "__main__":
    setup()
    main()