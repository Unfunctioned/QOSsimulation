from UI.Window import *
from Evaluation.Analyzer import Analyzer
import json
from Configuration.globals import GetConfig
from Configuration.ConfigurationEncoder import ConfigurationEncoder
import os

def main():
    jsonConfig = json.dumps(GetConfig(), cls=ConfigurationEncoder, indent=4)
    with open(os.path.join(GetConfig().filePaths.simulationPath, "Configuration.json"), 'w') as configFile:
        configFile.write(jsonConfig)
    window = Window()
    print(GetConfig().filePaths.simulationPath)
    analyzer = Analyzer(GetConfig().filePaths.simulationPath, window.GetSimulationTime())
    analyzer.analyze()
    analyzer.printResults()
    analyzer.writeData()

if __name__ == "__main__":
    main()