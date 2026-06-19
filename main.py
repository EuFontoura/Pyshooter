import pygame 
from player import Player
from enemy import Enemy
from ui import UI
from level import Level

pygame.init()
screen = pygame.display.set_mode((1280, 720))
clock = pygame.time.Clock()
pygame.mouse.set_visible(False)


level = Level("assets/maps/fase1_collision.png")

player = Player(*level.player_spawn)
enemies = []

for x, y in level.enemy_spawns:
    enemies.append(
        Enemy(x, y)
    )
ui = UI()
projectiles = []

running = True
dt = 0

player_pos = pygame.Vector2(screen.get_width() / 2, screen.get_height() / 2)

crosshair = pygame.image.load(
    "assets/ui/aim.png"
).convert_alpha()

dead_body_image = pygame.image.load(
    "assets/ui/dead_body.png"
).convert_alpha()

die_sound = pygame.mixer.Sound(
    "assets/sounds/die.mp3"
)

dead_bodies = []

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    if player.health > 0:
        bullet = player.update(level.walls)
        if bullet:
            projectiles.append(bullet)

    for enemy in enemies:

        if enemy.health <= 0:
            continue

        enemy_bullet = enemy.update(player)

        if enemy_bullet:
            projectiles.append(enemy_bullet)

    level.draw(screen)

    # Render dead bodies first (behind active entities)
    for body in dead_bodies:
        rotated_dead_body = pygame.transform.rotate(dead_body_image, -body['angle'] - 120)
        rect = rotated_dead_body.get_rect(center=(body['x'], body['y']))
        screen.blit(rotated_dead_body, rect)

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
            continue

        for wall in level.walls:

            if projectile.rect.colliderect(wall):

                if projectile in projectiles:
                    projectiles.remove(projectile)

                break

        if projectile not in projectiles:
            continue

        # Collision detection
        if projectile.owner == "player":

            hit_enemy = False

            for enemy in enemies:

                if enemy.health <= 0:
                    continue

                if projectile.rect.colliderect(
                    enemy.get_rect()
                ):

                    enemy.take_damage(20)

                    if projectile in projectiles:
                        projectiles.remove(projectile)

                    if enemy.health <= 0:

                        die_sound.play()

                        enemy.weapon.reload_sound.stop()

                        dead_bodies.append({
                            'x': enemy.x,
                            'y': enemy.y,
                            'angle': enemy.angle
                        })

                    hit_enemy = True
                    break

            if hit_enemy:
                continue

        elif projectile.owner == "enemy" and player.health > 0:

            if projectile.rect.colliderect(
                player.get_rect()
            ):

                player.take_damage(20)

                if projectile in projectiles:
                    projectiles.remove(projectile)

                if player.health <= 0:

                    die_sound.play()

                    player.weapon.reload_sound.stop()

                    dead_bodies.append({
                        'x': player.x,
                        'y': player.y,
                        'angle': player.angle
                    })

    if player.health > 0:
        player.draw(screen)
    for enemy in enemies:

        if enemy.health > 0:
            enemy.draw(screen)

    for projectile in projectiles:
        projectile.draw(screen)
    ui.draw(screen, player)

    mouse_x, mouse_y = pygame.mouse.get_pos()

    crosshair_rect = crosshair.get_rect(
        center=(mouse_x, mouse_y - 15)
    )

    screen.blit(
        crosshair,
        crosshair_rect
    )

    alive_enemies = sum(
    1
    for enemy in enemies
    if enemy.health > 0
)
    print(alive_enemies)
    pygame.display.flip()

    dt = clock.tick(60) / 1000

pygame.quit()