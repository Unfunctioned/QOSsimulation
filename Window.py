import pygame
from Config import *
from WorldGenerator import *

class Window(object):
    
    def __init__(self) -> None:
        self.config = Config()
        self.window_size = self.config.WINDOW_SIZE
        self.screen = pygame.display.set_mode([self.window_size[0], self.window_size[1]])
        self.worldGenerator = WorldGenerator(self.config)
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
            pygame.display.update()
            
            # Flip the display
            pygame.display.flip()
            
        # Done! Time to quit.
        pygame.quit()
        

        
    def draw(self):
        # Fill the background with white
        self.screen.fill((255, 255, 255))