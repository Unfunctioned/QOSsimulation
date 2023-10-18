from UI.Window import *
from Evaluation.Analyzer import Analyzer
import json
from Configuration.globals import GetConfig
from Configuration.ConfigurationEncoder import ConfigurationEncoder
from pathlib import Path
from datetime import datetime
from DataOutput.BasicDataRecorder import BasicDataRecorder
import Configuration.globals as globals
from Evaluation.Plotting.Plotter import Plotter
import time
from Evaluation.DataAggregator import DataAggregator
from Evaluation.Plotting.AggregationPlotter import AggregationPlotter

global LATENCY_RECORDER
LATENCY_RECORDER = None

global FAILURE_RECORDER
FAILURE_RECORDER = None

MAX_SPIKE_DURATIONS = [1,2,3,4,5] #[1,2,3,4,5,6,7,8,9,10,12,14,16,20,25,30]
WORLD_COUNT = len(MAX_SPIKE_DURATIONS)
SEEDS = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    
def initLatencyRecording(worldId):
    name = Path.joinpath(GetConfig().filePaths.analysisPath, "LatencyResults-" + datetime.now().strftime("%d-%m-%Y-%H-%M-%S")).name
    recorder = BasicDataRecorder(worldId, ["RUN_NO", "MIN_LATENCY_SPIKE_DURATION", "MAX_LATENCY_SPIKE_DURATION",
                                    "SUCCESS_RATE", "MIN_NETWORK_QUALITY", "MAX_NETWORK_QUALITY"])
    recorder.createFileOutput(GetConfig().filePaths.analysisPath, name)
    global LATENCY_RECORDER
    LATENCY_RECORDER = recorder
    
def initFailureRecording(worldId):
    name = Path.joinpath(GetConfig().filePaths.analysisPath, "FailureResults-" + datetime.now().strftime("%d-%m-%Y-%H-%M-%S")).name
    recorder = BasicDataRecorder(worldId, ["RUN_NO", "AREA_FAILS", "PATH_FAILS", "TRAJECTORY_FAILS", 
                                         "TOTAL_FAILS", "CAPACITY_FAILS", "LATENCY_FAILS"])
    recorder.createFileOutput(GetConfig().filePaths.analysisPath, name)
    global FAILURE_RECORDER
    FAILURE_RECORDER = recorder

def initWorldConfig(worldId : int, seedValue : int, config : Config = GetConfig()):
    if not worldId == 0 or not config.filePaths.seedId == seedValue:
        config = Config(worldId, seedValue)
    seeds = SEEDS.copy()
    seeds[0] = worldId
    seeds[1] = worldId
    for i in range(2, len(seeds)):
        seeds[i] = seedValue
    config.setSeeds(seeds)
    globals.UpdateConfig(config)
    
def initLatencyConfig(worldId : int, iterationNo, seedValue : int):
    if iterationNo > 0:
        initWorldConfig(worldId, seedValue, Config(worldId, seedValue))
    config = GetConfig()
    if not config.randoms.seeds[0] == worldId:
        raise ValueError("Invalid seed configuration")
    config.eventConfig.latencySpikeDurationRange = (1, MAX_SPIKE_DURATIONS[iterationNo])
    globals.UpdateConfig(config)

def runWorld(durations, worldId, seedValue):
    for i in range(len(durations)):
        startTime = time.time()
        initLatencyConfig(worldId, i, seedValue)
        jsonConfig = json.dumps(GetConfig(), cls=ConfigurationEncoder, indent=4)
        with Path.joinpath(GetConfig().filePaths.simulationPath, "Configuration.json").open('w') as configFile:
            configFile.write(jsonConfig)
        window = Window()
        #print(GetConfig().filePaths.simulationPath)
        analyzer = Analyzer(GetConfig().filePaths.simulationPath, window.GetSimulationTime())
        analyzer.analyze()
        #analyzer.printResults()
        analyzer.writeData()
        LATENCY_RECORDER.record([i, 1, durations[i], analyzer.qualityAnalyzer.rates.success,
                        analyzer.networkAnalyzer.qualityRange.min, 
                        analyzer.networkAnalyzer.qualityRange.max])
        FAILURE_RECORDER.record([i, analyzer.failureAnalyzer.acitivityFailureCount.area,
                        analyzer.failureAnalyzer.acitivityFailureCount.path,
                        analyzer.failureAnalyzer.acitivityFailureCount.trajectory,
                        analyzer.failureAnalyzer.acitivityFailureCount.total,
                        analyzer.failureAnalyzer.failureCount.capacity,
                        analyzer.failureAnalyzer.failureCount.latency])
        window.getImage(i)
        print("Executed World #" + str(worldId) + " Seed#" + str(seedValue) + " Case#" + str(i) + ": " + str(time.time()-startTime) + "s")
    LATENCY_RECORDER.terminate()
    FAILURE_RECORDER.terminate()


def main():
    for worldId in range(WORLD_COUNT):
        for i in range(WORLD_COUNT):
            initLatencyRecording(worldId)
            initFailureRecording(worldId)        
            initWorldConfig(worldId, i)
            runWorld(MAX_SPIKE_DURATIONS, worldId, i)
        print("World #" + str(worldId) + " complete")
    

if __name__ == "__main__":
    main()
    Plotter.addPath('Latency', LATENCY_RECORDER.filePath)
    Plotter.addPath('Failure', FAILURE_RECORDER.filePath)
    Plotter.plot()
    aggregator = DataAggregator()
    aggregator.aggregate()
    AggregationPlotter.plot(aggregator.filePaths['SUCCESS_RATE'])