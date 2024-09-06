#include <cuda_runtime.h>
#include <device_launch_parameters.h>

// CUDA kernel for hyperspace effect
__global__ void hyperspace_effect(unsigned char* screen, int width, int height, int time) {
    int x = blockIdx.x * blockDim.x + threadIdx.x;
    int y = blockIdx.y * blockDim.y + threadIdx.y;

    if (x < width && y < height) {
        int offset = (y * width + x) * 3;
        screen[offset] = (x + time) % 255;  // Red channel
        screen[offset + 1] = (y + time) % 255;  // Green channel
        screen[offset + 2] = 128;  // Blue channel
    }
}

extern "C" void run_hyperspace_effect(unsigned char* screen, int width, int height, int time) {
    dim3 blockSize(16, 16);
    dim3 gridSize((width + blockSize.x - 1) / blockSize.x, (height + blockSize.y - 1) / blockSize.y);
    hyperspace_effect<<<gridSize, blockSize>>>(screen, width, height, time);
    cudaDeviceSynchronize();
}
