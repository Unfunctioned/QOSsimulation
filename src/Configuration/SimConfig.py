from Simulation.PhysicalEnvironment.AreaType import AreaType
from Configuration.BaseConfig import BaseConfig
from Configuration.SimulationMode import SimulationMode
'''Stores configurations for the simulation'''
class SimConfig(BaseConfig):
    
    def __init__(self) -> None:
        self._densityScale = 1
        # Defines a NxN sized grid used to generate the voronoi diagram
        self.GRIDSIZE = 9
        # Amount of weights used to define AreaTypes
        self.WEIGHTS = 500
        # Defines the max. duration of the simulation (soft bound) - used to stop event generation
        self.MAX_TIME = 8000
        #Kilometers spanning the unit range 0.0 to 1.0 (the full map)
        self.SCALE = 100
        #user density rural per sq km
        self.UD_RURAL = 33 / self._densityScale
        #user density urban per sq km
        self.UD_URBAN = 3333 / self._densityScale
        #user density dense urban per sq km
        self.UD_DENSE_URBAN = 8333 / self._densityScale
        #Ratio of areas being of type 'dense urban'
        self.SHARE_DENSE = 0.1
        #Ratio of areas being of type 'rural'
        self.SHARE_RURAL = 0.3
        #Default user activity for 'rural', 'urban' and 'dense urban' areas
        self.DEFAULT_ACTIVITY_RURAL = 0.2
        self.DEFAULT_ACTIVITY_URBAN = 0.2
        self.DEFAULT_ACTIVITY_DENSE_URBAN = 0.1
        #Area traffic capacities by area type ( rural, urban, dense urban) in Mbps/km^2
        self.TRAFFIC_CAPACITY_RURAL = 170 / self._densityScale
        self.TRAFFIC_CAPACITY_URBAN = 17000 / self._densityScale
        self.TRAFFIC_CAPACITY_DENSE_URBAN = 42000 / self._densityScale
        #Network demand posed by non-MBP network users in Mbps
        self.BASIC_DATA_RATE_DEMAND = 25
        #Network activity spike duration range
        self.MAX_NETWORK_ACTIVITY_SPIKE_DURATION = 1200
        #Defines number of active companies in the simulation
        self.COMPANIES = 5000
        #Defines the time factor (in seconds) to determine business activity durations
        self.BUSINESS_ACTIVITY_TIME_FACTOR = 600
        #Reliablity of public slices
        self.PUBLIC_SLICE_RELIABILITY = 0.99
        
        #Default latency for local service networks
        self.DEFAULT_LATENCY = 4
        
        #Set simulation mode
        self.SIMULATION_MODE = SimulationMode.PRIORTY_FIRST
        
    def jsonable(self):
        jsonDict = self.__dict__.copy()
        jsonDict['SIMULATION_MODE'] = SimulationMode.SCHEDULING.name
        return jsonDict
        
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
                raise ValueError("Invalid area type")
                
    def get_default_activity(self, areaType):
        match areaType:
            case AreaType.RURAL:
                return self.DEFAULT_ACTIVITY_RURAL
            case AreaType.URBAN:
                return self.DEFAULT_ACTIVITY_URBAN
            case AreaType.DENSE_URBAN:
                return self.DEFAULT_ACTIVITY_DENSE_URBAN
            case _ :
                raise ValueError("Invalid area type")
                
    def get_traffic_capacity(self, areaType):
        match areaType:
            case AreaType.RURAL:
                return self.TRAFFIC_CAPACITY_RURAL
            case AreaType.URBAN:
                return self.TRAFFIC_CAPACITY_URBAN
            case AreaType.DENSE_URBAN:
                return self.TRAFFIC_CAPACITY_DENSE_URBAN
            case _ :
                raise ValueError("Invalid area type")
    