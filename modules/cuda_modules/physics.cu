#include <cuda_runtime.h>
#include <device_launch_parameters.h>

__global__ void apply_gravity(float* position, float* velocity, float gravity, int size) {
    int i = blockIdx.x * blockDim.x + threadIdx.x;
    if (i < size) {
        velocity[i] += gravity;
        position[i] += velocity[i];
    }
}

extern "C" void run_apply_gravity(float* position, float* velocity, float gravity, int size) {
    int blockSize = 256;
    int gridSize = (size + blockSize - 1) / blockSize;
    apply_gravity<<<gridSize, blockSize>>>(position, velocity, gravity, size);
    cudaDeviceSynchronize();
}
