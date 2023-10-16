from Evaluation.Plotting.Plotter import Plotter
from pathlib import Path
from datetime import datetime

def main():
    ANALYSIS_PATH = Path.joinpath(Path.cwd(), "Analysis")
    LATENCY = Path.joinpath(ANALYSIS_PATH, "LatencyResults-16-10-2023-21-01-44#0.txt")
    FAILURE = Path.joinpath(ANALYSIS_PATH, "FailureResults-16-10-2023-21-01-44#0.txt")
    LATENCY_PATH = ANALYSIS_PATH.joinpath(LATENCY)
    FAILURE_PATH = ANALYSIS_PATH.joinpath(FAILURE)
    fileName = 'AnalysisResults-16-10-2023-11-39-13#0.txt'
    Plotter.addPath('Latency', LATENCY_PATH)
    Plotter.addPath('Failure', FAILURE_PATH)
    Plotter.plot()

if __name__ == "__main__":
    main()