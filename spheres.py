import moderngl
import pygame
import numpy as np
import math

# Window parameters
LARGEUR = 800
HAUTEUR = 600
TITRE = "ESGI Spheres"
SPHERES_COUNT = 6
PIXEL_SIZE = 4  # Taille de chaque pixel rendu

camera_position = np.array([0.0, 0.0, -5.0], dtype='f4')
l_norm = math.sqrt(3.0)
light_dir = np.array([1.0 / l_norm, -1.0 / l_norm, -1.0 / l_norm], dtype='f4')

def generate_spheres_data(time, spheres_count):
    """Génère les positions, rayons et couleurs des sphères dynamiquement."""
    spheres_data = []
    for sphere_id in range(spheres_count):
        x = math.sin(sphere_id * 1274 + 0.2 * time)
        y = math.sin(sphere_id * 127478 + (0.3 + sphere_id * 0.1) * time)
        z = math.sin(sphere_id * 8899 + 0.5 * time)
        r = 0.375 + 0.25 * math.sin(sphere_id * 855) + 0.1 * math.sin(time)

        color = (
            ((sphere_id * 1337 + 127) % 256) / 255.0,
            ((sphere_id * 133712 + 127) % 256) / 255.0,
            ((sphere_id * 13371234 + 127) % 256) / 255.0
        )

        spheres_data.extend([x, y, z, r, *color])

    return np.array(spheres_data, dtype='f4')

def create_compute_shader(ctx):
    """Crée le shader de calcul pour rendre les sphères."""
    compute_shader_code = """
    #version 430

    layout(local_size_x = 8, local_size_y = 8) in;

    uniform vec3 camera_position;
    uniform vec3 light_dir;
    uniform float time;
    uniform vec2 resolution;

    struct Pixel {
        vec2 coord;
        vec3 color;
    };

    struct Sphere {
        vec3 center;
        float radius;
        vec3 color;
    };

    layout(std430, binding = 0) buffer PixelBuffer {
        Pixel pixels[];
    };

    layout(std430, binding = 1) buffer Spheres {
        Sphere spheres[];
    };

    float sphere_intersection(vec3 ray_origin, vec3 ray_dir, vec3 center, float radius) {
        vec3 oc = ray_origin - center;
        float b = dot(oc, ray_dir);
        float c = dot(oc, oc) - radius * radius;
        float h = b * b - c;
        if (h < 0.0) return -1.0;
        return -b - sqrt(h);
    }

    void main() {
        ivec2 pixel_coords = ivec2(gl_GlobalInvocationID.xy);
        if (pixel_coords.x >= int(resolution.x) || pixel_coords.y >= int(resolution.y)) return;

        int index = pixel_coords.y * int(resolution.x) + pixel_coords.x;

        vec2 uv = (vec2(pixel_coords) / resolution) * 2.0 - 1.0;
        uv.x *= resolution.x / resolution.y;

        vec3 ray_origin = camera_position;
        vec3 ray_dir = normalize(vec3(uv, 1.0));

        float nearest_t = 1e6;
        vec3 pixel_color = vec3(0.0);

        for (int i = 0; i < spheres.length(); i++) {
            Sphere sphere = spheres[i];
            float t = sphere_intersection(ray_origin, ray_dir, sphere.center, sphere.radius);
            if (t > 0.0 && t < nearest_t) {
                nearest_t = t;
                vec3 hit_point = ray_origin + t * ray_dir;
                vec3 normal = normalize(hit_point - sphere.center);
                float light_intensity = max(dot(normal, light_dir), 0.2);
                pixel_color = sphere.color * light_intensity;
            }
        }

        pixels[index].coord = vec2(pixel_coords);
        pixels[index].color = pixel_color;
    }
    """
    return ctx.compute_shader(compute_shader_code)

def main():
    pygame.init()
    screen = pygame.display.set_mode((LARGEUR, HAUTEUR))
    pygame.display.set_caption(TITRE)

    ctx = moderngl.create_context(standalone=True)
    compute_shader = create_compute_shader(ctx)

    pixel_count = (LARGEUR * HAUTEUR) // PIXEL_SIZE
    pixel_buffer = ctx.buffer(reserve=pixel_count * 5 * 4)  # Chaque pixel a 2 coords (vec2) + 3 couleurs (vec3)
    pixel_buffer.bind_to_storage_buffer(0)

    sphere_buffer = ctx.buffer(reserve=SPHERES_COUNT * 7 * 4)  # 7 floats par sphère
    sphere_buffer.bind_to_storage_buffer(1)

    running = True
    clock = pygame.time.Clock()

    while running:
        time = pygame.time.get_ticks() / 1000.0
        spheres_data = generate_spheres_data(time, SPHERES_COUNT)
        sphere_buffer.write(spheres_data)

        compute_shader['camera_position'].value = tuple(camera_position)
        compute_shader['light_dir'].value = tuple(light_dir)
        compute_shader['resolution'].value = (LARGEUR, HAUTEUR)

        compute_shader.run(group_x=LARGEUR // 8, group_y=HAUTEUR // 8)

        # Lire les données depuis le buffer
        pixel_data = np.frombuffer(pixel_buffer.read(), dtype=np.float32).reshape((pixel_count, 5))

        # Préparer les pixels pour pygame
        pixel_colors = (pixel_data[:, 2:] * 255).astype(np.uint8)  # Couleurs [r, g, b]
        pixels = pixel_colors.reshape((HAUTEUR, LARGEUR, 3))

        # Dessiner les pixels avec la taille ajustée
        for y in range(0, HAUTEUR, PIXEL_SIZE):
            for x in range(0, LARGEUR, PIXEL_SIZE):
                color = pixels[y // PIXEL_SIZE, x // PIXEL_SIZE]
                pygame.draw.rect(screen, color, (x, y, PIXEL_SIZE, PIXEL_SIZE))

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        clock.tick(60)

    pygame.quit()

if __name__ == "__main__":
    main()
