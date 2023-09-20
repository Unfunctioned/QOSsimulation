from Configuration.RandomConfig import RandomConfig
class Config(object):
    
    def __init__(self) -> None:
        self.WINDOW_SIZE = (720, 720)
        self.FPS = 60
        self.GRIDSIZE = 7
        self.DENSITY_LEVEL = 500
        self.randoms = RandomConfig()