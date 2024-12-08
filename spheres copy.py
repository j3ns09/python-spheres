import numpy as np
import moderngl
import pygame

# Constants
WIDTH, HEIGHT = 400, 400
TITRE = "Sphere ray tracing"

def 

def main():
    pygame.init()
    
    # Creation of pygame screen
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption(TITRE)
    
    # Creating context for OpenGL
    ctx = moderngl.create_context(standalone=True)
    
    # Holder of pixel data
    pixels = np.zeros((HEIGHT, WIDTH))
    # Creation of compute shader + buffer
    # compute_shader = 
    
    for y in range(HEIGHT):
        for x in range(WIDTH):
            pixels[y][x] = 5
    
if __name__ == "__main__":
    main()