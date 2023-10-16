from UI.Window import *
from Evaluation.Analyzer import Analyzer
import json
from Configuration.globals import GetConfig
from Configuration.ConfigurationEncoder import ConfigurationEncoder
from pathlib import Path
from datetime import datetime
from DataOutput.BasicDataRecorder import BasicDataRecorder
import Configuration.globals as globals
from Evaluation.Plotter import Plotter
import time

MAX_SPIKE_DURATIONS = [1,2,3,4,5,6,7,8,9,10,12,14,16,20,25,30]
ANALYSIS_PATH = Path.joinpath(Path.cwd(), "Analysis")
BASE_NAME = Path.joinpath(ANALYSIS_PATH, "AnalysisResults-" + datetime.now().strftime("%d-%m-%Y-%H-%M-%S")).name
RECORDER = BasicDataRecorder(0, ["RUN_NO", "MIN_LATENCY_SPIKE_DURATION", "MAX_LATENCY_SPIKE_DURATION",
                                    "SUCCESS_RATE", "MIN_NETWORK_QUALITY", "MAX_NETWORK_QUALITY"])

def setup():
    if(not Path.exists(ANALYSIS_PATH)):
        Path.mkdir(ANALYSIS_PATH)
    RECORDER.createFileOutput(ANALYSIS_PATH, BASE_NAME)


def main():
    for i in range(len(MAX_SPIKE_DURATIONS)):
        startTime = time.time()
        config = Config()
        config.eventConfig.latencySpikeDurationRange = (1, MAX_SPIKE_DURATIONS[i])
        globals.UpdateConfig(config)
        jsonConfig = json.dumps(GetConfig(), cls=ConfigurationEncoder, indent=4)
        with Path.joinpath(GetConfig().filePaths.simulationPath, "Configuration.json").open('w') as configFile:
            configFile.write(jsonConfig)
        window = Window()
        #print(GetConfig().filePaths.simulationPath)
        analyzer = Analyzer(GetConfig().filePaths.simulationPath, window.GetSimulationTime())
        analyzer.analyze()
        #analyzer.printResults()
        analyzer.writeData()
        RECORDER.record([i, 1, MAX_SPIKE_DURATIONS[i], analyzer.qualityAnalyzer.rates.success,
                         analyzer.networkAnalyzer.qualityRange.min, 
                         analyzer.networkAnalyzer.qualityRange.max])
        window.getImage(i)
        print("Executed simulation #" + str(i) + ": " + str(time.time()-startTime) + "s")
    RECORDER.terminate()
    

if __name__ == "__main__":
    setup()
    main()
    Plotter.plot(RECORDER.filePath)