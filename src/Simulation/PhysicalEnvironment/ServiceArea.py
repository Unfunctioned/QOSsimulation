from Configuration.globals import CONFIG
from UI.Colors import Colors
import math
from DataOutput.DataRecorder import DataRecorder
from Simulation.NetworkEnvironment.LocalServiceNetwork import LocalServiceNetwork
'''Represents the service area in the simulation'''
class ServiceArea(object):
    
    def __init__(self, id, cell, areaType) -> None:
        self.id = id
        self.areaType = areaType
        self.cell = cell
        cell.colorcode = Colors.GetColorCodeByAreaType(self.areaType)
        self.areaSize = CONFIG.simConfig.scale(self.cell.area)
        self.userDensity = CONFIG.simConfig.get_user_density(self.areaType)
        self.totalUsers = math.floor(self.userDensity * self.areaSize)
        self.default_activity = CONFIG.simConfig.get_default_activity(self.areaType)
        self.activity = self.default_activity
        self.activityHistory = DataRecorder(self.id, 1, ["ACTIVITY"])
        self.activityHistory.createFileOutput(CONFIG.filePaths.serviceAreaPath, "ServiceArea")
        self.localServiceNetwork = LocalServiceNetwork(id, self.areaSize, self.areaType)
        self.ChangeActivity(0, 1.0, 0.0)
        
    def ChangeActivity(self, currentTime, modifier, activityBoost):
        self.activity = self.default_activity * modifier + activityBoost
        self.activityHistory.record(currentTime, [self.activity])
        activeUsers = math.floor(self.activity * self.totalUsers)
        self.localServiceNetwork.UpdateActivity(currentTime, activeUsers)
        
    def draw(self, window):
        self.cell.draw(window)
        scaled_site = self.cell.site[0]*window.window_size[0], self.cell.site[1]*window.window_size[1]
        textSurface1 = window.font.render('A: {activity} '.format(activity = round(self.activity, 4)), False, (0, 0, 0))
        window.screen.blit(textSurface1, scaled_site)
        
    def drawInfo(self, window):
        scaled_site = self.cell.site[0]*window.window_size[0], self.cell.site[1]*window.window_size[1]
        textSurface1 = window.font.render('A: {area} '.format(area = round(self.areaSize, 2)), False, (0, 0, 0))
        textSurface2 = window.font.render('U: {users} '.format(users = self.totalUsers), False, (0, 0, 0))
        height = textSurface1.get_height()
        window.screen.blit(textSurface1, scaled_site)
        window.screen.blit(textSurface2, (scaled_site[0], scaled_site[1]+height))