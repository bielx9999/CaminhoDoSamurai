import pygame
import random
import sys
from Samurai import *
from Inimigo import *
from Dragao import *
from Chefao import *
from ShootShuriken import *
from Tela_menu import tela_inicial
from Tela_game_over import tela_game_over
from Tela_vitoria import tela_vitoria

pygame.init()

display = pygame.display.set_mode([900, 480]) #Tela do jogo
pygame.display.set_caption("Caminho do Samurai") #Nome da Janela

musica_game   = "Sons/MusicaGame.mp3"
musica_chefao = "Sons/Musica_Chefao.mp3"

SCORE_VITORIA = 250 # pontuacao da vitoria

def carregar_hud():
    vidas_imgs = {
        0: pygame.transform.scale(pygame.image.load('Personagem/coracao/0.png').convert_alpha(),      (120, 40)),
        1: pygame.transform.scale(pygame.image.load('Personagem/coracao/1 vida.png').convert_alpha(), (120, 40)),
        2: pygame.transform.scale(pygame.image.load('Personagem/coracao/2 vida.png').convert_alpha(), (120, 40)),
        3: pygame.transform.scale(pygame.image.load('Personagem/coracao/3 vida.png').convert_alpha(), (120, 40)),
    }
    icones = {
        'goblin': pygame.transform.scale(pygame.image.load('Personagem/goblin.png').convert_alpha(), (40, 30)),
        'dragao': pygame.transform.scale(pygame.image.load('Personagem/dragao.png').convert_alpha(), (40, 30)),
        'chefao': pygame.transform.scale(pygame.image.load('Personagem/chefao.PNG').convert_alpha(), (40, 35)),
    }
    return vidas_imgs, icones


def iniciar_jogo():
    ObjectGroup  = pygame.sprite.Group()
    InimigoGroup = pygame.sprite.Group()
    ChefaoGroup  = pygame.sprite.Group()
    ShootGroup   = pygame.sprite.Group()

    bg = pygame.sprite.Sprite(ObjectGroup)
    bg.image = pygame.transform.scale(
        pygame.image.load('ambientes/background - 1.png'), [900, 480]
    )

    bg.rect = bg.image.get_rect()
    guy = Samurai(ObjectGroup)
    Inimigo(ObjectGroup, InimigoGroup)
    pygame.mixer_music.load(musica_game)
    pygame.mixer_music.play(-1)

    shoot_sound = pygame.mixer.Sound('Sons/EspadaLanca.ogg') # Som da shuriken

    estado = {
        'kills_goblin': 0,
        'kills_dragao': 0,
        'kills_chefao': 0,
        'score':        0,
        'gameOver':     False,
        'venceu':       False,
        'chefao_ativo': False,
        'chefao_inst':  None,
        'musica_chefao_tocando': False,
        'timer_goblin': 0,
        'timer_dragao': 0,
        'timer_chefao': 0,
    }

    return ObjectGroup, InimigoGroup, ChefaoGroup, ShootGroup, guy, shoot_sound, estado


def spawnar_chefao(guy, ObjectGroup, ChefaoGroup, InimigoGroup, estado):
    boss = Chefao(guy, ObjectGroup, ChefaoGroup)
    estado['chefao_ativo'] = True
    estado['chefao_inst']  = boss
    for inimigo in InimigoGroup:
        inimigo.kill()
    pygame.mixer_music.load(musica_chefao)
    pygame.mixer_music.play(-1)
    estado['musica_chefao_tocando'] = True

def voltar_musica_normal(estado):
    pygame.mixer_music.load(musica_game)
    pygame.mixer_music.play(-1)
    estado['musica_chefao_tocando'] = False

def desenhar_hud_holder(surface, x, y, w, h):
    holder = pygame.Surface((w, h), pygame.SRCALPHA)
    holder.fill((0, 0, 0, 140))
    surface.blit(holder, (x, y))

vidas_imagens, icones = carregar_hud()
fonte_hud   = pygame.font.SysFont(None, 30)
fonte_score = pygame.font.SysFont(None, 32)
fonte_boss  = pygame.font.SysFont(None, 28)

clock = pygame.time.Clock()

tela_inicial(display)

