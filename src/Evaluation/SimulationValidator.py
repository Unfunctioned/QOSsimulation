from Evaluation.DataStorer import DataStorer, DataType
'''Used to validate the simulation ouput'''
class SimulationValidator(object):
    
    def __init__(self, dataStorage : DataStorer) -> None:
        self.activations = len(dataStorage.GetData(DataType.ACTIVATION).index)
        self.terminations = len(dataStorage.GetData(DataType.TERMINATION).index)
        
    def validate(self):
        if not self.activations == self.terminations:
            raise ValueError("Not all activities terminated")