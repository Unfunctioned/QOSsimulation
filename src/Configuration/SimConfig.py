from Simulation.PhysicalEnvironment.AreaType import AreaType
'''Stores configurations for the simulation'''
class SimConfig(object):
    
    def __init__(self) -> None:
        self.GRIDSIZE = 9
        self.DENSITY_LEVEL = 500
        #Kilometers spanning the unit range 0.0 to 1.0 (the full map)
        self.SCALE = 100
        #user density rural per sq km
        self.UD_RURAL = 100
        #user density urban per sq km
        self.UD_URBAN = 10000
        #user density dense urban per sq km
        self.UD_DENSE_URBAN = 25000
        #Ratio of areas being of type 'dense urban'
        self.SHARE_DENSE = 0.1
        #Ratio of areas being of type 'rural'
        self.SHARE_RURAL = 0.3
        
    def scale(self, value):
        return value * (self.SCALE ** 2)
    
    def get_user_density(self, areaType):
        match areaType:
            case AreaType.RURAL:
                return self.UD_RURAL
            case AreaType.URBAN:
                return self.UD_URBAN
            case AreaType.DENSE_URBAN:
                return self.UD_DENSE_URBAN
            case _ :
                ValueError("Invalid area type")
    
    