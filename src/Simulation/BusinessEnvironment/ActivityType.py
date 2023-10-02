from enum import Enum

'''Defines labels for the different activity types used for recording business processes'''
class ActivityType(Enum):
    TRAJECTORY = 'TRAJECTORY',
    PATH = 'PATH',
    AREA = 'AREA',