import pygame
import math
import heapq

from weapon import Weapon

# Para a IA do inimigo, usei o algoritmo A* para encontrar o caminho mais curto até o jogador, considerando as paredes como obstáculos.
# Por ser um algoritmo relativamente pesado e complexo, optei por comentar grandemente essa parte do código

class Enemy:
    grid_cache = None # variavel para guardar onde tem parede no mapa, para otimizar o pathfinding
    grid_size = 32 # tamanho da grade 

    def __init__(self, x, y):
        # carregamento das imagens
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
        self.fov = 160 # a visão periferica dele é de 160 graus (80 pra cada lado)

        self.weapon = Weapon()

        self.max_health = 100
        self.health = self.max_health
        self.small_font = pygame.font.SysFont("arial", 12, bold=True)

        self.path = [] # caminho atual para o jogador
        self.last_path_time = 0 # relogio para controlar a frequência de recalculo do caminho até o jogador

    def update(self, player, walls):
            # Calculo de distancia entre o inimigo e o player
            dx = player.x - self.x
            dy = player.y - self.y
            # Distancia euclidiana
            distance = math.sqrt(dx ** 2 + dy ** 2)
            # Checa se o inimigo pode ver o jogador (dentro do campo de visão, distância e sem paredes no caminho)
            can_see = self.can_see_player(player, walls)

            if not self.alerted and can_see:
                self.alerted = True

            bullet = None
            current_time = pygame.time.get_ticks()
        # Se o inimigo estiver alertado, ele tenta se mover em direção ao jogador usando o caminho calculado pelo A* e atira quando possível
            if self.alerted:
                # Recalcula o caminho para o jogador a cada meio segundo para otimizar a performance, ao invés de calcular toda frame pra não virar uma apresentação de PowerPoint
                if current_time - self.last_path_time > 500:
                    self.path = self.find_path(player.x, player.y, walls)
                    self.last_path_time = current_time

                if self.path and distance > 100:
                    target_x, target_y = self.path[0] # próximo ponto no caminho
                    dir_x = target_x - self.x
                    dir_y = target_y - self.y
                    dist_to_node = math.sqrt(dir_x**2 + dir_y**2)

                # Se estiver perto o suficiente do próximo ponto, remove ele da lista de caminho
                    if dist_to_node < self.speed * 2:
                        self.path.pop(0)
                    elif dist_to_node > 0:
                        # Normaliza a direção pra impedir o inimigo de andar mais rápido na diagonal
                        dir_x /= dist_to_node
                        dir_y /= dist_to_node

                    # Movimento com checagem de colisão com as paredes na horizontal e vertical separadamente pra evitar que o inimigo fique preso nas paredes
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

                # angulo do inimigo. Se tá vendo o player, olha pra ele, se não, olha pro próximo ponto do caminho
                if can_see:
                    self.angle = math.degrees(math.atan2(dy, dx))
                elif self.path:
                    target_x, target_y = self.path[0]
                    self.angle = math.degrees(math.atan2(target_y - self.y, target_x - self.x))

                self.weapon.update(self.x, self.y, player.x, player.y - 15)

                # se tá vendo o player e tá na distância do tiro (350 pixels), mete o pipoco
                if can_see and distance < 350:
                    bullet = self.weapon.shoot(self.x, self.y, "enemy")

            return bullet

    def can_see_player(self, player, walls):
        # mesmo calculo de distância e ângulo do update, mas aqui a função retorna apenas se o inimigo pode ver o jogador ou não, sem fazer nada além disso
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

    # função para pegar o retângulo do inimigo, usada para colisões. A tal da hitbox
    def get_rect(self):
        return pygame.Rect(self.x - 20, self.y - 20, 40, 40)

    # função para o inimigo tomar dano, subtrai a quantidade de vida do inimigo, mas não deixa ele com vida negativa, o que poderia causar bugs
    def take_damage(self, amount):
        self.health = max(0, self.health - amount)

    def find_path(self, target_x, target_y, walls):
        if Enemy.grid_cache is None:
            Enemy.grid_cache = set()
            for x in range(0, 1280, Enemy.grid_size):
                for y in range(0, 720, Enemy.grid_size):
                    # aqui a gente checa se tem parede na célula da grade, se tiver, adiciona na cache pra otimizar o pathfinding. 
                    # A função inflate é usada pra aumentar a hitbox do inimigo, pra evitar que ele tente passar por buracos muito pequenos entre as paredes
                    rect = pygame.Rect(x, y, Enemy.grid_size, Enemy.grid_size).inflate(16, 16)
                    if rect.collidelist(walls) != -1:
                        Enemy.grid_cache.add((x // Enemy.grid_size, y // Enemy.grid_size))

        start_node = (int(self.x // Enemy.grid_size), int(self.y // Enemy.grid_size))
        end_node = (int(target_x // Enemy.grid_size), int(target_y // Enemy.grid_size))

        if start_node == end_node:
            return []

        # Implementação do algoritmo A* para encontrar o caminho mais curto até o jogador, considerando as paredes como obstáculos. 
        # O algoritmo é otimizado usando uma cache para armazenar onde tem parede no mapa, e só recalcula o caminho a cada meio segundo para evitar que o jogo fique lento.

        open_set = [] # fila de prioridade para os nós a serem explorados, ordenada pelo custo total estimado (g + h)
        heapq.heappush(open_set, (0, start_node)) # adiciona o nó inicial à fila de prioridade com custo 0
        came_from = {} # dicionário para rastrear o caminho percorrido, mapeando cada nó para o nó anterior no caminho
        g_score = {start_node: 0} # dicionário para armazenar o custo real do caminho do nó inicial até cada nó, começando com 0 para o nó inicial


        # f_score é o custo total estimado do caminho do nó inicial até o nó final passando por um determinado nó, calculado como g_score + heurística (distância Manhattan até o destino)
        while open_set:
            _, current = heapq.heappop(open_set)

            if current == end_node:
                path = []
                while current in came_from:
                    path.append((
                        current[0] * Enemy.grid_size + Enemy.grid_size // 2,
                        current[1] * Enemy.grid_size + Enemy.grid_size // 2
                    ))
                    current = came_from[current]
                path.reverse()
                return path
            # Para cada nó vizinho (incluindo diagonais), o algoritmo verifica se ele está dentro dos limites do mapa, se não é uma parede (usando a cache), e calcula o custo tentativo de chegar até ele. Se o custo tentativo for menor do que o custo registrado para aquele nó, ou se o nó ainda não tiver um custo registrado, o nó é atualizado com o novo custo e adicionado à fila de prioridade para ser explorado. O processo continua até que o nó final seja alcançado ou que a fila de prioridade esteja vazia, indicando que não há caminho disponível.
            for dx, dy in [(0, -1), (0, 1), (-1, 0), (1, 0), (-1, -1), (-1, 1), (1, -1), (1, 1)]:
                neighbor = (current[0] + dx, current[1] + dy)

                if not (0 <= neighbor[0] < 1280 // Enemy.grid_size and 0 <= neighbor[1] < 720 // Enemy.grid_size):
                    continue

                if neighbor in Enemy.grid_cache:
                    continue

                tentative_g = g_score[current] + (1.414 if dx != 0 and dy != 0 else 1)

                if neighbor not in g_score or tentative_g < g_score[neighbor]:
                    came_from[neighbor] = current
                    g_score[neighbor] = tentative_g
                    f_score = tentative_g + (abs(neighbor[0] - end_node[0]) + abs(neighbor[1] - end_node[1]))
                    heapq.heappush(open_set, (f_score, neighbor))

        return []

# Função para desenhar o inimigo na tela, incluindo a animação de recarga da arma. A animação é feita movendo a arma e a mão direita do inimigo para baixo durante a recarga, e a mão esquerda se move para frente e para trás para simular o movimento de recarga. A barra de vida e a barra de recarga também são desenhadas acima do inimigo quando ele está ferido ou recarregando.
# Essa parte não vou comentar muito por que é mais visual.

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