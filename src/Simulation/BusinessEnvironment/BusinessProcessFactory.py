from Simulation.PhysicalEnvironment.ServiceArea import ServiceArea
from Simulation.BusinessEnvironment.ActivityType import ActivityType
from Simulation.BusinessEnvironment.BusinessActivity import *
from Configuration.globals import GetConfig
from Utilities.PathGenerator import GetPathGenerator
from DataOutput.TimeDataRecorder import TimeDataRecorder
'''Factory used to generate business processes based on a business process flow'''
class BuisnessProcessFactory(object):
    
    def __init__(self, pathGenerator : PathGenerator) -> None:
        self.pathGenerator = pathGenerator
        self.serviceAreas : list[ServiceArea]
        self.serviceAreas = pathGenerator.serviceAreas
        self.flows = self.SetBusinessProcessFlows()
        
    def SetBusinessProcessFlows(self):
        flow1 = [ActivityType.AREA, ActivityType.TRAJECTORY, ActivityType.AREA]
        flow2 = [ActivityType.AREA, ActivityType.PATH, ActivityType.AREA]
        return [flow1, flow2]
    
    def SelectBusinessProcessFlow(self):
        return GetConfig().randoms.flowSelector.choice(self.flows)
    
    def CreateBusinessActivities(self, processId, currentTime, companyLocation : ServiceArea,
                                 businessFlow : list[ActivityType],
                                 activityExecutionHistory : TimeDataRecorder) -> list[BusinessActivity]:
        activities = []
        validAreas = self.serviceAreas.copy()
        validAreas.remove(companyLocation)
        customerLocation = GetConfig().randoms.customerLocationSelector.choice(validAreas)
        for i in range(len(businessFlow)):
            item = businessFlow[i]
            activity = None
            match item:
                case ActivityType.AREA:
                    expectedDuration = GetConfig().simConfig.BUSINESS_ACTIVITY_TIME_FACTOR * GetConfig().randoms.workDurationSimulation.randint(1,6)
                    location = companyLocation if i == 0 else customerLocation
                    activity = AreaBasedActivity(processId, currentTime, activityExecutionHistory, expectedDuration, location)
                case ActivityType.TRAJECTORY:
                    activity = TrajectoryBasedActivity(processId, currentTime, activityExecutionHistory, companyLocation, customerLocation)
                case ActivityType.PATH:
                    activity = PathBasedActivity(processId, currentTime, activityExecutionHistory, companyLocation, customerLocation)
                case _:
                    raise ValueError("Invalid type")
            if activity is None:
                raise ValueError("The generated activity is of NoneType")
            activities.append(activity)
        return activities
    
global BUSINESS_PROCESS_FACTORY
BUSINESS_PROCESS_FACTORY = None

def SetBusinessProcessFactory(factory : BuisnessProcessFactory):
    global BUSINESS_PROCESS_FACTORY
    BUSINESS_PROCESS_FACTORY = factory
    
def GetBusinessProcessFactory() -> BuisnessProcessFactory:
    global BUSINESS_PROCESS_FACTORY
    if BUSINESS_PROCESS_FACTORY is None:
        raise ValueError("Business Process Factory not initialized")
    return BUSINESS_PROCESS_FACTORY