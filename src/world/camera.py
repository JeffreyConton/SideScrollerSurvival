import pygame
from src.settings import SCREEN_WIDTH, SCREEN_HEIGHT

class Camera:
    def __init__(self, width, height):
        self.camera = pygame.Rect(0, 0, width, height)
        self.width = width
        self.height = height
        self.camera_x = 0
        self.camera_y = 0

    def apply(self, entity):
        return entity.rect.move(self.camera.topleft)

    def update(self, target):
        x = -target.rect.centerx + SCREEN_WIDTH // 2
        y = -target.rect.centery + SCREEN_HEIGHT // 2

        # limit scrolling to the bounds of the level
        x = max(-(self.width - SCREEN_WIDTH), x)  # right
        x = min(0, x)  # left

        y = max(-(self.height - SCREEN_HEIGHT), y)  # bottom
        y = min(0, y)  # top

        self.camera = pygame.Rect(x, y, self.width, self.height)
        self.camera_x = -self.camera.left
        self.camera_y = -self.camera.top