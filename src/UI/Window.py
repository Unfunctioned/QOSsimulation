import pygame
from Configuration.globals import GetConfig
from Simulation.WorldGenerator import *
from pathlib import Path


class Window(object):
    
    def __init__(self, showOutput = False) -> None:
        self.showPutput = showOutput
        self.window_size = GetConfig().uiSettings.WINDOW_SIZE
        self.screen = None
        self.font = None
        if showOutput:
            pygame.display.init()
            pygame.font.init()
            self.screen = pygame.display.set_mode([self.window_size[0], self.window_size[1]])
            self.font = pygame.font.SysFont('Comic Sans MS', 14)
        worldGenerator = WorldGenerator(showOutput)
        self.world = worldGenerator.get_world()
        self.animate()
        
    def GetSimulationTime(self):
        return self.world.GetSimulationTime()
        
    def animate(self):
        # Run until the user asks to quit
        running = True
        while running:

            if self.showPutput:
                # Did the user click the window close button?
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        running = False

            self.world.Update(self.showPutput)
            if self.showPutput:
                self.draw()
                self.world.draw(self)
                pygame.display.update()
            
                # Flip the display
                pygame.display.flip()
            
            #Check if simulation is complete
            if(not self.world.isRunning(self.showPutput)):
                running = False            
        # Done! Time to quit.
        self.world.Terminate()
        pygame.quit()
        

        
    def draw(self):
        # Fill the background with white
        self.screen.fill((255, 255, 255))
        
    def getImage(self, id):
        pygame.display.init()
        pygame.font.init()
        self.screen = pygame.Surface([self.window_size[0], self.window_size[1]])
        self.font = pygame.font.SysFont('Comic Sans MS', 14)
        self.draw()
        self.world.draw(self)
            
        # Flip the display
        pygame.transform.flip(self.screen, flip_x=False, flip_y=True)
        Path().absolute()
        pygame.image.save(self.screen, "World#{no}.jpeg".format(no = id))
        self.screen = None