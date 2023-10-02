from enum import Enum

'''Stores enums to declare QoS Violation types'''
class ViolationType(Enum):
    CAPACITY = 'CAPACITY',
    LATENCY = 'LATENCY'
    