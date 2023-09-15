import pygame
from RandomPointSpawner import *

from pygame.locals import *

WINDOW_SIZE = (720,720)
FPS = 60

pygame.init()
screen = pygame.display.set_mode([WINDOW_SIZE[0], WINDOW_SIZE[1]])
pointSpawner = RandomPointSpawner()

#Generate points
points = pointSpawner.SpawnPoints(500)
numberPoints = pointSpawner.SpawnPoints(100)

# Run until the user asks to quit
running = True
while running:

    # Did the user click the window close button?
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Fill the background with white
    screen.fill((255, 255, 255))

    try:
    #Draw the points
        for i in range(len(points)):
            (x,y) = points[i]
            pygame.draw.circle(screen, (0, 0, 0), (x*WINDOW_SIZE[0], y*WINDOW_SIZE[1]), 3)
        
        for i in range(len(numberPoints)):
            (x,y) = numberPoints[i]
            '''Displays a number on that tile'''
            font = pygame.font.SysFont('arial', 24)
            text = font.render(str(random.randint(0,9)), True, (0, 0, 255))
            screen.blit(text, (x*WINDOW_SIZE[0], y*WINDOW_SIZE[1]))
        pygame.display.update()
    except:
        print("Fail")
    
    # Flip the display
    pygame.display.flip()

# Done! Time to quit.
pygame.quit()