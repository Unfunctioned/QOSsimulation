from Configuration.globals import GetConfig
from UI.Colors import Colors
import math
from DataOutput.TimeDataRecorder import TimeDataRecorder
from Simulation.NetworkEnvironment.LocalServiceNetwork import LocalServiceNetwork
from Simulation.NetworkEnvironment.PublicSlice import PublicSlice
from Simulation.NetworkEnvironment.ServiceRequirements.ServiceRequirement import DynamicServiceRequirement
from Simulation.NetworkEnvironment.NetworkSlice import NetworkSlice
from Utilities.VoronoiDiagram.Cell import Cell
from pygame import Surface
from pygame.font import Font
from Simulation.NetworkEnvironment.ServiceRequirements.ServiceRequirement import ServiceRequirement
from Configuration.SimulationMode import SimulationMode
from Utilities.ItemTypes.ReservationItem import ReservationItem

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
    
    def InitializeNetwork(self, currentTime : int):
        localNetworkFolderPath = LocalServiceNetwork.InitializeOutputFolder(self.id)
        trafficCapacity = self.areaSize * GetConfig().simConfig.get_traffic_capacity(self.areaType)
        userDemands = (5, GetConfig().simConfig.BASIC_DATA_RATE_DEMAND)
        serviceRequirement = DynamicServiceRequirement(userDemands, None, 0, GetConfig().simConfig.PUBLIC_SLICE_RELIABILITY, 0)
        publicSlice = PublicSlice(localNetworkFolderPath)
        
        self.localServiceNetwork = LocalServiceNetwork(self.id, localNetworkFolderPath, trafficCapacity, publicSlice)
        if GetConfig().simConfig.SIMULATION_MODE == SimulationMode.SCHEDULING:
            self.localServiceNetwork.ScheduleNetworkSlice(currentTime, publicSlice, ReservationItem(-1, -1, publicSlice, serviceRequirement))
        self.localServiceNetwork.ActivateNetworkSlice(currentTime, publicSlice, serviceRequirement)
        self.ChangeActivity(currentTime, 1.0, 0)
    
    def ChangeActivity(self, currentTime, modifier, activityBoost = 0):
        self.activity = min(self.default_activity * modifier + activityBoost, 1.0)
        self.activityHistory.record(currentTime, [self.activity])
        activeUsers = math.floor(self.activity * self.totalUsers)
        self.localServiceNetwork.UpdateActivity(currentTime, activeUsers)
        
    def GetLocalServiceNetwork(self):
        return self.localServiceNetwork
    
    #def UpdateServiceNetwork(self, currentTime):
    #    activeUsers = math.floor(self.activity * self.totalUsers)
    #    self.localServiceNetwork.UpdateActivity(currentTime, activeUsers)
        
    def Terminate(self):
        self.activityHistory.terminate()
        self.localServiceNetwork.terminate()
        self.cell.Terminate()
        self.cell = None
        self.localServiceNetwork = None
        
    def draw(self, screen : Surface, font : Font):
        resolution = GetConfig().appSettings.WINDOW_SIZE
        self.cell.draw(screen)
        scaled_site = self.cell.site[0]*resolution[0], self.cell.site[1]*resolution[1]
        textSurface1 = font.render('ID: {id} '.format(id = self.id), False, (0, 0, 0))
        screen.blit(textSurface1, scaled_site)
        
    def drawInfo(self, screen : Surface, font : Font):
        resolution = GetConfig().appSettings.WINDOW_SIZE
        scaled_site = self.cell.site[0]*resolution[0], self.cell.site[1]*resolution[1]
        textSurface1 = font.render('A: {area} '.format(area = round(self.areaSize, 2)), False, (0, 0, 0))
        textSurface2 = font.render('U: {users} '.format(users = self.totalUsers), False, (0, 0, 0))
        height = textSurface1.get_height()
        screen.blit(textSurface1, scaled_site)
        screen.blit(textSurface2, (scaled_site[0], scaled_site[1]+height))