import pygame
import sys

def tela_inicial(screen):
    try:
        fundo_img = pygame.image.load("ambientes/background - MENU.png").convert()
        botao_img = pygame.image.load("ambientes/Botao.png").convert_alpha()
    except pygame.error as e:
        print(f"Erro ao carregar imagem: {e}")
        pygame.quit()
        sys.exit()

    botao_img = pygame.transform.scale(botao_img, (200, 200))
    fundo_img = pygame.transform.scale(fundo_img, (screen.get_width(), screen.get_height()))
    botao_rect = botao_img.get_rect(center=(screen.get_width() // 2, screen.get_height() // 2 + 100))

    fonte          = pygame.font.SysFont(None, 22)
    fonte_objetivo = pygame.font.SysFont(None, 22, bold=True)
    BRANCO         = (255, 255, 255)
    DOURADO        = (255, 215,   0)

    controles = "W - Pular      A - Esquerda      D - Direita      ESPAÇO - Atirar"
    texto = fonte.render(controles, True, BRANCO)

    objetivo = "ATINJA 250 PONTOS PARA GANHAR "
    txt_obj  = fonte_objetivo.render(objetivo, True, BRANCO)

    padding = 10
    texto_x = screen.get_width() // 2 - texto.get_width() // 2
    texto_y = screen.get_height() - 30

    obj_x = screen.get_width() // 2 - txt_obj.get_width() // 2    # ← NOVO
    obj_y = texto_y - 25                                          # ← NOVO (acima dos controles)

    hover = pygame.Surface((texto.get_width() + padding * 2, texto.get_height() + padding), pygame.SRCALPHA)
    hover.fill((0, 0, 0, 100))

    # Fundo semi-transparente para o texto objetivo também                ← NOVO
    hover_obj = pygame.Surface((txt_obj.get_width() + padding * 2, txt_obj.get_height() + padding), pygame.SRCALPHA)
    hover_obj.fill((0, 0, 0, 100))

    menu_rodando = True
    while menu_rodando:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1 and botao_rect.collidepoint(event.pos):
                    menu_rodando = False

        screen.blit(fundo_img, (0, 0))

        # Texto objetivo                                                   ← NOVO
        screen.blit(hover_obj, (obj_x - padding, obj_y - padding // 2))
        screen.blit(txt_obj,   (obj_x, obj_y))

        # Controles (igual ao original)
        screen.blit(hover, (texto_x - padding, texto_y - padding // 2))
        screen.blit(texto, (texto_x, texto_y))

        botao_img.set_alpha(200 if botao_rect.collidepoint(pygame.mouse.get_pos()) else 255)
        screen.blit(botao_img, botao_rect.topleft)

        pygame.display.flip()