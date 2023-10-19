from Configuration.globals import GetConfig
from UI.Colors import Colors
import math
from DataOutput.TimeDataRecorder import TimeDataRecorder
from Simulation.NetworkEnvironment.LocalServiceNetwork import LocalServiceNetwork
from Simulation.NetworkEnvironment.PublicSlice import PublicSlice
from Simulation.NetworkEnvironment.ServiceRequirements.ServiceRequirement import DynamicServiceRequirement
from Simulation.NetworkEnvironment.NetworkSlice import NetworkSlice
from Utilities.VoronoiDiagram.Cell import Cell
'''Represents the service area in the simulation'''
class ServiceArea(object):
    
    def __init__(self, id, cell : Cell, areaType) -> None:
        self.id = id
        self.areaType = areaType
        self.cell = cell
        cell.colorcode = Colors.GetColorCodeByAreaType(self.areaType)
        self.areaSize = GetConfig().simConfig.scale(self.cell.area)
        self.userDensity = GetConfig().simConfig.get_user_density(self.areaType)
        self.totalUsers = math.floor(self.userDensity * self.areaSize)
        self.default_activity = GetConfig().simConfig.get_default_activity(self.areaType)
        self.activity = self.default_activity
        self.activityHistory = TimeDataRecorder(self.id, ["ACTIVITY"])
        self.activityHistory.createFileOutput(GetConfig().filePaths.serviceAreaPath, "ServiceArea")
        self.localServiceNetwork = None
    
    def InitializeNetwork(self, currentTime):
        localNetworkFolderPath = LocalServiceNetwork.InitializeOutputFolder(self.id)
        trafficCapacity = self.areaSize * GetConfig().simConfig.get_traffic_capacity(self.areaType)
        userDemands = (5, GetConfig().simConfig.BASIC_DATA_RATE_DEMAND)
        serviceRequirement = DynamicServiceRequirement(userDemands, None, 0, GetConfig().simConfig.PUBLIC_SLICE_RELIABILITY, 0)
        publicSlice = PublicSlice(localNetworkFolderPath)
        
        self.localServiceNetwork = LocalServiceNetwork(self.id, localNetworkFolderPath, trafficCapacity, publicSlice)
        self.ActivateNetworkSlice(currentTime, publicSlice, serviceRequirement)
        self.ChangeActivity(currentTime, 1.0, 0)
    
    def ChangeActivity(self, currentTime, modifier, activityBoost = 0):
        self.activity = min(self.default_activity * modifier + activityBoost, 1.0)
        self.activityHistory.record(currentTime, [self.activity])
        activeUsers = math.floor(self.activity * self.totalUsers)
        self.localServiceNetwork.UpdateActivity(currentTime, activeUsers)
        
    def ActivateNetworkSlice(self, currentTime, networkSlice : NetworkSlice, serviceRequirement):
        networkSlice.addServiceRequirement(self.id, serviceRequirement)
        self.localServiceNetwork.ActivateNetworkSlice(currentTime, networkSlice)
        
    def DeactivateNetworkSlice(self, currentTime, networkSlice : NetworkSlice, serviceRequirement):
                networkSlice.removeServiceRequirement(self.id, serviceRequirement)
                if not networkSlice.hasActiveRequirements(self.id):
                    self.localServiceNetwork.DeactivateNetworkSlice(currentTime, networkSlice)
        
    def Terminate(self):
        self.activityHistory.terminate()
        self.localServiceNetwork.terminate()
        self.localServiceNetwork = None
        
    def draw(self, window):
        self.cell.draw(window)
        scaled_site = self.cell.site[0]*window.window_size[0], self.cell.site[1]*window.window_size[1]
        textSurface1 = window.font.render('ID: {id} '.format(id = self.id), False, (0, 0, 0))
        window.screen.blit(textSurface1, scaled_site)
        
    def drawInfo(self, window):
        scaled_site = self.cell.site[0]*window.window_size[0], self.cell.site[1]*window.window_size[1]
        textSurface1 = window.font.render('A: {area} '.format(area = round(self.areaSize, 2)), False, (0, 0, 0))
        textSurface2 = window.font.render('U: {users} '.format(users = self.totalUsers), False, (0, 0, 0))
        height = textSurface1.get_height()
        window.screen.blit(textSurface1, scaled_site)
        window.screen.blit(textSurface2, (scaled_site[0], scaled_site[1]+height))