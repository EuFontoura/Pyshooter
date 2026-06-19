import pygame
import math

from weapon import Weapon

pygame.init()

class Player: 
    def __init__(self, x=400, y=300):
        
        self.body = pygame.image.load("assets/characters/player/player_body.png").convert_alpha()

        self.head = pygame.image.load("assets/characters/player/player_head.png").convert_alpha()

        self.left_hand = pygame.image.load("assets/characters/player/player_left.png").convert_alpha()

        self.right_hand = pygame.image.load("assets/characters/player/player_right.png").convert_alpha()

        self.x = x
        self.y = y
        
        self.weapon = Weapon()
        
        self.max_health = 100
        self.health = self.max_health

        self.max_shield = 100
        self.shield = self.max_shield
        self.angle = 0
        self.small_font = pygame.font.SysFont("arial", 12, bold=True)

    def update(self, walls):

        keys = pygame.key.get_pressed()

        speed = 5

        old_x = self.x

        if keys[pygame.K_a]:
            self.x -= speed

        if keys[pygame.K_d]:
            self.x += speed

        for wall in walls:
            if self.get_rect().colliderect(wall):
                self.x = old_x
                break


        old_y = self.y

        if keys[pygame.K_w]:
            self.y -= speed

        if keys[pygame.K_s]:
            self.y += speed

        for wall in walls:
            if self.get_rect().colliderect(wall):
                self.y = old_y
                break

        if keys[pygame.K_r]:
            self.weapon.start_reload()

        mouse_x, mouse_y = pygame.mouse.get_pos()

        dx = mouse_x - self.x
        dy = mouse_y - self.y
        
        self.weapon.update(
            self.x,
            self.y,
            mouse_x,
            mouse_y
        )

        self.angle = math.degrees(
            math.atan2(dy, dx)
        )
        
        mouse_buttons = pygame.mouse.get_pressed()

        if mouse_buttons[0]:
            bullet = self.weapon.shoot(
                self.x, 
                self.y,
                "player"
            )
            return bullet
        return None

    def get_rect(self):
        return pygame.Rect(self.x - 20, self.y - 20, 40, 40)

    def take_damage(self, amount):
        if self.shield >= amount:
            self.shield -= amount
        else:
            amount -= self.shield
            self.shield = 0
            self.health = max(0, self.health - amount)

    def draw(self, screen):

        canvas_size = 100

        player_surface = pygame.Surface(
            (canvas_size, canvas_size),
            pygame.SRCALPHA
        )

        center_x = canvas_size // 2
        center_y = canvas_size // 2

        player_surface.blit(
            self.body,
            (center_x - 10, center_y - 10)
        )

        left_hand_x = center_x - 12
        left_hand_y = center_y - 20
        right_hand_x = center_x + 6
        right_hand_y = center_y - 5
        weapon_x = center_x + 7
        weapon_y = center_y - 18

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

        player_surface.blit(
            self.left_hand,
            (left_hand_x, left_hand_y)
        )

        player_surface.blit(
            self.right_hand,
            (right_hand_x, right_hand_y)
        )
        
        self.weapon.draw(
            player_surface,
            weapon_x,
            weapon_y
        )

        player_surface.blit(
            self.head,
            (center_x - 7, center_y - 7)
        )

        rotated_player = pygame.transform.rotate(
            player_surface,
            -self.angle - 120
        )

        rect = rotated_player.get_rect(
            center=(self.x, self.y)
        )

        screen.blit(rotated_player, rect)

        if self.weapon.is_reloading:
            current_time = pygame.time.get_ticks()
            elapsed = current_time - self.weapon.reload_start
            progress = min(1.0, elapsed / self.weapon.reload_time)
            remaining_ratio = 1.0 - progress

            bar_width = 40
            bar_height = 5
            bar_x = self.x - bar_width // 2
            bar_y = self.y - 45

            pygame.draw.rect(screen, (40, 40, 40), (bar_x, bar_y, bar_width, bar_height))

            fill_width = int(bar_width * remaining_ratio)

            pygame.draw.rect(screen, (150, 150, 150), (bar_x, bar_y, fill_width, bar_height))

            pygame.draw.rect(screen, (0, 0, 0), (bar_x - 1, bar_y - 1, bar_width + 2, bar_height + 2), 1)

            reload_text = self.small_font.render("reloading", True, (200, 200, 200))
            text_rect = reload_text.get_rect(center=(self.x, bar_y - 10))
            screen.blit(reload_text, text_rect)