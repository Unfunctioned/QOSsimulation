import unittest
from Utilities.VoronoiDiagram.Cell import Cell
from Simulation.PhysicalEnvironment.AreaType import AreaType
from Simulation.PhysicalEnvironment.ServiceArea import ServiceArea
from Configuration.globals import CONFIG
from Simulation.BusinessEnvironment.Company import Company
from Simulation.World import World
from Simulation.Events.EventHandler import EventHandler

class QoSViolationTest(unittest.TestCase):
    
    def setupServiceArea(self):
        unitsize = 1.0 / CONFIG.simConfig.SCALE
        cell = Cell([unitsize / 2, unitsize / 2], [[0.0,0.0],[unitsize,0.0],[unitsize,unitsize],[0.0,unitsize]])
        serviceArea = ServiceArea(0, cell, AreaType.RURAL)
        serviceArea.InitializeNetwork()
        self.assertEqual(serviceArea.areaSize, 1.0)
        return serviceArea
    
    def setupCompanies(self, serviceArea, companyCount) -> list[Company]:
        companies = []
        for i in range(companyCount):
            companies.append(Company(i, serviceArea))
        return companies
            
    def test_registerQoSTotalCapacityViolation(self):
        serviceArea = self.setupServiceArea()
        network = serviceArea.localServiceNetwork
        self.assertEqual(network.totalTrafficCapacity, CONFIG.simConfig.TRAFFIC_CAPACITY_RURAL)
        companies = self.setupCompanies(serviceArea, 100)
        for company in companies:
            company.ActivateBusinessProcess(100)
        #serviceArea.ChangeActivity(1000, 1.0, 2.0) #Should result in an activity of 1.0 (due to being capped)
        #self.assertEqual(serviceArea.activity, 1.0)
        
        #End test
        serviceArea.Terminate()
        
    def test_registerQoSPartialCapacityViolation(self):
        pass