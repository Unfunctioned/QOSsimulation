from Simulation.BusinessEnvironment.BusinessActivity import *
from Simulation.Events.UserActivityEvent import UserActivityEvent
from Simulation.Events.LatencyEvent import LatencyEvent, LatencySpikeEvent
from Simulation.Events.BusinessEvents.BusinessProcessActivationEvent import BusinessProcessActivationEvent
from Simulation.Events.BusinessEvents.AreaTransitionEvent import AreaTransitionEvent
from Simulation.Events.BusinessEvents.ActivityChangeEvent import ActivityChangeEvent
from Simulation.Events.BusinessEvents.BusinessEvent import BusinessEvent
from DataOutput.TimeDataRecorder import TimeDataRecorder
from Configuration.globals import CONFIG
from Simulation.NetworkEnvironment.LocalServiceNetwork import LocalServiceNetwork
from Simulation.PhysicalEnvironment.ServiceArea import ServiceArea

'''Constructs business process related events'''
class EventFactory(object):
    history = TimeDataRecorder(0, 2, ["EVENTTYPE", "COMPANY_ID"])
    nextSpikeTime = {}
        
    @staticmethod
    def InitializeOutput():
        EventFactory.history.createFileOutput(CONFIG.filePaths.simulationPath, "BusinessEventHistory")
        
    @staticmethod
    def InitializeLatencySpikeTimes(areas: list[ServiceArea]):
        config = CONFIG.eventConfig.latencySpikeDelayRange
        for area in areas:
            spikeTime = CONFIG.randoms.latencyDelay.randint(config[0], config[1])
            EventFactory.nextSpikeTime[area.localServiceNetwork] = spikeTime

    
    @staticmethod
    def UpdateNextLatencySpikeTime(network : LocalServiceNetwork):
        config = CONFIG.eventConfig.latencySpikeDelayRange
        EventFactory.nextSpikeTime[network] += CONFIG.randoms.latencyDelay.randint(config[0], config[1])
        
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
            pass
        raise TypeError("Invalid activity type")
    
    @staticmethod
    def generateFollowUp(event):
        if isinstance(event, UserActivityEvent):
            return UserActivityEvent.generateFollowUp(event)
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
                duration = PathGenerator.CalculateMovementDuration(event.transitionPoint, event.currentActivity.endLocation.cell.site)         
                return EventFactory.generateActivityChangeEvent(event, duration)
            return EventFactory.generateAreaTransitionEvent(event.t, event.currentActivity, event)
        ValueError("The given event did not match any known type")
        
    @staticmethod
    def generateLatencyEvent(event : LatencyEvent):
        delayConfig = CONFIG.eventConfig.latencyEventDelayRange
        delay = CONFIG.randoms.latencyDelay.randint(delayConfig[0], delayConfig[1])
        eventTime = event.t + delay
        
        if isinstance(event, LatencySpikeEvent):
            if event.spikeDuration < delay:
                eventTime = event.t + event.spikeDuration
                EventFactory.nextSpikeTime[event.network] = eventTime
                EventFactory.UpdateNextLatencySpikeTime(event.network)
                return LatencyEvent.generateFollowUp(event, eventTime)
        
            return EventFactory.generateLatencySpikeEvent(event, eventTime)
        
        if eventTime > EventFactory.nextSpikeTime[event.network]:
            spikeEvent = EventFactory.generateLatencySpikeEvent(event, eventTime)
            EventFactory.nextSpikeTime[event.network] = event.t + spikeEvent.spikeDuration
            EventFactory.UpdateNextLatencySpikeTime(event.network)
            return spikeEvent
        return LatencyEvent.generateFollowUp(event, eventTime)
    
    @staticmethod
    def generateLatencySpikeEvent(event : LatencyEvent, eventTime):
        newEvent = LatencySpikeEvent(eventTime, event.network)
        if isinstance(event, LatencySpikeEvent):
            if (eventTime < event.t + event.spikeDuration):
                duration = event.t + event.spikeDuration - eventTime
                newEvent.SetSpikeDuration(duration)
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
    def generateAreaTransitionEvent(currentTime, currentActivity : PathBasedActivity, event : BusinessEvent):
        path = currentActivity.movementPath
        startingPosition = path[currentActivity.currentPosition]
        endPosition = path[currentActivity.currentPosition + 1]
        p1, p2 = PathGenerator.FindCommonBorder(startingPosition, endPosition)
        transitionPoint = (p1[0] + p2[0] / 2.0), (p1[1] + p2[1] / 2.0)
        startingPoint = startingPosition.cell.site[0], startingPosition.cell.site[1]
        if isinstance(event, AreaTransitionEvent):
            event : AreaTransitionEvent
            startingPoint = event.transitionPoint
        travelTime = PathGenerator.CalculateMovementDuration(startingPoint, transitionPoint, True)
        eventTime = currentTime + travelTime
        return AreaTransitionEvent(eventTime, event.company, event.businessProcess, currentActivity, transitionPoint)
        