from Configuration.BaseConfig import BaseConfig
'''Stores configurations for the UI'''
class AppSettings(BaseConfig):
    
    def __init__(self) -> None:
        self.WINDOW_SIZE = (720, 720)
        self.FPS = 60
        self.tracingEnabled = False
        
    def jsonable(self):
        return self.__dict__