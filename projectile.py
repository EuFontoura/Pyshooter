import pygame
import math

class Projectile:

    def __init__(self, x, y, angle, speed):

        self.x = x
        self.y = y

        self.speed = speed
        self.angle = angle

        radians = math.radians(angle)

        self.vx = math.cos(radians) * self.speed
        self.vy = math.sin(radians) * self.speed

        self.base_image = pygame.Surface((12, 4), pygame.SRCALPHA)
        self.base_image.fill((255, 220, 0))

        self.rect = self.base_image.get_rect(center=(x, y))

    def update(self):

        self.x += self.vx
        self.y += self.vy

        self.rect.center = (self.x, self.y)

    def draw(self, screen):

        # rotaciona de acordo com o ângulo do movimento
        rotated_image = pygame.transform.rotate(
            self.base_image,
            -self.angle
        )

        rect = rotated_image.get_rect(center=(self.x, self.y))

        screen.blit(rotated_image, rect)