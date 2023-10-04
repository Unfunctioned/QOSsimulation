'''Abstract Recorder class'''
class BaseRecorder(object):
    
    def createFileOutput(self, path, baseFileName):
        pass
    
    def record(self, values):
        pass
    
    def terminate(self):
        pass