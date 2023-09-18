import random
'''Class to configure the color of UI elements'''
class Colors(object):
    
    def GetRandomColor():
        i = random.randint(0,2)
        match i:
            case 0:
                return (255, 0, 0)
            case 1:
                return (236, 240, 7)
            case 2:
                return (0, 255, 0)
            case _ :
                ValueError("Invalid case")
                
    def GetLightVariant(color):
        r = max(color[0], 150)
        g = max(color[1], 150)
        b = max(color[2], 150)
        return (r,g,b)