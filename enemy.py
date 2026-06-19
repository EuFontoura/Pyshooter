import pygame
import math
import heapq

from weapon import Weapon

class Enemy:
    # --- Variáveis de Classe para o Pathfinding ---
    grid_cache = None
    grid_size = 32 # Tamanho de cada "bloco" mental do inimigo

    def __init__(self, x, y):
        self.body = pygame.image.load("assets/characters/enemy/enemy_body.png").convert_alpha()
        self.head = pygame.image.load("assets/characters/enemy/enemy_head.png").convert_alpha()
        self.left_hand = pygame.image.load("assets/characters/enemy/enemy_left.png").convert_alpha()
        self.right_hand = pygame.image.load("assets/characters/enemy/enemy_right.png").convert_alpha()

        self.x = x
        self.y = y

        self.speed = 2
        self.angle = 0

        self.alerted = False

        self.vision_distance = 700 
        self.fov = 160 

        self.weapon = Weapon()

        self.max_health = 100
        self.health = self.max_health
        self.small_font = pygame.font.SysFont("arial", 12, bold=True)

        # --- Variáveis do Pathfinding ---
        self.path = []
        self.last_path_time = 0

    def update(self, player, walls):
            dx = player.x - self.x
            dy = player.y - self.y
            distance = math.sqrt(dx ** 2 + dy ** 2)
            can_see = self.can_see_player(player, walls)

            if not self.alerted and can_see:
                self.alerted = True

            bullet = None
            current_time = pygame.time.get_ticks()

            if self.alerted:
                # Só atualiza a rota complexa a cada 500ms
                if current_time - self.last_path_time > 500:
                    self.path = self.find_path(player.x, player.y, walls)
                    self.last_path_time = current_time

                # Se temos um caminho, vamos seguir o primeiro ponto (waypoint)
                if self.path and distance > 100:
                    target_x, target_y = self.path[0]
                    dir_x = target_x - self.x
                    dir_y = target_y - self.y
                    dist_to_node = math.sqrt(dir_x**2 + dir_y**2)

                    # Se chegou muito perto do waypoint atual, descarta ele para focar no próximo
                    if dist_to_node < self.speed * 2:
                        self.path.pop(0)
                    elif dist_to_node > 0:
                        dir_x /= dist_to_node
                        dir_y /= dist_to_node

                        # Aplica movimento com colisão física por segurança
                        old_x = self.x
                        self.x += dir_x * self.speed
                        for wall in walls:
                            if self.get_rect().colliderect(wall):
                                self.x = old_x
                                break

                        old_y = self.y
                        self.y += dir_y * self.speed
                        for wall in walls:
                            if self.get_rect().colliderect(wall):
                                self.y = old_y
                                break

                # Direcionamento da visão do inimigo
                if can_see:
                    # Se vê o jogador, mira diretamente nele
                    self.angle = math.degrees(math.atan2(dy, dx))
                elif self.path:
                    # Se não vê, olha para onde está andando
                    target_x, target_y = self.path[0]
                    self.angle = math.degrees(math.atan2(target_y - self.y, target_x - self.x))

                # Disparo
                self.weapon.update(self.x, self.y, player.x, player.y - 15)

                if can_see and distance < 350:
                    bullet = self.weapon.shoot(self.x, self.y, "enemy")

            return bullet

    def can_see_player(self, player, walls):
        dx = player.x - self.x
        dy = player.y - self.y

        distance = math.sqrt(dx ** 2 + dy ** 2)

        if distance > self.vision_distance:
            return False

        angle_to_player = math.degrees(math.atan2(dy, dx))

        angle_difference = angle_to_player - self.angle
        angle_difference = (angle_difference + 180) % 360 - 180

        if abs(angle_difference) > (self.fov / 2):
            return False

        for wall in walls:
            if wall.clipline(self.x, self.y, player.x, player.y):
                return False 

        return True

    def get_rect(self):
        return pygame.Rect(self.x - 20, self.y - 20, 40, 40)

    def take_damage(self, amount):
        self.health = max(0, self.health - amount)

    def find_path(self, target_x, target_y, walls):
        # 1. Gera o mapa mental de obstáculos apenas uma vez para todos os inimigos
        if Enemy.grid_cache is None:
            Enemy.grid_cache = set()
            for x in range(0, 1280, Enemy.grid_size):
                for y in range(0, 720, Enemy.grid_size):
                    # Usamos inflate(16, 16) para engordar virtualmente a parede 
                    # e impedir que o inimigo raspe os ombros nas quinas
                    rect = pygame.Rect(x, y, Enemy.grid_size, Enemy.grid_size).inflate(16, 16)
                    if rect.collidelist(walls) != -1:
                        Enemy.grid_cache.add((x // Enemy.grid_size, y // Enemy.grid_size))

        # 2. Converte as coordenadas reais para a grade
        start_node = (int(self.x // Enemy.grid_size), int(self.y // Enemy.grid_size))
        end_node = (int(target_x // Enemy.grid_size), int(target_y // Enemy.grid_size))

        if start_node == end_node:
            return []

        open_set = []
        heapq.heappush(open_set, (0, start_node))
        came_from = {}
        g_score = {start_node: 0}

        # 3. Inicia a busca A*
        while open_set:
            _, current = heapq.heappop(open_set)

            if current == end_node:
                path = []
                while current in came_from:
                    # Converte o nó da grade de volta para o meio do pixel real na tela
                    path.append((
                        current[0] * Enemy.grid_size + Enemy.grid_size // 2,
                        current[1] * Enemy.grid_size + Enemy.grid_size // 2
                    ))
                    current = came_from[current]
                path.reverse()
                return path

            # Checa os 8 vizinhos (cima, baixo, lados e diagonais)
            for dx, dy in [(0, -1), (0, 1), (-1, 0), (1, 0), (-1, -1), (-1, 1), (1, -1), (1, 1)]:
                neighbor = (current[0] + dx, current[1] + dy)

                # Evita sair da tela
                if not (0 <= neighbor[0] < 1280 // Enemy.grid_size and 0 <= neighbor[1] < 720 // Enemy.grid_size):
                    continue

                # Ignora se for parede
                if neighbor in Enemy.grid_cache:
                    continue

                # Peso do movimento (diagonal custa um pouco mais, ~1.4)
                tentative_g = g_score[current] + (1.414 if dx != 0 and dy != 0 else 1)

                if neighbor not in g_score or tentative_g < g_score[neighbor]:
                    came_from[neighbor] = current
                    g_score[neighbor] = tentative_g
                    # Heurística de distância até o alvo
                    f_score = tentative_g + (abs(neighbor[0] - end_node[0]) + abs(neighbor[1] - end_node[1]))
                    heapq.heappush(open_set, (f_score, neighbor))

        return []

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