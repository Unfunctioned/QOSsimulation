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
        self.worldGenerator = WorldGenerator()
        self.animate()
        
    def animate(self):
        # Run until the user asks to quit
        running = True
        while running:

            # Did the user click the window close button?
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

            self.draw()
            self.worldGenerator.draw(self)
            pygame.display.update()
            
            # Flip the display
            pygame.display.flip()
            
        # Done! Time to quit.
        pygame.quit()
        

        
    def draw(self):
        # Fill the background with white
        self.screen.fill((255, 255, 255))