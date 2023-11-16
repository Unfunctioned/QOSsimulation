from UI.Window import *
from Evaluation.Analyzer import Analyzer
import json
from Configuration.globals import GetConfig
from Configuration.ConfigurationEncoder import ConfigurationEncoder
from pathlib import Path
from Simulation.WorldGenerator import WorldGenerator
import time

def main():
    startTime = time.time()
    jsonConfig = json.dumps(GetConfig(), cls=ConfigurationEncoder, indent=4)
    with Path.joinpath(GetConfig().filePaths.simulationPath, "Configuration.json").open('w') as configFile:
        configFile.write(jsonConfig)
    world = WorldGenerator().get_world()
    window = Window(world, False)
    window.animate()
    print(GetConfig().filePaths.simulationPath)
    analyzer = Analyzer(GetConfig().filePaths.simulationPath, window.GetSimulationTime())
    analyzer.analyze()
    analyzer.printResults()
    analyzer.writeData()
    print("Duration: " + str(time.time()-startTime) + "s")

if __name__ == "__main__":
    main()