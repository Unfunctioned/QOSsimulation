from Simulation.BusinessEnvironment.BusinessActivity import AreaBasedActivity, PathBasedActivity, TrajectoryBasedActivity, BusinessActivity
from DataOutput.BasicDataRecorder import BasicDataRecorder
from Simulation.BusinessEnvironment.ActivityType import ActivityType
from Simulation.NetworkEnvironment.NetworkSlice import NetworkSlice
from DataOutput.TimeDataRecorder import TimeDataRecorder
from Simulation.BusinessEnvironment.BusinessActivity import BusinessActivity
from Configuration.globals import GetConfig
'''Models the business process of a company'''
class BusinessProcess(object):
    
    @staticmethod
    def generateNewProcess():
        pass
    
    def __init__(self, id, activities : list[BusinessActivity], folderPath, 
                 activityHistory : TimeDataRecorder) -> None:
        self.id = id
        self.activities = activities
        self.activeActivityIndex = None
        self.activityHistory = activityHistory
        self.storeInfo(folderPath)
        
    def storeInfo(self, folderPath):
        if GetConfig().appSettings.tracingEnabled:
            businessRecorder = BasicDataRecorder(self.id, ["INDEX", "TYPE", "DURATION", "REQ.CAPACITY", "REQ.LATENCY"])
            businessRecorder.createFileOutput(folderPath, "ProcessDefinition")
            self._recordProcessDefinition(businessRecorder)
            businessRecorder.terminate()
    
    def Execute(self, currentTime, networkSlice : NetworkSlice):
        self.activeActivityIndex = 0
        activity : BusinessActivity
        activity = self.activities[0]
        activity.activate(currentTime, networkSlice)
        
    def ExecuteNext(self, currentTime, networkSlice : NetworkSlice):
        activity : BusinessActivity
        activity = self.activities[self.activeActivityIndex]
        nextActivity : BusinessActivity
        nextActivity = None
        if self.activeActivityIndex < len(self.activities) - 1:
            self.activeActivityIndex += 1
            nextActivity = self.activities[self.activeActivityIndex]
            nextActivity.activate(currentTime, networkSlice)
        activity.deactivate(currentTime, networkSlice)
        return nextActivity
    
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
        
    def GetCurrentActivity(self) -> BusinessActivity:
        if self.activeActivityIndex is None:
            return None
        return self.activities[self.activeActivityIndex]