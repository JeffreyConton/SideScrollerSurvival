import pygame
from src.settings import WHITE

class HUD:
    def __init__(self, font_size=30):
        self.font = pygame.font.SysFont(None, font_size)

    def draw_fps(self, screen, clock):
        fps = clock.get_fps()
        fps_text = self.font.render(f"FPS: {int(fps)}", True, WHITE)
        screen.blit(fps_text, (10, 10))