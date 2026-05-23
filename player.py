import pygame
import math

pygame.init()

class Player: 
    def __init__(self):
        
        self.body = pygame.image.load("assets/characters/player/player_body.png").convert_alpha()

        self.head = pygame.image.load("assets/characters/player/player_head.png").convert_alpha()

        self.left_hand = pygame.image.load("assets/characters/player/player_left.png").convert_alpha()

        self.right_hand = pygame.image.load("assets/characters/player/player_right.png").convert_alpha()

        self.x = 400
        self.y = 300

    def update(self):

        keys = pygame.key.get_pressed()

        if keys[pygame.K_w]:
                self.y -= 5

        if keys[pygame.K_s]:
                self.y += 5

        if keys[pygame.K_a]:
                self.x -= 5

        if keys[pygame.K_d]:
                self.x += 5

        mouse_x, mouse_y = pygame.mouse.get_pos()

        dx = mouse_x - self.x
        dy = mouse_y - self.y

        self.angle = math.degrees(
            math.atan2(dy, dx)
        )

    def draw(self, screen):

        # tamanho da área do personagem
        canvas_size = 100

        player_surface = pygame.Surface(
            (canvas_size, canvas_size),
            pygame.SRCALPHA
        )

        center_x = canvas_size // 2
        center_y = canvas_size // 2

        # desenha todas as partes juntas
        player_surface.blit(
            self.body,
            (center_x - 10, center_y - 10)
        )

        player_surface.blit(
            self.head,
            (center_x - 7, center_y - 7)
        )

        player_surface.blit(
            self.left_hand,
            (center_x - 12, center_y - 20)
        )

        player_surface.blit(
            self.right_hand,
            (center_x + 6, center_y - 5)
        )

        # gira o personagem inteiro
        rotated_player = pygame.transform.rotate(
            player_surface,
            -self.angle - 120
        )

        rect = rotated_player.get_rect(
            center=(self.x, self.y)
        )

        screen.blit(rotated_player, rect)