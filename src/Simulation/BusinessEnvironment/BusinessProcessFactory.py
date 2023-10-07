from Simulation.PhysicalEnvironment.ServiceArea import ServiceArea
from Simulation.BusinessEnvironment.ActivityType import ActivityType
from Simulation.BusinessEnvironment.BusinessActivity import *
from Configuration.globals import CONFIG
from Utilities.PathGenerator import PathGenerator
'''Factory used to generate business processes based on a business process flow'''
class BuisnessProcessFactory(object):
    serviceAreas = None
    flows = None
    pathGenerator = PathGenerator()
    
    def SetServiceAreas(serviceAreas : list[ServiceArea]):
        BuisnessProcessFactory.serviceAreas = serviceAreas
        BuisnessProcessFactory.pathGenerator.Initialize(serviceAreas)
        
    def SetBusinessProcessFlows():
        flow1 = [ActivityType.AREA, ActivityType.TRAJECTORY, ActivityType.AREA]
        #flow2 = [ActivityType.AREA, ActivityType.PATH, ActivityType.AREA]
        BuisnessProcessFactory.flows = [flow1]
    
    def SelectBusinessProcessFlow():
        if BuisnessProcessFactory.flows is None:
            raise ValueError("Business Process Flows not initialized")
        return CONFIG.randoms.flowSelector.choice(BuisnessProcessFactory.flows)
    
    def CreateBusinessActivities(companyLocation : ServiceArea, businessFlow : list[ActivityType]):
        activities = []
        for i in range(len(businessFlow)):
            item = businessFlow[i]
            activity = None
            match item:
                case ActivityType.AREA:
                    expectedDuration = CONFIG.simConfig.BUSINESS_ACTIVITY_TIME_FACTOR * CONFIG.randoms.workDurationSimulation.randint(1,6)
                    customerLocation = CONFIG.randoms.customerLocationSelector.choice(BuisnessProcessFactory.serviceAreas)
                    location = companyLocation if i == 0 else customerLocation
                    activity = AreaBasedActivity(expectedDuration, location)
                case ActivityType.PATH:
                    raise NotImplementedError()
                case ActivityType.TRAJECTORY:
                    customerLocation = CONFIG.randoms.customerLocationSelector.choice(BuisnessProcessFactory.serviceAreas)
                    activity = TrajectoryBasedActivity(companyLocation, customerLocation)
                case _:
                    raise ValueError("Invalid type")
            if activity is None:
                raise ValueError("The generated activity is of NoneType")
            activities.append(activity)
        return activities