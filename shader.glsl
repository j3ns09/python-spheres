#version 430

layout (local_size_x = 1, local_size_y = 1) in;

layout(std430, binding = 0) buffer PixelBuffer {
    uvec3 pixels[];
};

uint add_one(uint num) {
    return (num + 1) % 256;
}

void main() {
    const uint index = gl_GlobalInvocationID.x;
    const uint mask = 0xFF;

    uvec3 color = pixels[index];

    uint r = color.r;
    uint g = color.g;
    uint b = color.b;

    r = add_one(r);
    b = add_one(b);
    g = add_one(g);

    pixels[index] = uvec3(r, g, b);
}