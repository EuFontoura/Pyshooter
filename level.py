import pygame


class Level:
    TILE_SIZE = 8

    # Marcadores reservados para uso futuro:
    # Vermelho   (255, 0, 0)   -> spawn do jogador
    # Azul       (0, 0, 255)   -> spawn de inimigo
    # Amarelo    (255, 255, 0) -> saída/extração

    def __init__(self, map_path):
        self.map_path = map_path

        self.image = pygame.image.load(map_path).convert()

        self.image = pygame.transform.scale(
            self.image,
            (1280, 720)
        )
        self.rect = self.image.get_rect()

        self.player_spawn = None
        self.enemy_spawns = []
        self.exit_point = None

        self.walls = []

        self.load_markers()

        self.load_collisions()

    def draw(self, screen):
        screen.blit(self.image, (0, 0))


    def load_markers(self):

        width = self.image.get_width()
        height = self.image.get_height()

        for y in range(height):
            for x in range(width):

                color = self.image.get_at((x, y))[:3]

                if color == (255, 0, 0):

                    left_red = (
                        x > 0 and
                        self.image.get_at((x - 1, y))[:3] == (255, 0, 0)
                    )

                    top_red = (
                        y > 0 and
                        self.image.get_at((x, y - 1))[:3] == (255, 0, 0)
                    )

                    if not left_red and not top_red:
                        self.player_spawn = (x, y)

                elif color == (0, 0, 255):

                    left_blue = (
                        x > 0 and
                        self.image.get_at((x - 1, y))[:3] == (0, 0, 255)
                    )

                    top_blue = (
                        y > 0 and
                        self.image.get_at((x, y - 1))[:3] == (0, 0, 255)
                    )

                    if not left_blue and not top_blue:
                        self.enemy_spawns.append((x, y))

                elif color == (255, 255, 0):

                    left_yellow = (
                        x > 0 and
                        self.image.get_at((x - 1, y))[:3] == (255, 255, 0)
                    )

                    top_yellow = (
                        y > 0 and
                        self.image.get_at((x, y - 1))[:3] == (255, 255, 0)
                    )

                    if not left_yellow and not top_yellow:
                        self.exit_point = (x, y)

    def load_collisions(self):

        width = self.image.get_width()
        height = self.image.get_height()

        for y in range(0, height, self.TILE_SIZE):
            for x in range(0, width, self.TILE_SIZE):

                has_collision = False

                for py in range(
                    y,
                    min(y + self.TILE_SIZE, height)
                ):
                    for px in range(
                        x,
                        min(x + self.TILE_SIZE, width)
                    ):

                        color = self.image.get_at(
                            (px, py)
                        )[:3]

                        if color == (234, 54, 128):
                            has_collision = True
                            break

                    if has_collision:
                        break

                if has_collision:
                    self.walls.append(
                        pygame.Rect(
                            x,
                            y,
                            self.TILE_SIZE,
                            self.TILE_SIZE
                        )
                    )

            self.walls.append(
            pygame.Rect(-10, 0, 10, height)
        )

        self.walls.append(
            pygame.Rect(width, 0, 10, height)
        )

        self.walls.append(
            pygame.Rect(0, -10, width, 10)
        )

        self.walls.append(
            pygame.Rect(0, height, width, 10)
        )