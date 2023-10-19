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
    history = TimeDataRecorder(0, ["EVENTTYPE", "COMPANY_ID"])
    nextLatencySpikeTime = {}
    nextUserActivitySpikeTime = {}
        
    @staticmethod
    def InitializeOutput():
        EventFactory.history.createFileOutput(GetConfig().filePaths.simulationPath, "BusinessEventHistory")
        
    @staticmethod
    def InitializeSpikeTimes(areas: list[ServiceArea]):
        config = GetConfig().eventConfig.latencySpikeDelayRange
        activityConfig = GetConfig().eventConfig.userActivitypikeDelayRange
        for area in areas:
            spikeTime = GetConfig().randoms.latencyDelay.randint(config[0], config[1])
            activitySpikeTime = GetConfig().randoms.userActivitySpikeSimulation.randint(activityConfig[0], activityConfig[1])
            EventFactory.nextLatencySpikeTime[area.localServiceNetwork] = spikeTime
            EventFactory.nextUserActivitySpikeTime[area] = activitySpikeTime

    
    @staticmethod
    def UpdateNextLatencySpikeTime(network : LocalServiceNetwork):
        config = GetConfig().eventConfig.latencySpikeDelayRange
        EventFactory.nextLatencySpikeTime[network] += GetConfig().randoms.latencyDelay.randint(config[0], config[1])
        
    @staticmethod
    def UpdateNextUserActivitySpikeTime(area : ServiceArea):
        config = GetConfig().eventConfig.userActivitypikeDelayRange
        EventFactory.nextUserActivitySpikeTime[area] += GetConfig().randoms.activityDelay.randint(config[0], config[1])

    @staticmethod
    def generateActivityChangeEvent(event : BusinessEvent, addedTime = 0):
        currentTime = event.t
        businessProcess = event.businessProcess
        company = event.company
        businessActivity = businessProcess.GetCurrentActivity()
        if isinstance(businessActivity, AreaBasedActivity):
            eventTime = currentTime + businessActivity.expectedDuration
            return ActivityChangeEvent(eventTime, company, businessProcess)
        return ActivityChangeEvent(currentTime + addedTime, company, businessProcess)
    
    @staticmethod
    def generateActivityEvent(previousEvent : ActivityChangeEvent):
        currentTime = previousEvent.t
        businessProcess = previousEvent.businessProcess
        currentActivity = businessProcess.GetCurrentActivity()
        if isinstance(currentActivity, AreaBasedActivity):
            return EventFactory.generateActivityChangeEvent(previousEvent)
        if isinstance(currentActivity, TrajectoryBasedActivity):
            return EventFactory.generateTrajectoryActivityEvent(currentTime, currentActivity, previousEvent)
        if isinstance(currentActivity, PathBasedActivity):
            return EventFactory.generatePathBasedActivityEvent(currentTime, currentActivity, previousEvent)
        raise TypeError("Invalid activity type")
    
    @staticmethod
    def generateFollowUp(event):
        if isinstance(event, UserActivityEvent):
            return EventFactory.generateUserActivityEvent(event)
        if isinstance(event, LatencyEvent):
            return EventFactory.generateLatencyEvent(event)
        if isinstance(event, BusinessProcessActivationEvent):
            EventFactory.history.record(event.t, ["BP_ACTIVATION", event.company.id])
            return EventFactory.generateActivityChangeEvent(event)
        if isinstance(event, ActivityChangeEvent):
            EventFactory.history.record(event.t, ["ACTIVITY_CHANGE", event.company.id])
            return EventFactory.generateActivityEvent(event)
        if isinstance(event, AreaTransitionEvent):
            EventFactory.history.record(event.t, ["AREA_TRANSITION", event.company.id])
            event : AreaTransitionEvent
            if event.completed:
                duration = GetPathGenerator().CalculateMovementDuration(event.transitionPoint, event.currentActivity.endLocation.cell.site)         
                return EventFactory.generateActivityChangeEvent(event, duration)
            return EventFactory.generateAreaTransitionEvent(event.t, event.currentActivity, event)
        ValueError("The given event did not match any known type")
        
    @staticmethod
    def generateUserActivityEvent(event : UserActivityEvent):
        delayConfig = GetConfig().eventConfig.activityEventDelayRange
        delay = GetConfig().randoms.activityDelay.randint(delayConfig[0], delayConfig[1])
        eventTime = event.t + delay
        
        if isinstance(event, UserActivitySpikeEvent):
            if event.activityBoostDuration < delay:
                eventTime = event.t + event.activityBoostDuration
                EventFactory.UpdateNextUserActivitySpikeTime(event.area)
                return UserActivityEvent.generateFollowUp(event, eventTime)
            return EventFactory.generateUserActivitySpikeEvent(event, eventTime)
        
        if eventTime > EventFactory.nextUserActivitySpikeTime[event.area]:
            spikeEvent = EventFactory.generateUserActivitySpikeEvent(event, eventTime)
            EventFactory.nextLatencySpikeTime[event.area] = event.t + spikeEvent.activityBoostDuration
            EventFactory.UpdateNextUserActivitySpikeTime(event.area)
            return spikeEvent
        
        return UserActivityEvent.generateFollowUp(event, eventTime)
    
    @staticmethod
    def generateUserActivitySpikeEvent(event : UserActivityEvent, eventTime):
        newEvent = UserActivitySpikeEvent(eventTime, event.area)
        if isinstance(event, UserActivitySpikeEvent):
            if (eventTime < event.t + event.activityBoostDuration):
                duration = event.t + event.activityBoostDuration - eventTime
                newEvent.SetSpike(event.spike, duration)
        return newEvent
        
    @staticmethod
    def generateLatencyEvent(event : LatencyEvent):
        delayConfig = GetConfig().eventConfig.latencyEventDelayRange
        delay = GetConfig().randoms.latencyDelay.randint(delayConfig[0], delayConfig[1])
        eventTime = event.t + delay
        
        if isinstance(event, LatencySpikeEvent):
            if event.spikeDuration < delay:
                eventTime = event.t + event.spikeDuration
                EventFactory.nextLatencySpikeTime[event.network] = eventTime
                EventFactory.UpdateNextLatencySpikeTime(event.network)
                return LatencyEvent.generateFollowUp(event, eventTime)
        
            return EventFactory.generateLatencySpikeEvent(event, eventTime)
        
        if eventTime > EventFactory.nextLatencySpikeTime[event.network]:
            spikeEvent = EventFactory.generateLatencySpikeEvent(event, eventTime)
            EventFactory.nextLatencySpikeTime[event.network] = event.t + spikeEvent.spikeDuration
            EventFactory.UpdateNextLatencySpikeTime(event.network)
            return spikeEvent
        return LatencyEvent.generateFollowUp(event, eventTime)
    
    @staticmethod
    def generateLatencySpikeEvent(event : LatencyEvent, eventTime):
        newEvent = LatencySpikeEvent(eventTime, event.network)
        if isinstance(event, LatencySpikeEvent):
            if (eventTime < event.t + event.spikeDuration):
                duration = event.t + event.spikeDuration - eventTime
                newEvent.SetSpike(event.spike, duration)
        return newEvent
        
    @staticmethod
    def generateBusinessProcessActivationEvent(eventTime, company):
        return BusinessProcessActivationEvent(eventTime, company)
      
    @staticmethod
    def generateTrajectoryActivityEvent(currentTime, currentActivity : PathBasedActivity, event : ActivityChangeEvent):
        if currentActivity.currentPosition == len(currentActivity.movementPath) - 1:
            return EventFactory.generateActivityChangeEvent(event)
        return EventFactory.generateAreaTransitionEvent(currentTime, currentActivity, event)
    
    @staticmethod
    def generatePathBasedActivityEvent(currentTime, currentActivity : PathBasedActivity, event : ActivityChangeEvent):
        if currentActivity.currentPosition == len(currentActivity.movementPath) - 1:
            return EventFactory.generateActivityChangeEvent(event)
        return EventFactory.generateAreaTransitionEvent(currentTime, currentActivity, event)
    
    @staticmethod
    def generateAreaTransitionEvent(currentTime, currentActivity : PathBasedActivity, event : BusinessEvent):
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
        