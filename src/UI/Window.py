import pygame
from Configuration.globals import GetConfig
from Simulation.World import World

class Window(object):
    
    def __init__(self, world : World, showOutput = False) -> None:
        self.showPutput = showOutput
        self.screen = None
        self.font = None
        if self.showPutput:
            self._initPygame()
            resolution = GetConfig().appSettings.WINDOW_SIZE
            self.screen = pygame.display.set_mode([resolution[0], resolution[1]])
            self.font = pygame.font.SysFont('Comic Sans MS', 14)
        self.world = world
        
    def GetSimulationTime(self) -> int:
        return self.world.GetSimulationTime()
    
    def animate(self):
        isRunning = True
        while isRunning:

            isRunning = self.handleEvents()
            self.world.Update(self.showPutput)
            self.draw()
            
            #Check if simulation is complete
            if(not self.world.isRunning(self.showPutput)):
                isRunning = False        
        self.world.Terminate()
        self.world.printInfo()  
        pygame.quit()
        
    def handleEvents(self):
        if self.showPutput:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return False
        return True
        

        
    def draw(self):
        if self.showPutput:
            # Fill the background with white
            self.screen.fill((255, 255, 255))
            self.world.draw(self.screen, self.font)
            pygame.display.update()
            # Flip the display
            pygame.display.flip()
        
    def getImage(self, id):
        self._initPygame()
        resolution = GetConfig().appSettings.WINDOW_SIZE
        self.screen = pygame.Surface([resolution[0], resolution[1]])
        self.font = pygame.font.SysFont('Comic Sans MS', 14)
        self.screen.fill((255, 255, 255))
        self.world.draw(self.screen, self.font)
        
        pygame.image.save(self.screen, GetConfig().filePaths.simulationPath.joinpath("World#{no}.jpeg".format(no = id)))
        self._unloadPygame()
    
    def _initPygame(self):
        pygame.display.init()
        pygame.font.init()
    
    def _unloadPygame(self):
        if not self.showPutput:
            self.screen = None
            pygame.display.quit()
            pygame.font.quit()
            