from Configuration.globals import CONFIG
import os
'''Used to record simulation data'''
class BasicDataRecorder(object):
    
    def __init__(self, id, size, headers) -> None:
        self.id = id
        self.data = []
        self.size = size
        if(not len(headers) == size):
            raise ValueError("Invalid header count")
        self.headers = headers
        self.filePath = None
        self.file = None
        
    def createFileOutput(self, path, baseFileName):
        self.filePath = os.path.join(path, baseFileName + "#" + str(self.id) + ".txt")
        self.file = open(self.filePath, "a")
        self.file.write("{valueNames}\n".format(valueNames=self._namesToString()))
        
    def record(self, values):
        if(not len(values) == self.size):
            raise ValueError("Invalid value count")
        self.data.append(values)
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