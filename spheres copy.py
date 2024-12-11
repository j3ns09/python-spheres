from random import randint
import numpy as np
import moderngl
import pygame

# ---- Constants ----
# Pygame constants
WIDTH, HEIGHT = 400, 400
TITRE = "Sphere ray tracing"

# Moderngl constants
GROUP_X, GROUP_Y = 25, 25

# Color constants
BIT_MASK = 0xFF

def rgba_decode(pixel):
    r = (pixel >> 24) & BIT_MASK
    g = (pixel >> 16) & BIT_MASK
    b = (pixel >> 8) & BIT_MASK
    a = pixel & BIT_MASK
    return r, g, b, a

def get_source_shader() -> str:
    with open("shader.glsl", 'r', encoding='utf-8') as file:
        code = file.read()
    return code

def run_shader(context: moderngl.Context, program: moderngl.ComputeShader, data: np.ndarray) -> np.ndarray:
    flattened_data = data.flatten()
    buffer = context.buffer(flattened_data)
    
    buffer.write(flattened_data)
    buffer.bind_to_storage_buffer(0)

    program.run(len(flattened_data), 1)
    
    buffer.read_into(flattened_data)

    result = np.reshape(flattened_data, data.shape)
    
    buffer.release()
    return result


def init_pygame():
    global screen, running, clock
    
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption(TITRE)
    running = True
    clock = pygame.time.Clock()

def draw_pixels(pixel_array: np.ndarray):
    global l
    l += 1

    surface = pygame.surfarray.make_surface(pixel_array)
    screen.blit(surface, (0, 0))
    print("Done drawing", l)

def main():
    global screen, running, clock, l
    l = 0
    

    init_pygame()

    # Creating context for OpenGL
    ctx : moderngl.Context = moderngl.create_context(standalone=True)
    compute_shader : moderngl.ComputeShader = ctx.compute_shader(get_source_shader())
    
    # Holder of pixel data
    pixels = np.full((WIDTH, HEIGHT, 3), [0, 0, 0], dtype=np.uint8)
    
    while running:
        pixels = run_shader(ctx, compute_shader, pixels)
        draw_pixels(pixels)
        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        
        clock.tick(60)
    
if __name__ == "__main__":
    main()