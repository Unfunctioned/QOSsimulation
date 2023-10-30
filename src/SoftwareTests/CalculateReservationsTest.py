import unittest
from Configuration.globals import GetConfig, SetConfig
from Configuration.Config import Config
'''Tests if matching resource reservations are generated for given business process'''
class CalculateReservationTest(unittest.TestCase):
    
    def test_calculateReservations(self):
        
