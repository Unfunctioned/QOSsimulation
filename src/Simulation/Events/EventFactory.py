from Simulation.BusinessEnvironment.BusinessActivity import *
from Simulation.Events.UserActivityEvent import UserActivityEvent
from Simulation.Events.LatencyEvent import LatencyEvent
from Simulation.Events.BusinessEvents.BusinessProcessActivationEvent import BusinessProcessActivationEvent
from Simulation.BusinessEnvironment.Company import Company
from Simulation.BusinessEnvironment.BusinessProcess import BusinessProcess
from Simulation.Events.BusinessEvents.AreaTransitionEvent import AreaTransitionEvent
from Simulation.Events.BusinessEvents.ActivityChangeEvent import ActivityChangeEvent

'''Constructs business process related events'''
class EventFactory(object):
    
    @staticmethod
    def generateActivityTerminationEvent(event):
        currentTime = event.t
        businessProcess = event.businessProcess
        company = event.company
        businessActivity = businessProcess.GetCurrentActivity()
        if isinstance(businessActivity, AreaBasedActivity):
            eventTime = currentTime + businessActivity.expectedDuration
            return ActivityChangeEvent(eventTime, company, businessProcess)
        raise ValueError("Invalid Activity type")
    
    @staticmethod
    def generateActivityEvent(previousEvent : ActivityChangeEvent):
        company = previousEvent.company
        currentTime = previousEvent.t
        businessProcess = previousEvent.businessProcess
        currentActivity = businessProcess.GetCurrentActivity()
        if isinstance(currentActivity, AreaBasedActivity):
            return EventFactory.generateActivityTerminationEvent(currentTime + currentActivity.expectedDuration, company, currentActivity)
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
            return LatencyEvent.generateFollowUp(event)
        if isinstance(event, BusinessProcessActivationEvent):
            return EventFactory.generateActivityTerminationEvent(event)
        if isinstance(event, ActivityChangeEvent):
            return EventFactory.generateActivityEvent(event)
        if isinstance(event, AreaTransitionEvent):
            event : AreaTransitionEvent
            if event.completed:
                return EventFactory.generateActivityTerminationEvent(event)
        ValueError("The given event did not match any known type")
        
    @staticmethod
    def generateBusinessProcessActivationEvent(eventTime, company):
        return BusinessProcessActivationEvent(eventTime, company)
      
    @staticmethod
    def generateTrajectoryActivityEvent(currentTime, currentActivity : PathBasedActivity, event : ActivityChangeEvent):
        if currentActivity.currentPosition == 0:
            return EventFactory.generateActivityChangeEvent(currentTime, event.company, event.businessProcess)
        return EventFactory.generateAreaTransitionEvent(currentTime, currentActivity, event)   
    
    @staticmethod
    def generateActivityChangeEvent(currentTime, company : Company, businessProcess : BusinessProcess):
        return ActivityChangeEvent(currentTime, company, businessProcess)
    
    @staticmethod
    def generateAreaTransitionEvent(currentTime, currentActivity : PathBasedActivity, event : ActivityChangeEvent):
        path = currentActivity.movementPath
        startingPosition = path[currentActivity.currentPosition]
        endPosition = path[currentActivity.currentPosition + 1]
        p1, p2 = PathGenerator.FindCommonBorder(startingPosition, endPosition)
        transitionPoint = (p1[0] + p2[0] / 2.0), (p1[1] + p2[1] / 2.0)
        travelTime = PathGenerator.CalculateMovementDuration(startingPosition.cell.site, transitionPoint, True)
        eventTime = currentTime + travelTime
        return AreaTransitionEvent(eventTime, event.company, event.businessProcess, currentActivity, transitionPoint) 