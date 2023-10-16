from pathlib import Path
import matplotlib.pyplot as plt
import pandas
from Configuration.globals import GetConfig

'''Used to plot failure distribution by activity type'''
class FailurePlotter:
    
    def plot(fileName : Path):
        plotDataPath = Path.joinpath(Path.cwd(),'Analysis', fileName)
        dateStr = (fileName.name.split('-', 1)[1]).split('.')[0]
        data = pandas.read_csv(plotDataPath, delimiter=" ")
        
        fig1 = plt.figure()
        ax1 = fig1.add_subplot(1,1,1)
        ax1.plot(data['RUN_NO'], data['AREA_FAILS'])
        ax1.plot(data['RUN_NO'], data['PAtH_FAILS'])
        ax1.plot(data['RUN_NO'], data['TRAJECTORY_FAILS'])
        ax1.legend(['Area Fails', 'Path-based Fails', 'Trajectory-based fails'], loc ="lower right")
        ax1.set_title("Absolute Activity Failure Distribution")
        ax1.set_xlabel('Simulation Number (#)')
        ax1.set_ylabel("Failure Count (#)")
        fig1.add_subplot(ax1)
        
        fig2 = plt.figure()
        ax2 = fig1.add_subplot(1,1,1)
        ax2.plot(data['RUN_NO'], data['AREA_FAILS'] / data['TOTAL_FAILS'])
        ax2.plot(data['RUN_NO'], data['PAtH_FAILS'] / data['TOTAL_FAILS'])
        ax2.plot(data['RUN_NO'], data['TRAJECTORY_FAILS'] / data['TOTAL_FAILS'])
        ax2.legend(['Area Fails', 'Path-based Fails', 'Trajectory-based fails'], loc ="lower right")
        ax2.set_title("Relative Activity Failure Distribution")
        ax2.set_xlabel('Simulation Number (#)')
        ax2.set_ylabel("Relative Failure Amount (%)")
        fig2.add_subplot(ax2)
        
        fig1.savefig(GetConfig().filePaths.plotPath.joinpath('FailureDistributionAbsolute-' + dateStr + '.png'))
        fig2.savefig(GetConfig().filePaths.plotPath.joinpath('FailureDistributionRelative-' + dateStr + '.png'))