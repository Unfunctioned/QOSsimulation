from DataOutput.TimeDataRecorder import TimeDataRecorder
'''Mock class of the timeData recorder for testing purposes'''
class MockTimeDataRecorder(TimeDataRecorder):
    
    def __init__(self) -> None:
        return
    
    def createFileOutput(self, path, baseFileName):
        return
    
    def record(self, time, values):
        return
    
    def terminate(self):
        return
