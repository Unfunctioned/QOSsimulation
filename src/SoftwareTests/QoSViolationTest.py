import unittest
from Utilities.VoronoiDiagram.Cell import Cell
from Simulation.PhysicalEnvironment.AreaType import AreaType
from Simulation.PhysicalEnvironment.ServiceArea import ServiceArea
from Configuration.globals import GetConfig
from Simulation.BusinessEnvironment.Company import Company
from Simulation.BusinessEnvironment.BusinessProcessFactory import BuisnessProcessFactory
from DataOutput.MockTimeDataRecorder import MockTimeDataRecorder

class QoSViolationTest(unittest.TestCase):
    
    def setupServiceArea(self):
        unitsize = 1.0 / GetConfig().simConfig.SCALE
        cell = Cell([unitsize / 2, unitsize / 2], [[0.0,0.0],[unitsize,0.0],[unitsize,unitsize],[0.0,unitsize]])
        serviceArea = ServiceArea(0, cell, AreaType.RURAL)
        cell2 = Cell([unitsize / 2, unitsize / 2], [[0.0,0.0],[unitsize,0.0],[unitsize,unitsize],[0.0,unitsize]])
        cell.addNeighbour(cell2)
        cell2.addNeighbour(cell)
        serviceArea2 = ServiceArea(1, cell2, AreaType.RURAL)
        serviceArea.InitializeNetwork(0)
        serviceArea2.InitializeNetwork(0)
        self.assertEqual(serviceArea.areaSize, 1.0)
        return serviceArea, serviceArea2
    
    def setupCompanies(self, serviceAreas, companyCount) -> list[Company]:
        companies = []
        BuisnessProcessFactory.SetServiceAreas(serviceAreas)
        BuisnessProcessFactory.SetBusinessProcessFlows()
        for i in range(companyCount):
            processFlow = BuisnessProcessFactory.SelectBusinessProcessFlow()
            companies.append(Company(i, serviceAreas[0], processFlow, MockTimeDataRecorder()))
        return companies
            
    def test_registerQoSTotalCapacityViolation(self):
        serviceArea, serviceArea2 = self.setupServiceArea()
        network = serviceArea.localServiceNetwork
        self.assertEqual(network.totalTrafficCapacity, GetConfig().simConfig.TRAFFIC_CAPACITY_RURAL)
        companies = self.setupCompanies([serviceArea, serviceArea2], 100)
        for company in companies:
            company.ActivateBusinessProcess(100)
        serviceArea.ChangeActivity(1000, 1.0, 2.0) #Should result in an activity of 1.0 (due to being capped)
        self.assertEqual(serviceArea.activity, 1.0)
        
        #End test
        company : Company
        for company in companies:
            company.terminate()
        serviceArea.Terminate()
        serviceArea2.Terminate()