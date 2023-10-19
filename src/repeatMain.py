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

MAX_SPIKE_DURATIONS = [1,2,3,4,5] #,6,7,8,9,10,12,14,16,20,25,30]
WORLD_COUNT = 5
SEEDS = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
SNAPSHOTS = []
    
def initLatencyRecording(worldId):
    name = Path.joinpath(GetConfig().filePaths.analysisPath, "LatencyResults-" + datetime.now().strftime("%d-%m-%Y-%H-%M-%S")).name
    recorder = BasicDataRecorder(worldId, ["RUN_NO", "MIN_LATENCY_SPIKE_DURATION", "MAX_LATENCY_SPIKE_DURATION",
                                    "SUCCESS_RATE", "MIN_NETWORK_QUALITY", "MAX_NETWORK_QUALITY"])
    recorder.createFileOutput(GetConfig().filePaths.analysisPath, name)
    return recorder
    
def initFailureRecording(worldId):
    name = Path.joinpath(GetConfig().filePaths.analysisPath, "FailureResults-" + datetime.now().strftime("%d-%m-%Y-%H-%M-%S")).name
    recorder = BasicDataRecorder(worldId, ["RUN_NO", "AREA_FAILS", "PATH_FAILS", "TRAJECTORY_FAILS", 
                                         "TOTAL_FAILS", "CAPACITY_FAILS", "LATENCY_FAILS"])
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
    
def initLatencyConfig(worldId : int, iterationNo, seedValue : int):
    if iterationNo > 0:
        initWorldConfig(worldId, seedValue, Config(worldId, seedValue))
    config = GetConfig()
    if not config.randoms.seeds[0] == worldId:
        raise ValueError("Invalid seed configuration")
    config.eventConfig.latencySpikeDurationRange = (1, MAX_SPIKE_DURATIONS[iterationNo])
    globals.UpdateConfig(config)
    
def iterateCases(durations, worldId, seedValue):
    initWorldConfig(worldId, seedValue)
    latencyRecorder = initLatencyRecording(worldId)
    failureRecorder = initFailureRecording(worldId)
    for i in range(len(durations)):
        startTime = time.time()
        runWorld([worldId, seedValue], [latencyRecorder, failureRecorder], durations[i], i)
        print("Executed World #" + str(worldId) + " Seed#" + str(seedValue) + " Case#" + str(i) + ": " + str(time.time()-startTime) + "s")
    
    latencyRecorder.terminate()
    failureRecorder.terminate()

def runWorld(values, recorders : list[BasicDataRecorder], spikeDuration : int, caseNo : int):
        initLatencyConfig(values[0], caseNo, values[1])
        with Path.joinpath(GetConfig().filePaths.simulationPath, "Configuration.json").open('w') as configFile:
            configFile.write(json.dumps(GetConfig(), cls=ConfigurationEncoder, indent=4))
        generator = WorldGenerator()
        world = generator.get_world()
        simulate(world, caseNo)
        analyzeWorld(recorders, world.GetSimulationTime(), spikeDuration, caseNo)
        
def simulate(world : World, caseNo : int):
    window = Window(world)
    window.getImage(caseNo)
    window.animate()
    
        
def analyzeWorld(recorders : list[BasicDataRecorder], totalTime, spikeDuration, caseNo):
        analyzer = Analyzer(GetConfig().filePaths.simulationPath, totalTime)
        analyzer.analyze()
        analyzer.writeData()
        nA, qA, fA = analyzer.get_analyzers()
        recorders[0].record([caseNo, 1, spikeDuration, qA.rates.success,
                        nA.qualityRange.min, 
                        nA.qualityRange.max])
        recorders[1].record([caseNo, fA.acitivityFailureCount.area,
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
    AggregationPlotter.plot(aggregator.filePaths['SUCCESS_RATE'])