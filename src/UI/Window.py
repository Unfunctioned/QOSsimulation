import pygame
from Configuration.globals import *
from Simulation.WorldGenerator import *


class Window(object):
    
    def __init__(self) -> None:
        pygame.init()
        pygame.font.init()
        self.window_size = CONFIG.uiSettings.WINDOW_SIZE
        self.screen = pygame.display.set_mode([self.window_size[0], self.window_size[1]])
        self.font = pygame.font.SysFont('Comic Sans MS', 14)
        worldGenerator = WorldGenerator()
        self.world = worldGenerator.get_world()
        self.animate()
        
    def animate(self):
        # Run until the user asks to quit
        running = True
        while running:

            # Did the user click the window close button?
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

            self.world.Update()
            self.draw()
            self.world.draw(self)
            pygame.display.update()
            
            # Flip the display
            pygame.display.flip()
            
            #Check if simulation is complete
            if(not self.world.isRunning()):
                running = False            
        # Done! Time to quit.
        self.world.Terminate()
        pygame.quit()
        

        
    def draw(self):
        # Fill the background with white
        self.screen.fill((255, 255, 255))