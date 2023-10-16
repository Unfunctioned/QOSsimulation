from Configuration.BaseConfig import BaseConfig
'''Stores configurations for the UI'''
class UISettings(BaseConfig):
    
    def __init__(self) -> None:
        self.WINDOW_SIZE = (720, 720)
        self.FPS = 60
        
    def jsonable(self):
        return self.__dict__