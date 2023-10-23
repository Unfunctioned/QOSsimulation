from Evaluation.Plotting.Plotter import Plotter
from pathlib import Path

def main():
    ANALYSIS_PATH = Path.joinpath(Path.cwd(), "Analysis")
    LATENCY = Path.joinpath(ANALYSIS_PATH, "LatencyResults-20-10-2023-16-01-10#1.txt")
    FAILURE = Path.joinpath(ANALYSIS_PATH, "FailureResults-20-10-2023-16-01-10#1.txt")
    LATENCY_PATH = ANALYSIS_PATH.joinpath(LATENCY)
    FAILURE_PATH = ANALYSIS_PATH.joinpath(FAILURE)
    Plotter.addPath('Latency', LATENCY_PATH)
    Plotter.addPath('Failure', FAILURE_PATH)
    Plotter.plot()

if __name__ == "__main__":
    main()