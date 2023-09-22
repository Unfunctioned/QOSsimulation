from Configuration.globals import CONFIG
from Simulation.PhysicalEnvironment.AreaType import AreaType
from UI.Colors import Colors
import math
'''Represents the service area in the simulation'''
class ServiceArea(object):
    
    def __init__(self, cell, areaType) -> None:
        self.areaType = areaType
        self.cell = cell
        cell.colorcode = Colors.GetColorCodeByAreaType(self.areaType)
        self.areaSize = CONFIG.simConfig.scale(self.cell.area)
        self.userPool = CONFIG.simConfig.get_user_density(self.areaType)
        self.totalUsers = math.floor(self.userPool * self.areaSize)
        self.default_activity = CONFIG.simConfig.get_default_activity(self.areaType)
        self.activity = self.default_activity
        
    def ChangeActivity(self, modifier):
        self.activity = self.default_activity * modifier
        
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