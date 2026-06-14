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

        self.max_health = 100
        self.health = self.max_health
        self.small_font = pygame.font.SysFont("arial", 12, bold=True)

    def update(self, player):

        dx = player.x - self.x
        dy = player.y - self.y

        distance = math.sqrt(dx ** 2 + dy ** 2)

        if not self.alerted:
            if self.can_see_player(player):
                self.alerted = True

        bullet = None

        if self.alerted:

            self.angle = math.degrees(math.atan2(dy, dx))

            if distance > 100 and distance > 0:
                dx /= distance
                dy /= distance
                self.x += dx * self.speed
                self.y += dy * self.speed

            self.weapon.update(
                self.x,
                self.y,
                player.x,
                player.y - 15
            )

            if self.can_see_player(player) and distance < 250:
                bullet = self.weapon.shoot(
                    self.x,
                    self.y,
                    "enemy"
                )

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

    def get_rect(self):
        return pygame.Rect(self.x - 20, self.y - 20, 40, 40)

    def take_damage(self, amount):
        self.health = max(0, self.health - amount)

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

        left_hand_x = center_x - 12
        left_hand_y = center_y - 20
        right_hand_x = center_x + 6
        right_hand_y = center_y - 5
        weapon_x = center_x + 7
        weapon_y = center_y - 18

        # Reload animation offsets
        if self.weapon.is_reloading:
            current_time = pygame.time.get_ticks()
            elapsed = current_time - self.weapon.reload_start
            progress = min(1.0, elapsed / self.weapon.reload_time)

            if progress < 0.2:
                w_offset = (progress / 0.2) * 6
            elif progress > 0.8:
                w_offset = ((1.0 - progress) / 0.2) * 6
            else:
                w_offset = 6

            weapon_y += w_offset
            weapon_x -= w_offset / 2
            right_hand_y += w_offset
            right_hand_x -= w_offset / 2

            if progress < 0.5:
                t = progress / 0.5
                left_hand_x = int((center_x - 12) * (1 - t) + (center_x - 2) * t)
                left_hand_y = int((center_y - 20) * (1 - t) + (center_y - 5) * t)
            else:
                t = (progress - 0.5) / 0.5
                left_hand_x = int((center_x - 2) * (1 - t) + (center_x - 12) * t)
                left_hand_y = int((center_y - 5) * (1 - t) + (center_y - 20) * t)

        enemy_surface.blit(
            self.left_hand,
            (left_hand_x, left_hand_y)
        )

        enemy_surface.blit(
            self.right_hand,
            (right_hand_x, right_hand_y)
        )

        self.weapon.draw(
            enemy_surface,
            weapon_x,
            weapon_y
        )
        
        enemy_surface.blit(
            self.head,
            (center_x - 7, center_y - 7)
        )

        rotated_enemy = pygame.transform.rotate(
            enemy_surface,
            -self.angle - 120
        )

        rect = rotated_enemy.get_rect(
            center=(self.x, self.y)
        )

        screen.blit(rotated_enemy, rect)

        if self.health < self.max_health and self.health > 0:
            bar_width = 40
            bar_height = 5
            bar_x = self.x - bar_width // 2
            bar_y = self.y - 45

            pygame.draw.rect(screen, (40, 40, 40), (bar_x, bar_y, bar_width, bar_height))

            ratio = self.health / self.max_health
            fill_width = int(bar_width * ratio)

            r = int(255 * (1 - ratio))
            g = int(255 * ratio)
            b = 0
            color = (r, g, b)

            pygame.draw.rect(screen, color, (bar_x, bar_y, fill_width, bar_height))

            pygame.draw.rect(screen, (0, 0, 0), (bar_x - 1, bar_y - 1, bar_width + 2, bar_height + 2), 1)

        if self.weapon.is_reloading and self.health > 0:
            current_time = pygame.time.get_ticks()
            elapsed = current_time - self.weapon.reload_start
            progress = min(1.0, elapsed / self.weapon.reload_time)
            remaining_ratio = 1.0 - progress

            bar_width = 40
            bar_height = 5
            bar_x = self.x - bar_width // 2

            if self.health < self.max_health:
                bar_y = self.y - 55
            else:
                bar_y = self.y - 45

            pygame.draw.rect(screen, (40, 40, 40), (bar_x, bar_y, bar_width, bar_height))

            fill_width = int(bar_width * remaining_ratio)

            pygame.draw.rect(screen, (150, 150, 150), (bar_x, bar_y, fill_width, bar_height))

            pygame.draw.rect(screen, (0, 0, 0), (bar_x - 1, bar_y - 1, bar_width + 2, bar_height + 2), 1)

            reload_text = self.small_font.render("reloading", True, (200, 200, 200))
            text_rect = reload_text.get_rect(center=(self.x, bar_y - 10))
            screen.blit(reload_text, text_rect)