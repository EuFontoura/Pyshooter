import pygame 
from player import Player

pygame.init()
screen = pygame.display.set_mode((1280, 720))
clock = pygame.time.Clock()

player = Player()

running = True
dt = 0

player_pos = pygame.Vector2(screen.get_width() / 2, screen.get_height() / 2)

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    player.update()
    screen.fill((30, 30, 30))

    player.draw(screen)

    pygame.display.flip()

    dt = clock.tick(60) / 1000

pygame.quit()