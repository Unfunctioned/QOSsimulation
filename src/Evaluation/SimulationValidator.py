from Evaluation.DataStorer import DataStorer, DataType
'''Used to validate the simulation ouput'''
class SimulationValidator(object):
    
    def __init__(self, dataStorage : DataStorer) -> None:
        self.storage = dataStorage
        
    def validate(self):
        activationCount = len(self.storage.GetData(DataType.ACTIVATION).index)
        terminationCount = len(self.storage.GetData(DataType.TERMINATION).index)
        if not activationCount == terminationCount:
            raise ValueError("Not all activities terminated")