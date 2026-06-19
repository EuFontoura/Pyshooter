import pygame

class Menu:
    def __init__(self, screen):
        self.screen = screen
        
        # Fontes
        self.font_menu = pygame.font.SysFont("impact", 80)
        self.font_tutorial = pygame.font.SysFont("arial", 30, bold=True)

        # Imagens
        try:
            self.main_bg = pygame.image.load("assets/ui/main_bg.png").convert()
            self.main_bg = pygame.transform.scale(self.main_bg, (1280, 720))
        except FileNotFoundError:
            # Fundo de emergência caso a imagem não seja encontrada
            self.main_bg = pygame.Surface((1280, 720))
            self.main_bg.fill((40, 40, 40)) 

        self.win_image = pygame.image.load("assets/ui/win_menu.png").convert_alpha()
        self.win_rect = self.win_image.get_rect(center=(1280 // 2, 720 // 2))

        self.lose_image = pygame.image.load("assets/ui/lose_menu.png").convert_alpha()
        self.lose_rect = self.lose_image.get_rect(center=(1280 // 2, 720 // 2))

        # Hitboxes dos Botões do Menu Principal
        self.play_btn = pygame.Rect(540, 250, 200, 80)
        self.tutorial_btn = pygame.Rect(490, 350, 300, 80)
        self.exit_btn = pygame.Rect(540, 450, 200, 80)
        self.back_btn = pygame.Rect(50, 620, 150, 50)

        # Hitboxes configuradas por você no main.py original
        self.ok_win_btn = pygame.Rect(540, 360, 200, 60)
        self.yes_lose_btn = pygame.Rect(480, 360, 160, 60)
        self.no_lose_btn = pygame.Rect(660, 360, 160, 60)

    def draw_text(self, text, font, color, x, y):
        img = font.render(text, True, color)
        self.screen.blit(img, (x, y))

    def draw_main_menu(self):
        self.screen.blit(self.main_bg, (0, 0))
        self.draw_text("PLAY", self.font_menu, (255, 255, 255), 565, 250)
        self.draw_text("TUTORIAL", self.font_menu, (255, 255, 255), 495, 350)
        self.draw_text("EXIT", self.font_menu, (255, 255, 255), 570, 450)

    def draw_tutorial(self):
        self.screen.blit(self.main_bg, (0, 0))
        
        # Fundo escuro transparente para facilitar a leitura
        overlay = pygame.Surface((1280, 720), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 180))
        self.screen.blit(overlay, (0, 0))
        
        controles = [
            "W / S - Andar para Frente / Trás",
            "A / D - Andar para Esquerda / Direita",
            "R - Recarregar Arma",
            "Botão Esquerdo - Atirar",
            "",
            "OBJETIVO: Elimine todos os inimigos e chegue ao ponto amarelo."
        ]
        
        for i, linha in enumerate(controles):
            txt = self.font_tutorial.render(linha, True, (255, 255, 0))
            self.screen.blit(txt, (350, 200 + (i * 40)))
            
        pygame.draw.rect(self.screen, (255, 255, 255), self.back_btn, 2)
        self.draw_text("BACK", self.font_tutorial, (255, 255, 255), 90, 630)

    def draw_win_screen(self):
        self.screen.blit(self.win_image, self.win_rect)

    def draw_lose_screen(self):
        self.screen.blit(self.lose_image, self.lose_rect)

    def handle_click(self, mouse_pos, current_state):
        """
        Retorna: (novo_estado, resetar_jogo, fechar_jogo)
        """
        x, y = mouse_pos
        
        if current_state == 0: # MENU
            if self.play_btn.collidepoint(x, y):
                return 1, True, False # Vai para JOGANDO
            if self.tutorial_btn.collidepoint(x, y):
                return 4, False, False # Vai para TUTORIAL
            if self.exit_btn.collidepoint(x, y):
                return 0, False, True # Fecha o jogo
                
        elif current_state == 4: # TUTORIAL
            if self.back_btn.collidepoint(x, y):
                return 0, False, False # Volta pro MENU
                
        elif current_state == 2: # VITORIA
            if self.ok_win_btn.collidepoint(x, y):
                return 0, False, False # Volta pro MENU
                
        elif current_state == 3: # DERROTA
            if self.yes_lose_btn.collidepoint(x, y):
                return 1, True, False # Reinicia partida
            if self.no_lose_btn.collidepoint(x, y):
                return 0, False, False # Volta pro MENU
                
        return current_state, False, False