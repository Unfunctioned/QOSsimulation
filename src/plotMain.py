import os
import matplotlib.pyplot as plt
import pandas    
  
def main():
    if not os.path.exists(os.path.join(os.getcwd(), 'Plots')):
        os.mkdir(os.path.join(os.getcwd(), 'Plots'))
    fileName = 'AnalysisResults-16-10-2023-11-39-13#0.txt'
    plotDataPath = os.path.join(os.getcwd(),'Analysis', fileName)
    dateStr = (fileName.split('-', 1)[1]).split('.')[0]
    data = pandas.read_csv(plotDataPath, delimiter=" ")
    plt.plot(data['MAX_LATENCY_SPIKE_DURATION'], data['SUCCESS_RATE'].apply(lambda x : x*100))
    plt.ylabel("BP Activity Success Rate (%)")
    plt.xlabel("Max Latency Spike Duration")
    plt.xscale('linear')
    plt.savefig(os.path.join(os.getcwd(), 'Plots', 'SuccessRate-' + dateStr + '.png'))  
    plt.show()

if __name__ == "__main__":
    main()