from Configuration.globals import CONFIG
import os
'''Used to record simulation data'''
class DataRecorder(object):
    
    def __init__(self, id, valueName) -> None:
        self.data = []
        self.valueName = valueName
        self.filePath = os.path.join(CONFIG.filePaths.serviceAreaPath, "ServiceArea#" + str(id) + ".txt")
        self.file = open(self.filePath, "a")
        self.file.write("{time} {value}\n".format(time = "TIME", value=valueName))
        
    def record(self, time, value):
        self.data.append((time, value))
        self.file.write("{time} {value}\n".format(time = time, value = value))