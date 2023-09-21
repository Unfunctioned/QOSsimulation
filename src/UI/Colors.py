from Configuration.globals import CONFIG
from Simulation.PhysicalEnvironment.AreaType import AreaType
from UI.ColorCode import *
'''Class to configure the color of UI elements'''
class Colors(object):
    
    def GetRandomColorCode():
        colors = list(ColorCode)
        return CONFIG.randoms.colorGeneration.choice(colors)
    
    def GetColor(colorCode):
        match colorCode:
            case ColorCode.RED:
                return (255, 0, 0)
            case ColorCode.YELLOW:
                return (236, 240, 7)
            case ColorCode.GREEN:
                return (0, 255, 0)
            case ColorCode.WHITE:
                return (255, 255, 255)
            case _ :
                ValueError("Invalid code")
                
    def GetLightVariant(colorcode):
        color = Colors.GetColor(colorcode)
        r = max(color[0], 150)
        g = max(color[1], 150)
        b = max(color[2], 150)
        return (r,g,b)
    
    def GetColorCodeByAreaType(areaType):
        colorCode = None
        match areaType:
            case AreaType.RURAL:
                return ColorCode.GREEN
            case AreaType.URBAN:
                return ColorCode.YELLOW
            case AreaType.DENSE_URBAN:
                return ColorCode.RED
            case AreaType.NONE:
                return ColorCode.WHITE