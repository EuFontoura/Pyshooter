import pygame

pygame.init()

class Player: 
    def __init__(self):
        
        self.body = pygame.image.load("assets/characters/player/player_body.png").convert_alpha()

        self.head = pygame.image.load("assets/characters/player/player_head.png").convert_alpha()

        self.left_hand = pygame.image.load("assets/characters/player/player_left.png").convert_alpha()

        self.right_hand = pygame.image.load("assets/characters/player/player_right.png").convert_alpha()

        self.x = 400
        self.y = 300

    def update(self):

        keys = pygame.key.get_pressed()

        if keys[pygame.K_w]:
                self.y -= 5

        if keys[pygame.K_s]:
                self.y += 5

        if keys[pygame.K_a]:
                self.x -= 5

        if keys[pygame.K_d]:
                self.x += 5

    def draw(self, screen):

        screen.blit(
            self.body,
            (self.x, self.y)
        )


        screen.blit(
            self.left_hand,
            (self.x - 0, self.y - 5)
        )

        screen.blit(
            self.right_hand,
            (self.x + 14, self.y)
        )

        screen.blit(
            self.head,
            (self.x, self.y + 3)
        )