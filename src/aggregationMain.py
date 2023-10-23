from Evaluation.DataAggregator import DataAggregator
from Evaluation.Plotting.AggregationPlotter import AggregationPlotter

def main():
    aggregator = DataAggregator()
    aggregator.aggregate()
    AggregationPlotter.plotSuccessRate(aggregator.filePaths['SUCCESS_RATE'])
    AggregationPlotter.plotNetworkQuality(aggregator.filePaths['NETWORK_QUALITY'])
    AggregationPlotter.plotAbsoluteActivityFailureDistribution(aggregator.filePaths['ABSOlUTE_ACTIVITY_FAILS'])
    AggregationPlotter.plotRelativeActivityFailureDistribution(aggregator.filePaths['ABSOlUTE_ACTIVITY_FAILS'])
    AggregationPlotter.plotRelativeActivityFailureTypeDistribution(aggregator.filePaths['ABSOLUTE_ACTIVITY_TYPE_FAILS'])
    AggregationPlotter.plotConfiguration(aggregator.filePaths['CONFIGURATION'])

if __name__ == "__main__":
    main()