rodando = True
while rodando:

    ObjectGroup, InimigoGroup, ChefaoGroup, ShootGroup, guy, shoot_sound, estado = iniciar_jogo()

    while not estado['gameOver'] and not estado['venceu']:
        clock.tick(60)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    shoot_sound.play()
                    ns = Shuriken(guy.rect.centerx, guy.rect.centery,
                                  guy.direcao, ObjectGroup, ShootGroup)
                    ns.rect.center = guy.rect.center

        ObjectGroup.update()

        bateram = pygame.sprite.spritecollide(guy, InimigoGroup, True, pygame.sprite.collide_mask)
        for _ in bateram:
            guy.vidas -= 1
            if guy.vidas <= 0:
                estado['gameOver'] = True

        if estado['chefao_ativo']:
            if pygame.sprite.spritecollide(guy, ChefaoGroup, False, pygame.sprite.collide_mask):
                guy.vidas -= 1
                if guy.vidas <= 0:
                    estado['gameOver'] = True

        hit_normal = pygame.sprite.groupcollide(ShootGroup, InimigoGroup, True, True, pygame.sprite.collide_mask)
        for _, atingidos in hit_normal.items():
            for inimigo in atingidos:
                if isinstance(inimigo, Dragao):
                    estado['kills_dragao'] += 1
                    estado['score']        += 10
                else:
                    estado['kills_goblin'] += 1
                    estado['score']        += 5

        if estado['chefao_ativo']:
            hit_chefao = pygame.sprite.groupcollide(ShootGroup, ChefaoGroup, True, False, pygame.sprite.collide_mask)
            for _, atingidos in hit_chefao.items():
                for boss in atingidos:
                    boss.vida -= 1
                    if boss.vida <= 0:
                        boss.kill()
                        estado['chefao_ativo'] = False
                        estado['chefao_inst']  = None
                        estado['kills_chefao'] += 1
                        estado['score']        += 30
                        voltar_musica_normal(estado)

        ## verifica condição de vitória
        if estado['score'] >= SCORE_VITORIA:
            estado['venceu'] = True
        # ──────────────────────────────────────────────────────────────────────

        if not estado['chefao_ativo']:
            estado['timer_goblin'] += 1
            if estado['timer_goblin'] > 20:
                estado['timer_goblin'] = 0
                if random.random() < 0.2:
                    Inimigo(ObjectGroup, InimigoGroup)

            estado['timer_dragao'] += 1
            if estado['timer_dragao'] > 40:
                estado['timer_dragao'] = 0
                if random.random() < 0.15:
                    Dragao(ObjectGroup, InimigoGroup)

        if not estado['chefao_ativo']:
            estado['timer_chefao'] += 1
            if estado['timer_chefao'] >= 1800 and random.random() < 0.008:
                spawnar_chefao(guy, ObjectGroup, ChefaoGroup, InimigoGroup, estado)
                estado['timer_chefao'] = 0

        display.fill([94, 174, 190])
        ObjectGroup.draw(display)

        display.blit(vidas_imagens[max(0, min(guy.vidas, 3))], (8, 8))

        txt_score = fonte_score.render(f"SCORE: {estado['score']}", True, (255, 255, 255))
        display.blit(txt_score, (400 - txt_score.get_width() - 11, 13))

        display.blit(icones['goblin'], (535, 7))
        display.blit(fonte_hud.render(f"x{estado['kills_goblin']}", True, (255, 255, 255)), (578, 13))

        display.blit(icones['dragao'], (620, 7))
        display.blit(fonte_hud.render(f"x{estado['kills_dragao']}", True, (255, 255, 255)), (663, 13))

        display.blit(icones['chefao'], (705, 4))
        display.blit(fonte_hud.render(f"x{estado['kills_chefao']}", True, (255, 220, 0)), (748, 13))

        if estado['chefao_ativo'] and estado['chefao_inst']:
            pygame.draw.rect(display, (80, 0, 0),  (245, 40, 410, 18), border_radius=5)
            bw = int((estado['chefao_inst'].vida / 10) * 410)
            pygame.draw.rect(display, (220, 0, 0), (245, 40, bw,  18), border_radius=5)
            tb = fonte_boss.render(f"CHEFÃO  {estado['chefao_inst'].vida}/10", True, (255, 255, 255))
            display.blit(tb, (450 - tb.get_width() // 2, 40))

        pygame.display.update()

    # decide qual tela mostrar
    pygame.mixer_music.stop()

    if estado['venceu']:
        escolha = tela_vitoria(
            display,
            estado['score'],
            estado['kills_goblin'],
            estado['kills_dragao'],
            estado['kills_chefao'],
        )
    else:
        escolha = tela_game_over(
            display,
            estado['score'],
            estado['kills_goblin'],
            estado['kills_dragao'],
            estado['kills_chefao'],
        )

    if escolha == 'menu':
        tela_inicial(display)