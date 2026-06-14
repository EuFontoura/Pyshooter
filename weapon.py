import pygame
import math
from projectile import Projectile

class Weapon:

    def __init__(self):

        image = pygame.image.load(
            "assets/gun/shapes/836.png"
        ).convert_alpha()

        self.image = pygame.transform.rotate(
            image,
            +35
        )
        
        self.muzzle_flash = pygame.image.load(
        "assets/gun/fire/730.png"
        ).convert_alpha()

        self.muzzle_offset_x = 35
        self.muzzle_offset_y = 14

        self.muzzle_flash = pygame.transform.rotate(
            self.muzzle_flash,
            +35
        )
            
                # tiros por segundo
        self.fire_rate = 10

        # tempo entre tiros
        self.cooldown = 1000 / self.fire_rate

        self.projectile_speed = 15

        # último disparo
        self.last_shot = 0

        # som
        self.shot_sound = pygame.mixer.Sound(
            "assets/sounds/shoot.mp3"
        )
        
        self.reload_sound = pygame.mixer.Sound(
            "assets/sounds/reload.mp3"
        )
        
        # imagem flash
        self.show_flash = False
        self.flash_duration = 20
        self.flash_start = 0
        
        self.magazine_size = 50
        self.ammo = 50 
        self.angle = 0

        self.is_reloading = False
        self.reload_time = 2000 # 2 seconds
        self.reload_start = 0


    def update(self, owner_x, owner_y, target_x, target_y):

        dx = target_x - owner_x
        dy = target_y - owner_y

        self.angle = math.degrees(
            math.atan2(dy, dx)
        )

        # Check for reload completion
        if self.is_reloading:
            current_time = pygame.time.get_ticks()
            if current_time - self.reload_start >= self.reload_time:
                self.ammo = self.magazine_size
                self.is_reloading = False
                self.reload_sound.stop()

    def shoot(self, x, y, owner):

        if self.is_reloading:
            return None

        if self.ammo <= 0:
            self.start_reload()
            return None

        current_time = pygame.time.get_ticks()

        can_shoot = (
            current_time - self.last_shot >= self.cooldown
        )

        if can_shoot:

            self.ammo -= 1
            self.last_shot = current_time
            self.shot_sound.play()

            muzzle_x, muzzle_y = self.get_muzzle_position(x, y)

            return Projectile(
                muzzle_x,
                muzzle_y,
                self.angle,
                self.projectile_speed,
                owner
            )

        return None

    def start_reload(self):
        if not self.is_reloading and self.ammo < self.magazine_size:
            self.is_reloading = True
            self.reload_start = pygame.time.get_ticks()
            self.reload_sound.play(loops=-1)
    
    def get_muzzle_position(self, x, y):

        radians = math.radians(self.angle)

        # offset no espaço local da arma
        local_x = self.muzzle_offset_x
        local_y = self.muzzle_offset_y

        # aplica rotação
        muzzle_x = x + (
            local_x * math.cos(radians) -
            local_y * math.sin(radians)
        )

        muzzle_y = y + (
            local_x * math.sin(radians) +
            local_y * math.cos(radians)
        )

        return muzzle_x, muzzle_y

    def draw(self, screen, x, y):

        rect = self.image.get_rect(
            center=(x, y)
        )

        screen.blit(
            self.image,
            rect
        )
        
        current_time = pygame.time.get_ticks()

        flash_visible = (
            current_time - self.last_shot
            < self.flash_duration
        )

        if flash_visible:

            flash_rect = self.muzzle_flash.get_rect(
                center=(x - 14, y - 20)
            )

            screen.blit(
                self.muzzle_flash,
                flash_rect
            )