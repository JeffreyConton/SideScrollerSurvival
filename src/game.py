import pygame
from src.settings import SCREEN_WIDTH, SCREEN_HEIGHT, BLACK, WHITE, FPS, GRID_SIZE
from src.world.camera import Camera
from src.entities.player import Player
from src.world.terrain import generate_terrain, draw_terrain, expand_terrain
from src.ui.menu import Menu
from src.ui.hud import HUD
from src.systems.save_load import save_game, load_game

class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("2D Side-Scroller with Procedural Terrain")
        self.clock = pygame.time.Clock()
        self.running = True
        self.playing = False

        self.menu = Menu()

        self.camera = Camera(SCREEN_WIDTH * 10, SCREEN_HEIGHT * 2)  # Adjusted for taller levels

        self.all_sprites = pygame.sprite.Group()
        self.player = Player()
        self.all_sprites.add(self.player)

        self.rows = SCREEN_HEIGHT * 2 // GRID_SIZE  # Adjusted for taller levels
        self.cols = SCREEN_WIDTH * 10 // GRID_SIZE
        self.terrain = generate_terrain(self.rows, self.cols)

        self.hud = HUD()

    def run(self):
        while self.running:
            if self.playing:
                self.events()
                self.update()
                self.draw()
            else:
                self.menu_events()
                self.menu.display_menu(self.screen)
                pygame.display.flip()

            self.clock.tick(FPS)

        pygame.quit()

    def menu_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.KEYDOWN:
                action = self.menu.handle_input(event)
                if action == "Start Game":
                    self.playing = True
                elif action == "Quit":
                    self.running = False

    def events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_s:
                    save_game(self.player, self.terrain)
                elif event.key == pygame.K_l:
                    load_game(self.player, self.terrain)

    def update(self):
        keys = pygame.key.get_pressed()
        platforms_slopes = self.get_platforms_and_slopes()
        self.all_sprites.update(keys, platforms_slopes)
        self.camera.update(self.player)

        # Expand terrain if the player is near the edges
        player_col = self.player.rect.x // GRID_SIZE
        if player_col > self.cols - 10:
            expand_terrain(self.terrain, self.rows, 0, 20)  # Expand right
            self.cols += 20
        elif player_col < 10:
            expand_terrain(self.terrain, self.rows, 20, 0)  # Expand left
            self.cols += 20
            self.player.rect.x += 200  # Adjust player's position to account for the shift

    def get_platforms_and_slopes(self):
        platforms = []
        slopes = []
        start_col = max(0, self.camera.camera_x // GRID_SIZE)
        end_col = min(self.cols, (self.camera.camera_x + SCREEN_WIDTH) // GRID_SIZE + 1)
        start_row = max(0, self.camera.camera_y // GRID_SIZE)
        end_row = min(self.rows, (self.camera.camera_y + SCREEN_HEIGHT) // GRID_SIZE + 1)
        for row in range(start_row, end_row):
            for col in range(start_col, end_col):
                if self.terrain[row][col] == 1:
                    platforms.append(pygame.Rect(col * GRID_SIZE, row * GRID_SIZE, GRID_SIZE, GRID_SIZE))
                # Check for slopes
                if col < self.cols - 1:
                    if self.terrain[row][col] == 1 and self.terrain[row][col + 1] == 0:
                        slopes.append(pygame.Rect(col * GRID_SIZE, row * GRID_SIZE, GRID_SIZE, GRID_SIZE))
                    elif self.terrain[row][col] == 0 and self.terrain[row][col + 1] == 1:
                        slopes.append(pygame.Rect((col + 1) * GRID_SIZE, row * GRID_SIZE, GRID_SIZE, GRID_SIZE))
        return platforms, slopes

    def draw(self):
        self.screen.fill(BLACK)
        draw_terrain(self.screen, self.terrain, self.camera.camera_x, self.camera.camera_y)
        for entity in self.all_sprites:
            self.screen.blit(entity.image, self.camera.apply(entity))

        # Render HUD elements
        self.hud.draw_fps(self.screen, self.clock)

        pygame.display.flip()