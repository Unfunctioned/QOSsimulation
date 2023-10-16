from pathlib import Path
from Evaluation.Plotting.LatencyPlotting import LatencyPlotter
from Evaluation.Plotting.FailurePlotter import FailurePlotter

class Plotter:
    
    filePaths = dict()
    
    def addPath(key : str, path : Path):
        Plotter.filePaths[key] = path
  
    def plot():
        LatencyPlotter.plot(Plotter.filePaths['Latency'])
        FailurePlotter.plot(Plotter.filePaths['Failure'])