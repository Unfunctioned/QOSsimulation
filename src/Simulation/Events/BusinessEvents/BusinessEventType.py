from enum import Enum
'''Enum to express eventTypes'''
class BusinessEventType(Enum):
    PROCESS_ACTIVATION = 'PROCESS_ACTIVATION',
    ACTIVITY_CHANGE = 'ACtIVITY_CHANGE',
    AREA_TRANSITION = 'AREA_TRANSITION'