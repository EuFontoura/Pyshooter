import pygame 
import sys
from player import Player
from enemy import Enemy
from ui import UI
from level import Level
from menu import Menu # <-- Importamos a nova classe!

pygame.init()
screen = pygame.display.set_mode((1280, 720))
clock = pygame.time.Clock()

# --- ESTADOS DO JOGO ---
MENU = 0
JOGANDO = 1
VITORIA = 2
DERROTA = 3
TUTORIAL = 4
game_state = MENU # O jogo agora começa no Menu

# Inicializando UI e Menu
ui = UI()
game_menu = Menu(screen)

# Variáveis Globais de Gameplay
level = None
player = None
enemies = []
impacts = []
projectiles = []
dead_bodies = []

def reset_game():
    """Função auxiliar para iniciar/reiniciar a partida limpa"""
    global level, player, enemies, impacts, projectiles, dead_bodies
    level = Level("assets/maps/fase1_collision.png")
    player = Player(*level.player_spawn)
    enemies = []
    impacts = []
    projectiles = []
    dead_bodies = []
    
    for x, y in level.enemy_spawns:
        enemies.append(Enemy(x, y))

# Carregamento de Recursos Visuais e Sonoros do Game
crosshair = pygame.image.load("assets/ui/aim.png").convert_alpha()
dead_body_image = pygame.image.load("assets/ui/dead_body.png").convert_alpha()
die_sound = pygame.mixer.Sound("assets/sounds/die.mp3")
fire_impact_image = pygame.image.load("assets/gun/fire/730.png").convert_alpha()

running = True
dt = 0

while running:
    mouse_x, mouse_y = pygame.mouse.get_pos()
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            
        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            # O Menu decide o que acontece com o clique com base no estado atual!
            new_state, should_reset, should_quit = game_menu.handle_click((mouse_x, mouse_y), game_state)
            
            game_state = new_state
            
            if should_reset:
                reset_game()
            if should_quit:
                running = False

    # ==========================================
    # LÓGICA DE DESENHO E ATUALIZAÇÃO POR ESTADO
    # ==========================================
    
    if game_state == MENU:
        pygame.mouse.set_visible(True)
        game_menu.draw_main_menu()

    elif game_state == TUTORIAL:
        pygame.mouse.set_visible(True)
        game_menu.draw_tutorial()

    elif game_state == JOGANDO:
        pygame.mouse.set_visible(False)

        # --- UPDATE DA FASE ---
        if player.health > 0:
            bullet = player.update(level.walls)
            if bullet:
                projectiles.append(bullet)
        else:
            game_state = DERROTA

        for enemy in enemies:
            if enemy.health <= 0:
                continue
            enemy_bullet = enemy.update(player, level.walls)
            if enemy_bullet:
                projectiles.append(enemy_bullet)

        # --- UPDATE DOS PROJÉTEIS ---
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

        # --- DRAW DA FASE ---
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

        if player.health > 0: player.draw(screen)
        for enemy in enemies:
            if enemy.health > 0: enemy.draw(screen)
        for projectile in projectiles: projectile.draw(screen)
            
        ui.draw(screen, player)
        crosshair_rect = crosshair.get_rect(center=(mouse_x, mouse_y - 15))
        screen.blit(crosshair, crosshair_rect)

        # --- CHECAGEM DE VITÓRIA ---
        alive_enemies = sum(1 for enemy in enemies if enemy.health > 0)
        if alive_enemies == 0 and level.exit_point is not None:
            if player.get_rect().colliderect(level.exit_point):
                game_state = VITORIA

    elif game_state == VITORIA:
        pygame.mouse.set_visible(True)
        # Mantém a tela do jogo congelada no fundo e desenha o menu por cima
        level.draw(screen)
        for body in dead_bodies:
            rotated_dead_body = pygame.transform.rotate(dead_body_image, -body['angle'] - 120)
            rect = rotated_dead_body.get_rect(center=(body['x'], body['y']))
            screen.blit(rotated_dead_body, rect)
        for enemy in enemies:
            if enemy.health > 0: enemy.draw(screen)
        if player.health > 0: player.draw(screen)
        
        game_menu.draw_win_screen()

    elif game_state == DERROTA:
        pygame.mouse.set_visible(True)
        # Mantém a tela do jogo congelada no fundo e desenha o menu por cima
        level.draw(screen)
        for body in dead_bodies:
            rotated_dead_body = pygame.transform.rotate(dead_body_image, -body['angle'] - 120)
            rect = rotated_dead_body.get_rect(center=(body['x'], body['y']))
            screen.blit(rotated_dead_body, rect)
        for enemy in enemies:
            if enemy.health > 0: enemy.draw(screen)
            
        game_menu.draw_lose_screen()

    pygame.display.flip()
    dt = clock.tick(60) / 1000

pygame.quit()