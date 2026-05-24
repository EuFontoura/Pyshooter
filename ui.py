import pygame


class UI:

    def __init__(self):

        self.health_icon = pygame.image.load(
            "assets/ui/life.png"
        ).convert_alpha()

        self.shield_icon = pygame.image.load(
            "assets/ui/shield.png"
        ).convert_alpha()

        self.bullet_icon = pygame.image.load(
            "assets/ui/ammunition.png"
        ).convert_alpha()

        self.font = pygame.font.SysFont(
            "arial",
            26,
            bold=True
        )


    def draw(self, screen, player):

        # -------- VIDA --------

        screen.blit(
            self.health_icon,
            (60, 640)
        )

        health_text = self.font.render(
            str(player.health),
            True,
            (255, 255, 255)
        )

        screen.blit(
            health_text,
            (10, 635)
        )

        # largura proporcional
        health_width = int(
            300 *
            (
                player.health /
                player.max_health
            )
        )

        pygame.draw.rect(
            screen,
            (220, 0, 0),
            (90, 640, health_width, 20)
        )


        # -------- ESCUDO --------

        screen.blit(
            self.shield_icon,
            (60, 670)
        )

        shield_text = self.font.render(
            str(player.shield),
            True,
            (255, 255, 255)
        )

        screen.blit(
            shield_text,
            (10, 667)
        )

        shield_width = int(
            300 *
            (
                player.shield /
                player.max_shield
            )
        )

        pygame.draw.rect(
            screen,
            (0, 80, 255),
            (90, 670, shield_width, 20)
        )


        # -------- MUNIÇÃO --------

        ammo_text = self.font.render(
            str(player.weapon.ammo),
            True,
            (255, 190, 0)
        )

        screen.blit(
            self.bullet_icon,
            (1080, 630)
        )

        screen.blit(
            ammo_text,
            (1150, 650)
        )