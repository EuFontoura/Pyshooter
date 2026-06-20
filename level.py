import pygame

class Level:
    TILE_SIZE = 8

    def __init__(self, visual_map_path, collision_map_path):
        # 1. Imagem visual (o que o jogador vê na tela)
        self.image = pygame.image.load(visual_map_path).convert()
        self.image = pygame.transform.scale(self.image, (1280, 720))

        # 2. Imagem de dados invisível (onde lemos os blocos rosa, vermelho, etc.)
        self.collision_image = pygame.image.load(collision_map_path).convert()
        self.collision_image = pygame.transform.scale(self.collision_image, (1280, 720))

        self.rect = self.image.get_rect()

        self.player_spawn = None
        self.enemy_spawns = []
        self.exit_point = None

        self.walls = []

        self.load_markers()
        self.load_collisions()

    def draw(self, screen):
        # O jogo sempre desenha a arte limpa da fase
        screen.blit(self.image, (0, 0))

    def load_markers(self):
        # Lemos a largura e altura da imagem de colisão
        width = self.collision_image.get_width()
        height = self.collision_image.get_height()

        for y in range(height):
            for x in range(width):
                # Extrai a cor da imagem invisível de colisões!
                color = self.collision_image.get_at((x, y))[:3]

                # Spawn Player (Vermelho)
                if color == (255, 0, 0):
                    left_red = (
                        x > 0 and
                        self.collision_image.get_at((x - 1, y))[:3] == (255, 0, 0)
                    )
                    top_red = (
                        y > 0 and
                        self.collision_image.get_at((x, y - 1))[:3] == (255, 0, 0)
                    )
                    if not left_red and not top_red:
                        self.player_spawn = (x, y)

                # Spawn Inimigo (Azul)
                elif color == (0, 0, 255):
                    left_blue = (
                        x > 0 and
                        self.collision_image.get_at((x - 1, y))[:3] == (0, 0, 255)
                    )
                    top_blue = (
                        y > 0 and
                        self.collision_image.get_at((x, y - 1))[:3] == (0, 0, 255)
                    )
                    if not left_blue and not top_blue:
                        self.enemy_spawns.append((x, y))

                # Zona de Extração (Amarelo)
                elif color == (255, 255, 0):
                    # Salva uma área centralizada de 30x30 pixels baseada nesse ponto
                    if self.exit_point is None:
                        self.exit_point = pygame.Rect(x - 15, y - 15, 30, 30)


    def load_collisions(self):
        width = self.collision_image.get_width()
        height = self.collision_image.get_height()

        for y in range(0, height, self.TILE_SIZE):
            for x in range(0, width, self.TILE_SIZE):
                has_collision = False

                for py in range(y, min(y + self.TILE_SIZE, height)):
                    for px in range(x, min(x + self.TILE_SIZE, width)):
                        
                        # Verifica o Rosa (234, 54, 128) na imagem invisível
                        color = self.collision_image.get_at((px, py))[:3]

                        if color == (234, 54, 128):
                            has_collision = True
                            break

                    if has_collision:
                        break

                if has_collision:
                    self.walls.append(
                        pygame.Rect(x, y, self.TILE_SIZE, self.TILE_SIZE)
                    )

        # Bordas da tela
        self.walls.append(pygame.Rect(-10, 0, 10, height))
        self.walls.append(pygame.Rect(width, 0, 10, height))
        self.walls.append(pygame.Rect(0, -10, width, 10))
        self.walls.append(pygame.Rect(0, height, width, 10))