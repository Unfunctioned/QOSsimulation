from Evaluation.Analyzer import Analyzer

def main():
    analyzer = Analyzer('D:\Repositories\QOSsimulation\Simulations\World#0#3\Run-19-10-2023-00-01-16')
    analyzer.analyze()
    analyzer.printResults()
    analyzer.writeData()
    
    
if __name__ == "__main__":
    main()