from Simulation.PhysicalEnvironment.ServiceArea import ServiceArea
from Simulation.BusinessEnvironment.ActivityType import ActivityType
from Simulation.BusinessEnvironment.BusinessActivity import *
from Configuration.globals import GetConfig
from Utilities.PathGenerator import PathGenerator
from DataOutput.TimeDataRecorder import TimeDataRecorder
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
        flow2 = [ActivityType.AREA, ActivityType.PATH, ActivityType.AREA]
        BuisnessProcessFactory.flows = [flow1, flow2]
    
    def SelectBusinessProcessFlow():
        if BuisnessProcessFactory.flows is None:
            raise ValueError("Business Process Flows not initialized")
        return GetConfig().randoms.flowSelector.choice(BuisnessProcessFactory.flows)
    
    def CreateBusinessActivities(processId, currentTime, companyLocation : ServiceArea, businessFlow : list[ActivityType],
                                 activityExecutionHistory : TimeDataRecorder):
        activities = []
        validAreas = BuisnessProcessFactory.serviceAreas.copy()
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