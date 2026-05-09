import pygame
import sys

def tela_game_over(screen, score, kills_goblin, kills_dragao, kills_chefao):

    BRANCO      = (255, 255, 255)
    CINZA_BTN   = (90,  90,  90)
    CINZA_HOVER = (130, 130, 130)
    PRETO       = (0,   0,   0)

    fonte_info  = pygame.font.SysFont(None, 30)
    fonte_botao = pygame.font.SysFont(None, 32)
    # No seu bloco de inicialização de fontes:
    fonte_game_over = pygame.font.SysFont("Arial", 100, bold=True)

    W = screen.get_width()
    H = screen.get_height()

    try:
        fundo_go = pygame.image.load("ambientes/background - 1.png").convert()
        fundo_go = pygame.transform.scale(fundo_go, (W, H))
    except pygame.error as e:
        print(f"Erro ao carregar background game over: {e}")
        fundo_go = None

    margem      = 20
    btn_menu    = pygame.Rect(margem,            H - 68, 160, 48)
    btn_restart = pygame.Rect(W - 160 - margem, H - 68, 160, 48)

    rodando   = True
    resultado = None

    while rodando:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if btn_menu.collidepoint(event.pos):
                    resultado = 'menu'
                    rodando   = False
                if btn_restart.collidepoint(event.pos):
                    resultado = 'restart'
                    rodando   = False

        mouse = pygame.mouse.get_pos()

        if fundo_go:
            screen.blit(fundo_go, (0, 0))
        else:
            screen.fill(PRETO)

        txt_score = fonte_info.render(f"SCORE:  {score}", True, PRETO)
        screen.blit(txt_score, (W // 2 - txt_score.get_width() // 2, H // 2 + 10))

        txt_gameover = fonte_game_over.render("GAME OVER", True, PRETO)

        pos_x = (W // 2) - (txt_gameover.get_width() // 2)
        pos_y = 50

        sombra = fonte_game_over.render("GAME OVER", True, (50, 50, 50))
        screen.blit(sombra, (pos_x + 5, pos_y + 5))

        screen.blit(txt_gameover, (pos_x, pos_y))

        txt_kills = fonte_info.render(
            f"Goblins: {kills_goblin}    Dragões: {kills_dragao}    Chefões: {kills_chefao}",
            True, PRETO
        )
        screen.blit(txt_kills, (W // 2 - txt_kills.get_width() // 2, H // 2 + 45))

        cor_menu = CINZA_HOVER if btn_menu.collidepoint(mouse) else CINZA_BTN
        pygame.draw.rect(screen, cor_menu, btn_menu, border_radius=8)
        txt_menu = fonte_botao.render("MENU", True, BRANCO)
        screen.blit(txt_menu, (btn_menu.centerx - txt_menu.get_width() // 2,
                                btn_menu.centery - txt_menu.get_height() // 2))

        cor_rest = CINZA_HOVER if btn_restart.collidepoint(mouse) else CINZA_BTN
        pygame.draw.rect(screen, cor_rest, btn_restart, border_radius=8)
        txt_rest = fonte_botao.render("RESTART", True, BRANCO)
        screen.blit(txt_rest, (btn_restart.centerx - txt_rest.get_width() // 2,
                                btn_restart.centery - txt_rest.get_height() // 2))

        pygame.display.flip()

    return resultado