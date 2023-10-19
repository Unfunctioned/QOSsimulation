from enum import Enum
from pandas import DataFrame
'''Enum to specify types of data'''
class DataType(Enum):
    ALL = 0,
    ACTIVATION = 1,
    TERMINATION = 2,
    SUCCESS = 3,
    FAILURE = 4
    
'''Used to store simulation data for evaluation'''
class DataStorer(object):
    
    def __init__(self, allData : DataFrame) -> None:
        self._dataStorage : dict[DataType, DataFrame]
        self._dataStorage = dict()
        self._dataStorage[DataType.ALL] = allData
        
    def AddData(self, key : DataType, data : DataFrame):
        self._dataStorage[key] = data
        
    def GetData(self, key : DataType) -> DataFrame:
        if key in self._dataStorage:
            return self._dataStorage[key]
        raise KeyError("Key not found")