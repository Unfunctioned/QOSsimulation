from pathlib import Path
import matplotlib.pyplot as plt
import pandas
from Configuration.globals import GetConfig
'''Used to create plots based on aggregated data'''
class AggregationPlotter:
    
    def plot(fileName: Path):        
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