from enum import Enum

'''Stores enums to declare QoS Violation types'''
class ViolationStatusType(Enum):
    CAPACITY = 'CAPACITY',
    PARTIAL_CAPACITY = 'PARTIAL_CAPACITY'
    LATENCY = 'LATENCY',
    RECOVERY = 'RECOVERY'
    