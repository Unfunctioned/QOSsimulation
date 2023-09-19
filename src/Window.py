import pygame
from Configuration.globals import *
from Simulation.WorldGenerator import *


class Window(object):
    
    def __init__(self) -> None:
        self.window_size = CONFIG.WINDOW_SIZE
        self.screen = pygame.display.set_mode([self.window_size[0], self.window_size[1]])
        self.worldGenerator = WorldGenerator()
        self.animate()
        
    def animate(self):
        pygame.init()
        voronoi = self.worldGenerator.voronoi
        
        # Run until the user asks to quit
        running = True
        while running:

            # Did the user click the window close button?
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

            self.draw()
            voronoi.draw(self)
            for point in self.worldGenerator.points:
                point.draw(self)
            pygame.display.update()
            
            # Flip the display
            pygame.display.flip()
            
        # Done! Time to quit.
        pygame.quit()
        

        
    def draw(self):
        # Fill the background with white
        self.screen.fill((255, 255, 255))