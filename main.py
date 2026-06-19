import pygame 
import sys
from player import Player
from enemy import Enemy
from ui import UI
from level import Level

pygame.init()
screen = pygame.display.set_mode((1280, 720))
clock = pygame.time.Clock()
pygame.mouse.set_visible(False)

# Carrega a imagem de vitória
win_menu_image = pygame.image.load("assets/ui/win_menu.png").convert_alpha()
win_menu_rect = win_menu_image.get_rect(center=(1280 // 2, 720 // 2))

# =========================================================================
# AJUSTE AQUI: Altere os números abaixo para mover a caixa vermelha na tela
# Parâmetros: Rect( X,  Y, Largura, Altura)
# =========================================================================
ok_button_rect = pygame.Rect(540, 360, 200, 60) 

def reset_game():
    """Função auxiliar para reiniciar todas as variáveis do jogo"""
    global level, player, enemies, impacts, projectiles, dead_bodies, game_won
    level = Level("assets/maps/fase1_collision.png")
    player = Player(*level.player_spawn)
    enemies = []
    impacts = []
    projectiles = []
    dead_bodies = []
    game_won = False
    
    for x, y in level.enemy_spawns:
        enemies.append(Enemy(x, y))

# Inicializa o jogo pela primeira vez
level = Level("assets/maps/fase1_collision.png")
player = Player(*level.player_spawn)
enemies = []
impacts = []

for x, y in level.enemy_spawns:
    enemies.append(Enemy(x, y))

ui = UI()
projectiles = []

running = True
game_won = False 
dt = 0

crosshair = pygame.image.load("assets/ui/aim.png").convert_alpha()
dead_body_image = pygame.image.load("assets/ui/dead_body.png").convert_alpha()
die_sound = pygame.mixer.Sound("assets/sounds/die.mp3")
fire_impact_image = pygame.image.load("assets/gun/fire/730.png").convert_alpha()
dead_bodies = []

while running:
    mouse_x, mouse_y = pygame.mouse.get_pos()
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            
        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if game_won:
                if ok_button_rect.collidepoint(mouse_x, mouse_y):
                    reset_game()

    if game_won:
        pygame.mouse.set_visible(True) # Mostra a seta do mouse padrão do Windows
        
        # Desenha o fundo estático
        level.draw(screen)
        for body in dead_bodies:
            rotated_dead_body = pygame.transform.rotate(dead_body_image, -body['angle'] - 120)
            rect = rotated_dead_body.get_rect(center=(body['x'], body['y']))
            screen.blit(rotated_dead_body, rect)
        for enemy in enemies:
            if enemy.health > 0: enemy.draw(screen)
        if player.health > 0: player.draw(screen)
        
        # Desenha a imagem de vitória
        screen.blit(win_menu_image, win_menu_rect)

        pygame.display.flip()
        clock.tick(60)
        continue

    # --- GAMEPLAY EM EXECUÇÃO ---
    pygame.mouse.set_visible(False)

    if player.health > 0:
        bullet = player.update(level.walls)
        if bullet:
            projectiles.append(bullet)

    for enemy in enemies:
        if enemy.health <= 0:
            continue
        enemy_bullet = enemy.update(player, level.walls)
        if enemy_bullet:
            projectiles.append(enemy_bullet)

    level.draw(screen)
    
    current_time = pygame.time.get_ticks()

    for impact in impacts[:]:
        age = current_time - impact["created"]
        if age > 150:
            impacts.remove(impact)
            continue
        fire_rect = fire_impact_image.get_rect(center=(int(impact["x"]), int(impact["y"])))
        screen.blit(fire_impact_image, fire_rect)

    for body in dead_bodies:
        rotated_dead_body = pygame.transform.rotate(dead_body_image, -body['angle'] - 120)
        rect = rotated_dead_body.get_rect(center=(body['x'], body['y']))
        screen.blit(rotated_dead_body, rect)

    for projectile in projectiles:
        projectile.update()

    for projectile in projectiles[:]:
        if (projectile.x < 0 or projectile.x > screen.get_width() or 
            projectile.y < 0 or projectile.y > screen.get_height()):
            projectiles.remove(projectile)
            continue

        for wall in level.walls:
            if projectile.rect.colliderect(wall):
                impacts.append({
                    "x": projectile.x,
                    "y": projectile.y,
                    "created": pygame.time.get_ticks()
                })
                if projectile in projectiles:
                    projectiles.remove(projectile)
                break

        if projectile not in projectiles:
            continue

        if projectile.owner == "player":
            hit_enemy = False
            for enemy in enemies:
                if enemy.health <= 0:
                    continue

                if projectile.rect.colliderect(enemy.get_rect()):
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
            if projectile.rect.colliderect(player.get_rect()):
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

    crosshair_rect = crosshair.get_rect(center=(mouse_x, mouse_y - 15))
    screen.blit(crosshair, crosshair_rect)

    alive_enemies = sum(1 for enemy in enemies if enemy.health > 0)

    # Condição de vitória
    if alive_enemies == 0 and level.exit_point is not None:
        if player.get_rect().colliderect(level.exit_point):
            game_won = True

    pygame.display.flip()
    dt = clock.tick(60) / 1000

pygame.quit()