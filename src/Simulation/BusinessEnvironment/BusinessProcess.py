from Configuration.globals import CONFIG
from Simulation.BusinessEnvironment.BusinessActivity import AreaBasedActivity, PathBasedActivity, TrajectoryBasedActivity
from DataOutput.BasicDataRecorder import BasicDataRecorder
from Simulation.BusinessEnvironment.ActivityType import ActivityType
from Simulation.NetworkEnvironment.NetworkSlice import NetworkSlice
'''Models the business process of a company'''
class BusinessProcess(object):
    
    def __init__(self, id, location, folderPath) -> None:
        self.activities = self.generateProcess(location)
        businessRecorder = BasicDataRecorder(id, 5, ["INDEX", "TYPE", "DURATION", "REQ.CAPACITY", "REQ.LATENCY"])
        businessRecorder.createFileOutput(folderPath, "ProcessDefinition")
        self._recordProcessDefinition(businessRecorder)       
        
    def generateProcess(self, companyLocation):
        activities = []
        expectedDuration = CONFIG.simConfig.BUSINESS_ACTIVITY_TIME_FACTOR * CONFIG.randoms.workDurationSimulation.randint(1,6)
        activities.append(AreaBasedActivity(expectedDuration, companyLocation))
        return activities
    
    def Execute(self, currentTime, networkSlice : NetworkSlice):
        activity = self.activities[0]
        activity.activate(currentTime, networkSlice)
    
    def _recordProcessDefinition(self, businessRecorder : BasicDataRecorder):
        for i in range(len(self.activities)):
            activity = self.activities[i]
            requirements = activity.serviceRequirement
            activityType = self._extractActivityType(activity)
            businessRecorder.record((i, activityType.value[0], activity.expectedDuration, requirements.defaultCapacityDemand, requirements.latency))
            
    def _extractActivityType(self, activity):
        if(isinstance(activity, AreaBasedActivity)):
            return ActivityType.AREA
        elif(isinstance(activity, TrajectoryBasedActivity)):
            return ActivityType.TRAJECTORY
        elif(isinstance(activity, PathBasedActivity)):
            return ActivityType.PATH
        else:
            raise ValueError("Unknown activity type")