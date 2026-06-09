import pygame 
from player import Player
from enemy import Enemy
from ui import UI

pygame.init()
screen = pygame.display.set_mode((1280, 720))
clock = pygame.time.Clock()
pygame.mouse.set_visible(False)


player = Player()
enemy = Enemy(100, 100)
ui = UI()
projectiles = []

running = True
dt = 0

player_pos = pygame.Vector2(screen.get_width() / 2, screen.get_height() / 2)

crosshair = pygame.image.load(
    "assets/ui/aim.png"
).convert_alpha()

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    bullet = player.update()
    if bullet:
        projectiles.append(bullet)
        
    enemy_bullet = enemy.update(player)
    if enemy_bullet:
        projectiles.append(enemy_bullet)

    enemy.update(player)

    screen.fill((30, 30, 30))

    for projectile in projectiles:
        projectile.update()

    for projectile in projectiles[:]:

        if (
            projectile.x < 0
            or projectile.x > screen.get_width()
            or projectile.y < 0
            or projectile.y > screen.get_height()
        ):
            projectiles.remove(projectile)

    player.draw(screen)
    enemy.draw(screen)
    for projectile in projectiles:
        projectile.draw(screen)
    ui.draw(screen, player)

    mouse_x, mouse_y = pygame.mouse.get_pos()

    crosshair_rect = crosshair.get_rect(
        center=(mouse_x, mouse_y)
    )

    screen.blit(
        crosshair,
        crosshair_rect
    )

    pygame.display.flip()

    dt = clock.tick(60) / 1000

pygame.quit()