from pathlib import Path
import matplotlib.pyplot as plt
import pandas
from Configuration.globals import GetConfig

'''Used to plot figures for the latency analysis'''
class LatencyPlotter:

    def plot(fileName : Path):
        plotDataPath = Path.joinpath(Path.cwd(),'Analysis', fileName)
        dateStr = (fileName.name.split('-', 1)[1]).split('.')[0]
        data = pandas.read_csv(plotDataPath, delimiter=" ")
        fig1 = plt.figure()
        ax1 = fig1.add_subplot(1,1,1)
        ax1.plot(data['MAX_LATENCY_SPIKE_DURATION'], data['SUCCESS_RATE'].apply(lambda x : x*100))
        ax1.set_title("BP Activity Success Rate")
        ax1.set_xlabel("Max Latency Spike Duration (s)")
        ax1.set_ylabel("Success Rate (%)")
        fig1.add_subplot(ax1)
        
        fig2 = plt.figure()
        ax2 = fig2.add_subplot(1,1,1)
        ax2.plot(data['MAX_LATENCY_SPIKE_DURATION'], data['MIN_NETWORK_QUALITY'].apply(lambda x : x * 100))
        ax2.plot(data['MAX_LATENCY_SPIKE_DURATION'], data['MAX_NETWORK_QUALITY'].apply(lambda x : x * 100))
        ax2.legend(["Min. Quality", "Max. Quality"], loc ="lower right") 
        ax2.set_title('Network Quality')
        ax2.set_xlabel('Max Latency Spike Duration (s)')
        ax2.set_ylabel('Network Quality (%)')
        fig2.add_subplot(ax2)
        
        fig3 = plt.figure()
        ax3 = fig3.add_subplot(1,1,1)
        ax3.plot(data['CASE'], data['MIN_LATENCY_SPIKE_DURATION'])
        ax3.plot(data['CASE'], data['MAX_LATENCY_SPIKE_DURATION'])
        ax3.legend(["Min. Duration", "Max. Duration"], loc ="lower right")
        ax3.set_title('Latency Spike Configurations')
        ax3.set_xlabel('Simulation Number (#)')
        ax3.set_ylabel('Latency Spike Duration (s)')
        fig3.add_subplot(ax3)
        
        fig1.savefig(GetConfig().filePaths.plotPath.joinpath('SuccessRate-' + dateStr + '.png'))
        fig2.savefig(GetConfig().filePaths.plotPath.joinpath('NetworkQuality-' + dateStr + '.png'))
        fig3.savefig(GetConfig().filePaths.plotPath.joinpath('LatencyConfigurations-' + dateStr + '.png'))
        
        fig1.show()
        fig2.show()
        fig3.show()
