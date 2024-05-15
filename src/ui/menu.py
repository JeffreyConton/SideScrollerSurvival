import pygame
from src.settings import SCREEN_WIDTH, SCREEN_HEIGHT, WHITE, BLACK

class Menu:
    def __init__(self):
        self.font = pygame.font.Font(None, 74)
        self.options = ["Start Game", "Load Save", "Settings", "Quit"]
        self.selected = 0

    def display_menu(self, screen):
        screen.fill(BLACK)
        for i, option in enumerate(self.options):
            if i == self.selected:
                label = self.font.render(option, True, WHITE)
            else:
                label = self.font.render(option, True, (100, 100, 100))
            width = label.get_width()
            height = label.get_height()
            posX = (SCREEN_WIDTH / 2) - (width / 2)
            posY = (SCREEN_HEIGHT / 2) - (height / 2) + (i * 100)
            screen.blit(label, (posX, posY))

    def handle_input(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                self.selected = (self.selected - 1) % len(self.options)
            elif event.key == pygame.K_DOWN:
                self.selected = (self.selected + 1) % len(self.options)
            elif event.key == pygame.K_RETURN:
                return self.options[self.selected]
        return None