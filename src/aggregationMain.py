from Evaluation.DataAggregator import DataAggregator
from Evaluation.Plotting.AggregationPlotter import AggregationPlotter

def main():
    aggregator = DataAggregator()
    aggregator.aggregate()
    AggregationPlotter.plot(aggregator.filePaths['SUCCESS_RATE'])

if __name__ == "__main__":
    main()