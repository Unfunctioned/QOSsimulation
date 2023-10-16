from Evaluation.Analyzer import Analyzer

def main():
    analyzer = Analyzer('D:\Repositories\QOSsimulation\Simulations\Run-16-10-2023-15-45-50', 10829)
    analyzer.analyze()
    analyzer.printResults()
    analyzer.writeData()
    
    
if __name__ == "__main__":
    main()