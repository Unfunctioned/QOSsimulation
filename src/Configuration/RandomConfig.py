from random import Random
'''Stores the configurations for random variables'''
class RandomConfig(object):
    
    def __init__(self) -> None:
        self.siteGeneration = Random(0)
        self.colorGeneration = Random(0)
        self.pointGeneration = Random(0)