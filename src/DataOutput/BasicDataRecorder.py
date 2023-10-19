from DataOutput.BaseRecorder import BaseRecorder
from pathlib import Path
'''Used to record simulation data'''
class BasicDataRecorder(BaseRecorder):
    
    def __init__(self, id, headers) -> None:
        self.id = id
        #self.data = []
        self.size = len(headers)
        self.headers = headers
        self.filePath = None
        self.file = None
        
    def createFileOutput(self, path : Path, baseFileName, withOverride = False):
        self.filePath = path.joinpath(baseFileName + '#' + str(self.id) + '.txt')
        writeOption = 'a'
        if withOverride:
            writeOption = 'w'
        self.file = self.filePath.open(writeOption)
        self.file.write("{valueNames}\n".format(valueNames=self._namesToString()))
        
    def record(self, values):
        if(not len(values) == self.size):
            raise ValueError("Invalid value count")
        #self.data.append(values)
        self.file.write("{value}\n".format(value = self._valuesToString(values)))
        
    def _namesToString(self):
        text = ""
        for header in self.headers:
            text += header + " "
        return text
    
    def _valuesToString(self, values):
        text = ""
        for value in values:
            text += str(value) + " "
        return text
    
    def terminate(self):
        self.file.close()