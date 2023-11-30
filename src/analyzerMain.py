from Evaluation.Analyzer import Analyzer

def main():
    analyzer = Analyzer('D:\Repositories\QOSsimulation\Simulations\World#0#0\Run-26-11-2023-20-32-23', 11095)
    analyzer.analyze()
    analyzer.printResults()
    analyzer.writeData()
    
    
if __name__ == "__main__":
    main()