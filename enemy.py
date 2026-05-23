import pygame
import math


class Enemy:

    def __init__(self, x, y):

        self.body = pygame.image.load(
            "assets/characters/enemy/enemy_body.png"
        ).convert_alpha()

        self.head = pygame.image.load(
            "assets/characters/enemy/enemy_head.png"
        ).convert_alpha()

        self.left_hand = pygame.image.load(
            "assets/characters/enemy/enemy_left.png"
        ).convert_alpha()

        self.right_hand = pygame.image.load(
            "assets/characters/enemy/enemy_right.png"
        ).convert_alpha()

        self.x = x
        self.y = y

        self.speed = 2
        self.angle = 0


    def update(self, player):

        # distância até player
        dx = player.x - self.x
        dy = player.y - self.y

        # ângulo pra olhar pro player
        self.angle = math.degrees(
            math.atan2(dy, dx)
        )

        # distância real
        distance = math.sqrt(
            dx ** 2 + dy ** 2
        )

        # evita divisão por zero
        if distance > 0:

            # normaliza vetor
            dx /= distance
            dy /= distance

            # move até player
            self.x += dx * self.speed
            self.y += dy * self.speed


    def draw(self, screen):

        canvas_size = 100

        enemy_surface = pygame.Surface(
            (canvas_size, canvas_size),
            pygame.SRCALPHA
        )

        center_x = canvas_size // 2
        center_y = canvas_size // 2

        enemy_surface.blit(
            self.body,
            (center_x - 10, center_y - 10)
        )

        enemy_surface.blit(
            self.head,
            (center_x - 7, center_y - 7)
        )

        enemy_surface.blit(
            self.left_hand,
            (center_x - 12, center_y - 20)
        )

        enemy_surface.blit(
            self.right_hand,
            (center_x + 6, center_y - 5)
        )

        rotated_enemy = pygame.transform.rotate(
            enemy_surface,
            -self.angle - 120
        )

        rect = rotated_enemy.get_rect(
            center=(self.x, self.y)
        )

        screen.blit(
            rotated_enemy,
            rect
        )