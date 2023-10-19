from pathlib import Path
from DataOutput.BaseRecorder import BaseRecorder
'''Used to record simulation data'''
class TimeDataRecorder(BaseRecorder):
    
    def __init__(self, id, headers) -> None:
        self.id = id
        #self.data = []
        self.size = len(headers)
        self.headers = headers
        self.filePath = None
        self.file = None
        
    def createFileOutput(self, path, baseFileName):
        self.filePath = Path.joinpath(path, baseFileName + "#" + str(self.id) + ".txt")
        self.file = self.filePath.open("a")
        self.file.write("{time} {valueNames}\n".format(time = "TIME", valueNames=self._namesToString()))
        
    def record(self, time, values):
        if(not len(values) == self.size):
            raise ValueError("Invalid value count")
        #self.data.append((time, values))
        self.file.write("{time} {value}\n".format(time = time, value = self._valuesToString(values)))
        
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