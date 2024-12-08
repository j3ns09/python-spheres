import numpy as np
import moderngl
import pygame

# Constants
WIDTH, HEIGHT = 400, 400
TITRE = "Sphere ray tracing"

def create_compute_shader():
    pass

def main():
    pygame.init()

    # Creation of pygame screen
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption(TITRE)

    # Creating context for OpenGL
    ctx = moderngl.create_context(standalone=True)

    # Holder of pixel data
    # HEIGHT rows, WIDTH lines
    #
    # In the compute shader, use 16 rows for each workgroup -> meaning that 25 workgroups are needed
    # Dispatch with dimensions x = 5, y = 5, z = 1
    #
    # This will result in each workgroup handling 16 * WIDTH pixels
    # Currently, this means 16 * 400 = 6400 pixels in total
    #
    # I'll use 64 threads (x = 4, y = 4, z = 4) to make each thread process 100 pixels

    pixels = np.zeros((HEIGHT, WIDTH))
    # Creation of compute shader + buffer
    # compute_shader =

    for y in range(HEIGHT):
        for x in range(WIDTH):
            pixels[y][x] = 5

if __name__ == "__main__":
    main()
