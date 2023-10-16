from Configuration.Config import Config

global CONFIG 
CONFIG = Config()

def GetConfig():
    global CONFIG
    return CONFIG


def UpdateConfig(config : Config):
    global CONFIG 
    CONFIG = config