import pygame
import random
import math
from src.settings import GRID_SIZE, GREEN

def generate_terrain(rows, cols, num_octaves=3):
    terrain = []

    # Generate base height map using stacked sine waves with random factors
    height_map = [0] * cols

    for octave in range(num_octaves):
        frequency = 0.05 * (2 ** octave) * random.uniform(0.8, 1.2)
        amplitude = (rows / 8) / (2 ** octave) * random.uniform(0.8, 1.2)  # Reduced amplitude
        for col in range(cols):
            height_map[col] += int((math.sin(col * frequency) + 1) * amplitude)

    # Normalize the height map
    min_height = min(height_map)
    max_height = max(height_map)
    for col in range(cols):
        height_map[col] = (height_map[col] - min_height) / (max_height - min_height) * (rows - 1)

    # Smooth the height map
    height_map = smooth_height_map(height_map, smooth_factor=4)  # Increased smoothing

    # Generate terrain based on the height map
    for row in range(rows):
        terrain_row = []
        for col in range(cols):
            if row > rows - height_map[col]:
                terrain_row.append(1)  # Ground
            else:
                terrain_row.append(0)  # Air
        terrain.append(terrain_row)

    return terrain

def smooth_height_map(height_map, smooth_factor=4):
    smoothed = height_map[:]
    for i in range(smooth_factor):
        for col in range(1, len(height_map) - 1):
            smoothed[col] = (height_map[col - 1] + height_map[col] + height_map[col + 1]) / 3
        height_map = smoothed[:]
    return smoothed

def draw_terrain(screen, terrain, camera_x, camera_y):
    rows = len(terrain)
    cols = len(terrain[0])

    for row in range(rows):
        start_col = -1
        for col in range(cols):
            if terrain[row][col] == 1:
                if start_col == -1:
                    start_col = col
            else:
                if start_col != -1:
                    rect = pygame.Rect((start_col * GRID_SIZE) - camera_x, (row * GRID_SIZE) - camera_y, (col - start_col) * GRID_SIZE, GRID_SIZE)
                    pygame.draw.rect(screen, GREEN, rect)
                    start_col = -1
        if start_col != -1:
            rect = pygame.Rect((start_col * GRID_SIZE) - camera_x, (row * GRID_SIZE) - camera_y, (cols - start_col) * GRID_SIZE, GRID_SIZE)
            pygame.draw.rect(screen, GREEN, rect)