import pygame
from src.settings import SCREEN_WIDTH, SCREEN_HEIGHT, PLAYER_JUMP, GRAVITY, ACCELERATION, MAX_SPEED, SPRINT_ACCELERATION, SPRINT_MAX_SPEED, GROUND_FRICTION, AIR_FRICTION, GRID_SIZE

class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.width = 30
        self.height = 60
        self.image = pygame.Surface((self.width, self.height))  # Rectangular shape
        self.image.fill((255, 0, 0))  # Fill with red color
        self.rect = self.image.get_rect()
        self.rect.center = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)
        self.vel_x = 0
        self.vel_y = 0
        self.on_ground = False

    def update(self, keys, platforms_slopes):
        platforms, slopes = platforms_slopes
        self.handle_input(keys)
        self.apply_gravity()
        self.apply_friction()
        self.move_and_collide(platforms, slopes)

    def apply_gravity(self):
        if not self.on_ground:
            self.vel_y += GRAVITY

    def handle_input(self, keys):
        is_sprinting = keys[pygame.K_LSHIFT] or keys[pygame.K_RSHIFT]
        acceleration = SPRINT_ACCELERATION if is_sprinting else ACCELERATION
        max_speed = SPRINT_MAX_SPEED if is_sprinting else MAX_SPEED

        if keys[pygame.K_LEFT]:
            self.vel_x -= acceleration
        elif keys[pygame.K_RIGHT]:
            self.vel_x += acceleration
        else:
            self.vel_x *= AIR_FRICTION if not self.on_ground else GROUND_FRICTION  # Apply friction based on ground state

        if keys[pygame.K_UP] and self.on_ground:
            self.vel_y = -PLAYER_JUMP
            self.on_ground = False

        # Limit speed
        self.vel_x = max(-max_speed, min(max_speed, self.vel_x))

    def apply_friction(self):
        if self.on_ground:
            self.vel_x *= GROUND_FRICTION
        else:
            self.vel_x *= AIR_FRICTION

    def move_and_collide(self, platforms, slopes):
        # Check for horizontal collisions
        self.rect.x += self.vel_x
        self.handle_horizontal_collisions(platforms, slopes)

        # Check for vertical collisions
        self.rect.y += self.vel_y
        self.handle_vertical_collisions(platforms, slopes)

    def handle_horizontal_collisions(self, platforms, slopes):
        collisions = self.get_collisions(platforms)
        for platform in collisions:
            if self.vel_x > 0:  # Moving right
                self.rect.right = platform.left
            elif self.vel_x < 0:  # Moving left
                self.rect.left = platform.right
            self.vel_x = 0

    def handle_vertical_collisions(self, platforms, slopes):
        self.on_ground = False
        collisions = self.get_collisions(platforms)
        for platform in collisions:
            if self.vel_y > 0:  # Falling
                self.rect.bottom = platform.top
                self.vel_y = 0
                self.on_ground = True
            elif self.vel_y < 0:  # Jumping
                self.rect.top = platform.bottom
                self.vel_y = 0

        # Handle slope collisions
        slope_collisions = self.get_collisions(slopes)
        for slope in slope_collisions:
            if self.vel_y > 0:  # Falling
                self.rect.bottom = slope.top
                self.vel_y = 0
                self.on_ground = True
            elif self.vel_y < 0:  # Jumping
                self.rect.top = slope.bottom
                self.vel_y = 0

    def get_collisions(self, platforms):
        return [platform for platform in platforms if self.rect.colliderect(platform)]