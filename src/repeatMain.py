from UI.Window import Window
from Evaluation.Analyzer import Analyzer
import json
from Configuration.globals import GetConfig, Config
from Configuration.ConfigurationEncoder import ConfigurationEncoder
from pathlib import Path
from datetime import datetime
from DataOutput.BasicDataRecorder import BasicDataRecorder
import Configuration.globals as globals
import time
from Simulation.WorldGenerator import WorldGenerator
from Evaluation.DataAggregator import DataAggregator
from Evaluation.Plotting.AggregationPlotter import AggregationPlotter
from Simulation.World import World
from memory_profiler import profile

MAX_SPIKE_DURATIONS = [1,2,3,4,5,6,7,8,9,10,12,14,16,20,25,30]
WORLD_COUNT = 10
SEEDS = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
SNAPSHOTS = []
    
def initLatencyRecording(worldId):
    name = Path.joinpath(GetConfig().filePaths.analysisPath, "LatencyResults-" + datetime.now().strftime("%d-%m-%Y-%H-%M-%S")).name
    recorder = BasicDataRecorder(worldId, ["WORLD", "SEED", "CASE", "MIN_LATENCY_SPIKE_DURATION", "MAX_LATENCY_SPIKE_DURATION",
                                    "SUCCESS_RATE", "MIN_NETWORK_QUALITY", "MAX_NETWORK_QUALITY"])
    recorder.createFileOutput(GetConfig().filePaths.analysisPath, name)
    return recorder
    
def initFailureRecording(worldId):
    name = Path.joinpath(GetConfig().filePaths.analysisPath, "FailureResults-" + datetime.now().strftime("%d-%m-%Y-%H-%M-%S")).name
    recorder = BasicDataRecorder(worldId, ["WORLD", "SEED", "CASE", "AREA_FAILS", "PATH_FAILS", "TRAJECTORY_FAILS", 
                                         "TOTAL_FAILS", "CAPACITY_FAILS", "LATENCY_FAILS"])
    recorder.createFileOutput(GetConfig().filePaths.analysisPath, name)
    return recorder

def initNetworkQualityRecording(worldId):
    name = Path.joinpath(GetConfig().filePaths.analysisPath, "NetworkQualityResults-" + datetime.now().strftime("%d-%m-%Y-%H-%M-%S")).name
    recorder = BasicDataRecorder(worldId, ['RUN_NO', 'SEED_NO', 'AREA_ID', 'MIN_QUALITY', 'MAX_QUALITY'])
    recorder.createFileOutput(GetConfig().filePaths.analysisPath, name)
    return recorder

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
    
def initLatencyConfig(caseID : tuple[int,int,int]):
    if caseID[2] > 0:
        initWorldConfig(caseID[0], caseID[1], Config(caseID[0], caseID[1]))
    config = GetConfig()
    if not config.randoms.seeds[0] == caseID[0]:
        raise ValueError("Invalid seed configuration")
    config.eventConfig.latencySpikeDurationRange = (1, MAX_SPIKE_DURATIONS[caseID[2]])
    globals.UpdateConfig(config)
    
def iterateCases(durations, worldId, seedValue):
    initWorldConfig(worldId, seedValue)
    latencyRecorder = initLatencyRecording(worldId)
    failureRecorder = initFailureRecording(worldId)
    networkQualityRecorder = initNetworkQualityRecording(worldId)
    for i in range(len(durations)):
        startTime = time.time()
        runWorld((worldId, seedValue, i), [latencyRecorder, failureRecorder, networkQualityRecorder], durations[i])
        print("Executed World #" + str(worldId) + " Seed#" + str(seedValue) + " Case#" + str(i) + ": " + str(time.time()-startTime) + "s")
    
    latencyRecorder.terminate()
    failureRecorder.terminate()

def runWorld(caseID : tuple[int,int,int], recorders : list[BasicDataRecorder], spikeDuration : int):
        initLatencyConfig(caseID)
        with Path.joinpath(GetConfig().filePaths.simulationPath, "Configuration.json").open('w') as configFile:
            configFile.write(json.dumps(GetConfig(), cls=ConfigurationEncoder, indent=4))
        generator = WorldGenerator()
        world = generator.get_world()
        simulate(world, caseID[2])
        analyzeWorld(recorders, world.GetSimulationTime(), spikeDuration, caseID)
        
def simulate(world : World, caseNo : int):
    window = Window(world)
    window.getImage(caseNo)
    window.animate()
    
        
def analyzeWorld(recorders : list[BasicDataRecorder], totalTime, spikeDuration, caseID : tuple[int,int,int]):
        analyzer = Analyzer(GetConfig().filePaths.simulationPath, totalTime)
        analyzer.analyze()
        analyzer.writeData()
        nA, qA, fA = analyzer.get_analyzers()
        recorders[0].record([caseID[0], caseID[1], caseID[2], 1, spikeDuration, qA.rates.success,
                        nA.qualityRange.min, 
                        nA.qualityRange.max])
        recorders[1].record([caseID[0], caseID[1], caseID[2], fA.acitivityFailureCount.area,
                        fA.acitivityFailureCount.path,
                        fA.acitivityFailureCount.trajectory,
                        fA.acitivityFailureCount.total,
                        fA.failureCount.capacity,
                        fA.failureCount.latency])
    
def iterateSeeds(worldId):
    for seed in range(WORLD_COUNT):
        iterateCases(MAX_SPIKE_DURATIONS, worldId, seed)
        
    
def main():
    for worldId in range(WORLD_COUNT):
        iterateSeeds(worldId)
        print("World #" + str(worldId) + " complete")
    

if __name__ == "__main__":
    main()
    aggregator = DataAggregator()
    aggregator.aggregate()
    AggregationPlotter.plotSuccessRate(aggregator.filePaths['SUCCESS_RATE'])
    AggregationPlotter.plotNetworkQuality(aggregator.filePaths['NETWORK_QUALITY'])
    AggregationPlotter.plotAbsoluteActivityFailureDistribution(aggregator.filePaths['ABSOlUTE_ACTIVITY_FAILS'])
    AggregationPlotter.plotRelativeActivityFailureDistribution(aggregator.filePaths['ABSOlUTE_ACTIVITY_FAILS'])
    AggregationPlotter.plotRelativeActivityFailureTypeDistribution(aggregator.filePaths['ABSOLUTE_ACTIVITY_TYPE_FAILS'])
    AggregationPlotter.plotConfiguration(aggregator.filePaths['CONFIGURATION'])
    AggregationPlotter.plotSuccessRateAsBoxPlot()