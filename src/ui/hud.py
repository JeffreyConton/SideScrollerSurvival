import pygame
from src.settings import SCREEN_WIDTH, WHITE

class HUD:
    def __init__(self):
        self.font = pygame.font.Font(None, 36)

    def draw_fps(self, screen, clock):
        fps = int(clock.get_fps())
        fps_text = self.font.render(f"FPS: {fps}", True, WHITE)
        screen.blit(fps_text, (10, 10))

    def draw_time(self, screen, time_system):
        current_time = time_system.get_time()
        time_text = (f"Year: {current_time['years']}, "
                     f"Month: {current_time['months'] + 1}, "
                     f"Week: {current_time['weeks'] + 1}, "
                     f"Day: {current_time['days'] + 1}, "
                     f"Hour: {current_time['hours']}, "
                     f"Minute: {current_time['minutes']}")
        time_surface = self.font.render(time_text, True, WHITE)
        screen.blit(time_surface, (10, 40))