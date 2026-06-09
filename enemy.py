import pygame
import math

from weapon import Weapon

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

        self.alerted = False

        self.vision_distance = 300
        self.fov = 70

        self.weapon = Weapon()

    def update(self, player):

        dx = player.x - self.x
        dy = player.y - self.y

        distance = math.sqrt(dx ** 2 + dy ** 2)

        # detecta player pela primeira vez
        if not self.alerted:
            if self.can_see_player(player):
                self.alerted = True

        bullet = None

        if self.alerted:

            # atualiza direção do inimigo
            self.angle = math.degrees(math.atan2(dy, dx))

            # movimento em direção ao player (mantém distância mínima)
            if distance > 100 and distance > 0:
                dx /= distance
                dy /= distance
                self.x += dx * self.speed
                self.y += dy * self.speed

            # atualiza arma sempre (importante pro angle do tiro)
            self.weapon.update(
                self.x,
                self.y,
                player.x,
                player.y - 15
            )

            # atira apenas se enxergar e estiver no alcance
            if self.can_see_player(player) and distance < 250:
                bullet = self.weapon.shoot(
                    self.x,
                    self.y)

        return bullet

    def can_see_player(self, player):

        dx = player.x - self.x
        dy = player.y - self.y

        distance = math.sqrt(dx ** 2 + dy ** 2)

        if distance > self.vision_distance:
            return False

        angle_to_player = math.degrees(math.atan2(dy, dx))

        angle_difference = angle_to_player - self.angle
        angle_difference = (angle_difference + 180) % 360 - 180

        return abs(angle_difference) < (self.fov / 2)

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

        weapon_x = center_x + 7
        weapon_y = center_y - 18

        self.weapon.draw(
            enemy_surface,
            weapon_x,
            weapon_y
        )

        rotated_enemy = pygame.transform.rotate(
            enemy_surface,
            -self.angle - 120
        )

        rect = rotated_enemy.get_rect(
            center=(self.x, self.y)
        )

        screen.blit(rotated_enemy, rect)