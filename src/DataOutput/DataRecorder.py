from Configuration.globals import CONFIG
import os
'''Used to record simulation data'''
class DataRecorder(object):
    
    def __init__(self, id, size, headers) -> None:
        self.id = id
        self.data = []
        self.size = size
        if(not len(headers) == size):
            ValueError("Invalid header count")
        self.headers = headers
        self.filePath = None
        self.file = None
        
    def createFileOutput(self, path, baseFileName):
        self.filePath = os.path.join(path, baseFileName + "#" + str(self.id) + ".txt")
        self.file = open(self.filePath, "a")
        self.file.write("{time} {valueNames}\n".format(time = "TIME", valueNames=self._namesToString()))
        
    def record(self, time, values):
        if(len(values) == self.size):
            ValueError("Invalid value count")
        self.data.append((time, values))
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