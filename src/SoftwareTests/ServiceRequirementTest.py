import unittest
from Utilities.VoronoiDiagram.Cell import Cell
from Simulation.PhysicalEnvironment.AreaType import AreaType
from Simulation.PhysicalEnvironment.ServiceArea import ServiceArea
from Configuration.globals import GetConfig
from Simulation.NetworkEnvironment.ServiceRequirements.ServiceRequirement import ServiceRequirement
from Simulation.NetworkEnvironment.ViolationStatusType import ViolationStatusType
'''Specifies tests that service requirments behave as intended'''
class ServiceRequirementTest(unittest.TestCase):
    
    def setupServiceArea(self) -> ServiceArea:
        unitsize = 1.0 / GetConfig().simConfig.SCALE
        cell = Cell([unitsize / 2, unitsize / 2], [[0.0,0.0],[unitsize,0.0],[unitsize,unitsize],[0.0,unitsize]])
        serviceArea = ServiceArea(2, cell, AreaType.RURAL)
        serviceArea.InitializeNetwork(0)
        self.assertEqual(serviceArea.areaSize, 1.0)
        return serviceArea
    
    def test_updateQoSStatus(self):
        serviceArea = self.setupServiceArea()
        serviceRequirement = ServiceRequirement(10, 10, 0.95, 0)
        serviceRequirement.UpdateQoSStatus(100, serviceArea.id, ViolationStatusType.CAPACITY)
        print(serviceRequirement.totalViolationTime)
        self.assertEqual(serviceRequirement.totalViolationTime, 0)
        serviceRequirement.UpdateQoSStatus(200, serviceArea.id, ViolationStatusType.LATENCY)
        print(serviceRequirement.totalViolationTime)
        self.assertEqual(serviceRequirement.totalViolationTime, 100)
        self.assertEqual(serviceRequirement.capacityViolationTime, 100)
        serviceRequirement.UpdateQoSStatus(350, serviceArea.id, ViolationStatusType.RECOVERY)
        print(serviceRequirement.totalViolationTime)
        self.assertEqual(serviceRequirement.totalViolationTime, 250)
        self.assertEqual(serviceRequirement.latencyViolationTime, 150)
        
        serviceArea.Terminate()
