from Simulation.BusinessEnvironment.BusinessActivity import *
from Simulation.Events.UserActivityEvent import UserActivityEvent, UserActivitySpikeEvent
from Simulation.Events.LatencyEvent import LatencyEvent, LatencySpikeEvent
from Simulation.Events.BusinessEvents.BusinessProcessActivationEvent import BusinessProcessActivationEvent
from Simulation.Events.BusinessEvents.AreaTransitionEvent import AreaTransitionEvent
from Simulation.Events.BusinessEvents.ActivityChangeEvent import ActivityChangeEvent
from Simulation.Events.BusinessEvents.BusinessEvent import BusinessEvent
from DataOutput.TimeDataRecorder import TimeDataRecorder
from Configuration.globals import GetConfig
from Simulation.NetworkEnvironment.LocalServiceNetwork import LocalServiceNetwork
from Simulation.PhysicalEnvironment.ServiceArea import ServiceArea
from Utilities.PathGenerator import PathGenerator, GetPathGenerator

'''Constructs business process related events'''
class EventFactory(object):
    
    def __init__(self, serviceAreas : list[ServiceArea]) -> None:
        self.history = TimeDataRecorder(0, ["EVENTTYPE", "COMPANY_ID"])
        self.history.createFileOutput(GetConfig().filePaths.simulationPath, "BusinessEventHistory")
        self.nextLatencySpikeTime = {}
        self.nextUserActivitySpikeTime = {}
        self.InitializeSpikeTimes(serviceAreas)
        
    def InitializeSpikeTimes(self, areas: list[ServiceArea]):
        config = GetConfig().eventConfig.latencySpikeDelayRange
        activityConfig = GetConfig().eventConfig.userActivitypikeDelayRange
        for area in areas:
            spikeTime = GetConfig().randoms.latencyDelay.randint(config[0], config[1])
            activitySpikeTime = GetConfig().randoms.userActivitySpikeSimulation.randint(activityConfig[0], activityConfig[1])
            self.nextLatencySpikeTime[area.localServiceNetwork] = spikeTime
            self.nextUserActivitySpikeTime[area] = activitySpikeTime

    
    def UpdateNextLatencySpikeTime(self, network : LocalServiceNetwork):
        config = GetConfig().eventConfig.latencySpikeDelayRange
        self.nextLatencySpikeTime[network] += GetConfig().randoms.latencyDelay.randint(config[0], config[1])
        
    def UpdateNextUserActivitySpikeTime(self, area : ServiceArea):
        config = GetConfig().eventConfig.userActivitypikeDelayRange
        self.nextUserActivitySpikeTime[area] += GetConfig().randoms.activityDelay.randint(config[0], config[1])

    
    def generateActivityChangeEvent(self, event : BusinessEvent, addedTime = 0):
        currentTime = event.t
        businessProcess = event.businessProcess
        company = event.company
        businessActivity = businessProcess.GetCurrentActivity()
        if isinstance(businessActivity, AreaBasedActivity):
            eventTime = currentTime + businessActivity.expectedDuration
            return ActivityChangeEvent(eventTime, company, businessProcess)
        return ActivityChangeEvent(currentTime + addedTime, company, businessProcess)
    
    def generateActivityEvent(self, previousEvent : ActivityChangeEvent):
        currentTime = previousEvent.t
        businessProcess = previousEvent.businessProcess
        currentActivity = businessProcess.GetCurrentActivity()
        if isinstance(currentActivity, AreaBasedActivity):
            return self.generateActivityChangeEvent(previousEvent)
        if isinstance(currentActivity, TrajectoryBasedActivity):
            return self.generateTrajectoryActivityEvent(currentTime, currentActivity, previousEvent)
        if isinstance(currentActivity, PathBasedActivity):
            return self.generatePathBasedActivityEvent(currentTime, currentActivity, previousEvent)
        raise TypeError("Invalid activity type")
    
    def generateFollowUp(self, event):
        if isinstance(event, UserActivityEvent):
            return self.generateUserActivityEvent(event)
        if isinstance(event, LatencyEvent):
            return self.generateLatencyEvent(event)
        if isinstance(event, BusinessProcessActivationEvent):
            self.history.record(event.t, ["BP_ACTIVATION", event.company.id])
            return self.generateActivityChangeEvent(event)
        if isinstance(event, ActivityChangeEvent):
            self.history.record(event.t, ["ACTIVITY_CHANGE", event.company.id])
            return self.generateActivityEvent(event)
        if isinstance(event, AreaTransitionEvent):
            self.history.record(event.t, ["AREA_TRANSITION", event.company.id])
            event : AreaTransitionEvent
            if event.completed:
                duration = GetPathGenerator().CalculateMovementDuration(event.transitionPoint, event.currentActivity.endLocation.cell.site)         
                return self.generateActivityChangeEvent(event, duration)
            return self.generateAreaTransitionEvent(event.t, event.currentActivity, event)
        ValueError("The given event did not match any known type")
        
    def generateUserActivityEvent(self, event : UserActivityEvent):
        delayConfig = GetConfig().eventConfig.activityEventDelayRange
        delay = GetConfig().randoms.activityDelay.randint(delayConfig[0], delayConfig[1])
        eventTime = event.t + delay
        
        if isinstance(event, UserActivitySpikeEvent):
            if event.activityBoostDuration < delay:
                eventTime = event.t + event.activityBoostDuration
                self.UpdateNextUserActivitySpikeTime(event.area)
                return UserActivityEvent.generateFollowUp(event, eventTime)
            return self.generateUserActivitySpikeEvent(event, eventTime)
        
        if eventTime > self.nextUserActivitySpikeTime[event.area]:
            spikeEvent = self.generateUserActivitySpikeEvent(event, eventTime)
            self.nextLatencySpikeTime[event.area] = event.t + spikeEvent.activityBoostDuration
            self.UpdateNextUserActivitySpikeTime(event.area)
            return spikeEvent
        
        return UserActivityEvent.generateFollowUp(event, eventTime)
    
    def generateUserActivitySpikeEvent(self, event : UserActivityEvent, eventTime):
        newEvent = UserActivitySpikeEvent(eventTime, event.area)
        if isinstance(event, UserActivitySpikeEvent):
            if (eventTime < event.t + event.activityBoostDuration):
                duration = event.t + event.activityBoostDuration - eventTime
                newEvent.SetSpike(event.spike, duration)
        return newEvent
        
    def generateLatencyEvent(self, event : LatencyEvent):
        delayConfig = GetConfig().eventConfig.latencyEventDelayRange
        delay = GetConfig().randoms.latencyDelay.randint(delayConfig[0], delayConfig[1])
        eventTime = event.t + delay
        
        if isinstance(event, LatencySpikeEvent):
            if event.spikeDuration < delay:
                eventTime = event.t + event.spikeDuration
                self.nextLatencySpikeTime[event.network] = eventTime
                self.UpdateNextLatencySpikeTime(event.network)
                return LatencyEvent.generateFollowUp(event, eventTime)
        
            return self.generateLatencySpikeEvent(event, eventTime)
        
        if eventTime > self.nextLatencySpikeTime[event.network]:
            spikeEvent = self.generateLatencySpikeEvent(event, eventTime)
            self.nextLatencySpikeTime[event.network] = event.t + spikeEvent.spikeDuration
            self.UpdateNextLatencySpikeTime(event.network)
            return spikeEvent
        return LatencyEvent.generateFollowUp(event, eventTime)
    
    def generateLatencySpikeEvent(self, event : LatencyEvent, eventTime):
        newEvent = LatencySpikeEvent(eventTime, event.network)
        if isinstance(event, LatencySpikeEvent):
            if (eventTime < event.t + event.spikeDuration):
                duration = event.t + event.spikeDuration - eventTime
                newEvent.SetSpike(event.spike, duration)
        return newEvent
        
    def generateBusinessProcessActivationEvent(self, eventTime, company):
        return BusinessProcessActivationEvent(eventTime, company)
      
    def generateTrajectoryActivityEvent(self, currentTime, currentActivity : PathBasedActivity, event : ActivityChangeEvent):
        if currentActivity.currentPosition == len(currentActivity.movementPath) - 1:
            return self.generateActivityChangeEvent(event)
        return self.generateAreaTransitionEvent(currentTime, currentActivity, event)
    
    def generatePathBasedActivityEvent(self, currentTime, currentActivity : PathBasedActivity, event : ActivityChangeEvent):
        if currentActivity.currentPosition == len(currentActivity.movementPath) - 1:
            return self.generateActivityChangeEvent(event)
        return self.generateAreaTransitionEvent(currentTime, currentActivity, event)
    
    def generateAreaTransitionEvent(self, currentTime, currentActivity : PathBasedActivity, event : BusinessEvent):
        path = currentActivity.movementPath
        startingPosition = path[currentActivity.currentPosition]
        endPosition = path[currentActivity.currentPosition + 1]
        p1, p2 = GetPathGenerator().FindCommonBorder(startingPosition, endPosition)
        transitionPoint = (p1[0] + p2[0] / 2.0), (p1[1] + p2[1] / 2.0)
        startingPoint = startingPosition.cell.site[0], startingPosition.cell.site[1]
        if isinstance(event, AreaTransitionEvent):
            event : AreaTransitionEvent
            startingPoint = event.transitionPoint
        travelTime = GetPathGenerator().CalculateMovementDuration(startingPoint, transitionPoint, True)
        eventTime = currentTime + travelTime
        return AreaTransitionEvent(eventTime, event.company, event.businessProcess, currentActivity, transitionPoint)
    
global EVENT_FACTORY
EVENT_FACTORY = None

def SetEventFactory(factory : EventFactory):
    global EVENT_FACTORY
    EVENT_FACTORY = factory
    
def GetEventFactory() -> EventFactory:
    global EVENT_FACTORY
    if EVENT_FACTORY is None:
        raise ValueError("Path generator not initialized")
    return EVENT_FACTORY