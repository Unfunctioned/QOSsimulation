from Evaluation.Analyzer import Analyzer

def main():
    analyzer = Analyzer('D:\Repositories\QOSsimulation\Simulations\Run-16-10-2023-10-26-38', 10858)
    analyzer.analyze()
    analyzer.printResults()
    analyzer.writeData()
    
    
if __name__ == "__main__":
    main()