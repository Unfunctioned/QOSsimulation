from Configuration.BaseConfig import BaseConfig
'''Stores configurations for the UI'''
class AppSettings(BaseConfig):
    
    def __init__(self) -> None:
        self.WINDOW_SIZE = (720, 720)
        self.FPS = 60
        self.tracingEnabled = False
        #Maximum number of line stored before writing to file
        self.writingBufferSize = 100
        
    def jsonable(self):
        return self.__dict__