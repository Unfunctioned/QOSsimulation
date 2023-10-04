from enum import Enum

'''Stores enums to declare QoS Violation types'''
class ViolationStatusType(Enum):
    CAPACITY = 'CAPACITY',
    LATENCY = 'LATENCY',
    RECOVERY = 'RECOVERY'
    