from pathlib import Path
import matplotlib.pyplot as plt
import matplotlib.ticker as mtick
import pandas
from Configuration.globals import GetConfig
import numpy as np
from Evaluation.DataLoader import DataLoader

'''Used to create plots based on aggregated data'''
class AggregationPlotter:
    
    def plotConfigurations(fileName : Path):
        pass
    
    def plotSuccessRate(fileName: Path):        
        data = pandas.read_csv(fileName, delimiter=" ")
        fig1 = plt.figure()
        ax1 = fig1.add_subplot(1,1,1)
        ax1.plot(data['MAX_LATENCY_SPIKE_DURATION'], data['MIN_SUCCESS_RATE'].apply(lambda x : x*100))
        ax1.plot(data['MAX_LATENCY_SPIKE_DURATION'], data['MEAN_SUCCESS_RATE'].apply(lambda x : x*100))
        ax1.plot(data['MAX_LATENCY_SPIKE_DURATION'], data['MAX_SUCCESS_RATE'].apply(lambda x : x*100))
        ax1.legend(['MIN', 'MEAN', 'MAX'])
        ax1.set_title("BP Activity Success Rate")
        ax1.set_xlabel("Max Latency Spike Duration (s)")
        ax1.set_ylabel("Success Rate (%)")
        fig1.add_subplot(ax1)
        
        fig1.savefig(GetConfig().filePaths.plotPath.joinpath('AggregatedSuccessRate.png'))
        
    def plotNetworkQuality(fileName : Path):        
        data = pandas.read_csv(fileName, delimiter=" ")
        fig1 = plt.figure()
        ax1 = fig1.add_subplot(1,1,1)
        ax1.plot(data['MAX_LATENCY_SPIKE_DURATION'], data['MIN_NETWORK_QUALITY'].apply(lambda x : x*100))
        ax1.plot(data['MAX_LATENCY_SPIKE_DURATION'], data['MAX_NETWORK_QUALITY'].apply(lambda x : x*100))
        ax1.legend(["Min. Time", "Max. Time"], loc ="center right")
        ax1.set_title('Normal network operation time ')
        ax1.set_xlabel('Max Latency Spike Duration (s)')
        ax1.set_ylabel('Normal operation time (%)')
        fig1.add_subplot(ax1)
        
        fig1.savefig(GetConfig().filePaths.plotPath.joinpath('AggregatedNetworkQuality.png'))
        
    def plotAbsoluteActivityFailureDistribution(fileName : Path):
        data = pandas.read_csv(fileName, delimiter=" ")
        fig1 = plt.figure()
        ax1 = fig1.add_subplot(1,1,1)
        ax1.plot(data['CASE'], data['AREA_FAILS'])
        ax1.plot(data['CASE'], data['PATH_FAILS'])
        ax1.plot(data['CASE'], data['TRAJECTORY_FAILS'])
        ax1.legend(['Area Fails', 'Path-based Fails', 'Trajectory-based Fails'], loc ="upper left")
        ax1.set_title("Absolute Activity Type Failure Distribution")
        _, end = ax1.get_xlim()
        ax1.xaxis.set_ticks(np.arange(0, end, 1))
        ax1.set_xlabel('Simulation Number (#)')
        ax1.set_ylabel("Failure Count (#)")
        fig1.add_subplot(ax1)
        
        fig1.savefig(GetConfig().filePaths.plotPath.joinpath('AggregatedActivityFailureDistributionAbsolute.png'))
        
    def plotRelativeActivityFailureDistribution(filename : Path):
        data = pandas.read_csv(filename, delimiter=" ")
        fig1 = plt.figure()
        ax1 = fig1.add_subplot(1,1,1)
        ax1.plot(data['CASE'], data['AREA_FAILS'] / data['TOTAL_FAILS'])
        ax1.plot(data['CASE'], data['PATH_FAILS'] / data['TOTAL_FAILS'])
        ax1.plot(data['CASE'], data['TRAJECTORY_FAILS'] / data['TOTAL_FAILS'])
        ax1.legend(['Area Fails', 'Path-based Fails', 'Trajectory-based Fails'], loc='center right')
        ax1.set_title("Relative Activity Type Failure Distribution")
        ax1.set_xlabel('Simulation Number (#)')
        _, end = ax1.get_xlim()
        ax1.xaxis.set_ticks(np.arange(0, end, 1))
        ax1.set_ylabel('Relative Failure Amount (%)')
        fig1.add_subplot(ax1)
        
        fig1.savefig(GetConfig().filePaths.plotPath.joinpath('AggregatedActivityFailureDistributionRelative.png'))
        
    def plotRelativeActivityFailureTypeDistribution(filename : Path):
        data = pandas.read_csv(filename, delimiter=" ")
        fig1 = plt.figure()
        ax1 = fig1.add_subplot(1,1,1)
        ax1.plot(data['CASE'], (data['CAPACITY_FAILS'] / (data['TOTAL_FAILS'])).multiply(100))
        ax1.plot(data['CASE'], (data['LATENCY_FAILS'] /(data['TOTAL_FAILS'])).multiply(100))
        ax1.legend(['Capacity Fails', 'Latency Fails'], loc = 'center left')
        ax1.set_title("Absolute Failure Type Distribution")
        ax1.set_xlabel('Simulation Number (#)')
        ax1.set_ylim(0, 100)
        _, end = ax1.get_xlim()
        ax1.xaxis.set_ticks(np.arange(0, end, 1))
        ax1.set_ylabel("Relative Failure Amount (%)")
        fig1.add_subplot(ax1)
        
        fig1.savefig(GetConfig().filePaths.plotPath.joinpath('AggregatedActivityFailureTypeDistributionRelative.png'))
    
    def plotConfiguration(filename : Path):
        data = pandas.read_csv(filename, delimiter=" ")
        fig1 = plt.figure()
        ax1 = fig1.add_subplot(1,1,1)
        ax1.plot(data['CASE'], data['MAX_LATENCY_SPIKE_DURATION'])
        ax1.legend(['Configuration'])
        ax1.set_title('Configuration settings')
        ax1.set_xlabel('Simulation Number (#)')
        ax1.set_ylabel('Max Latency Spike Duration (s)')
        _, end = ax1.get_xlim()
        ax1.xaxis.set_ticks(np.arange(0, end, 1))
        fig1.add_subplot(ax1)
        
        fig1.savefig(GetConfig().filePaths.plotPath.joinpath('AggregatedConfigurations.png'))
        
    def plotSuccessRateAsBoxPlot():
        data = DataLoader.loadLatencyResults()
        data['SUCCESS_RATE'] = data['SUCCESS_RATE'].apply(lambda x : x * 100)
        fig1 = plt.figure()
        ax1 = fig1.add_subplot(1,1,1)
        ax1.set_title("MBP Activity Success Rate by Spike Duration Range")
        ax1.yaxis.set_major_formatter(mtick.PercentFormatter())
        ax1.set_ylabel("Success Rate (%)")
        ax1.set_xlabel("Maximum Spike Duration Range")
        seriesData = []
        for i in data['MAX_LATENCY_SPIKE_DURATION'].unique():
            seriesData.append(data.loc[data['MAX_LATENCY_SPIKE_DURATION'] == i]['SUCCESS_RATE'])

        ax1.boxplot(seriesData)
        ax1.set_xticklabels(data['MAX_LATENCY_SPIKE_DURATION'].unique())
        fig1.add_subplot(ax1)
        fig1.savefig(GetConfig().filePaths.plotPath.joinpath('SuccessRatesBoxPlot.png'))