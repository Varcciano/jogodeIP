"""
meio que a nossa engine (ferramenta que faz o jogo rodar).
o run do jogo vai acontecer nessa pasta .py, aqui tudo o que foi
customizado/feito nas outras será organizado e executado.
"""

# IMPORTS DE OUTRAS PASTAS OU DE BIBLIOTECAS PYTHON.
import pygame as pg
import sys
from settings import LARGURA, ALTURA, FPS, COR_FUNDO
from player import Player
from levels import Level1
from menu import MenuPrincipal
# ===================================================

pg.init()  # inicializa a biblioteca pygame.
larg_monitor, alt_monitor = pg.display.get_desktop_sizes()[0]
escala_inicial = max(1, min(int(larg_monitor * 0.9) //
                     LARGURA, int(alt_monitor * 0.85) // ALTURA))
tamanho_janela = (LARGURA * escala_inicial, ALTURA * escala_inicial)
janela = pg.display.set_mode(tamanho_janela, pg.RESIZABLE)
canvas = pg.Surface((LARGURA, ALTURA))  # jogo vai rolar visualmente aqui
tela_cheia = False
relogio = pg.time.Clock()  # relogio pra contar o tempo
pausado = False  # utilizado para freezar o jogo quando for minizado, pra n ficar rodando em segunda instância

levels = Level1()  # cria um objeto da classe Level1 da pasta de levels.py.
# cria um objeto da classe Player da pasta de player.py.
player = Player(50, 150)
menu = MenuPrincipal("Vetor Zero", ["Jogar", "Sair"])  # cria o menu
menu_pausa = MenuPrincipal("PAUSA", ["Continuar Jogando", "Sair"])
estado = "menu"  # começa no menu
# sequencia lógica da run do jogo: eventos -> atualização das lógicas -> desenhamento -> disposição do que foi desenhado.
while True:

    # dt é o delta time, extremamente importante: é o tempo que passou desde o último frame
    dt = relogio.tick(FPS) / 1000
    # importante para calcular quantidade de px / s, seja velocidade ou até mesmo aceleração
    # o relogio.tick(FPS) basicamente faz uma sincronização do jogo com os frames por segundo. Ele da um valor em ms
    # por isso dividimos por 1000, pra trabalhar o dt em seg.
    # evita que o retangulo bugue para fora da tela ao minimizar a janela ou sair da tela.
    dt = min(dt, 1 / 30)

    # pega todo tipo de evento que estiver rolando na tela. seja fechar, aperta tecla, clicar...
    for evento in pg.event.get():
        if evento.type == pg.QUIT:
            pg.quit()
            sys.exit()  # fecha a tela e a instância do jogo
        if evento.type == pg.WINDOWFOCUSLOST:
            pausado = True
        if evento.type == pg.WINDOWFOCUSGAINED:
            pausado = False
        if evento.type == pg.KEYDOWN and evento.key == pg.K_F11:
            tela_cheia = not tela_cheia
            if tela_cheia:
                janela = pg.display.set_mode((0, 0), pg.FULLSCREEN)
            else:
                janela = pg.display.set_mode(tamanho_janela, pg.RESIZABLE)

        if estado == "menu":
            acao = menu.processar_evento(evento)
            if acao == "Jogar":
                estado = "jogando"
            elif acao == "Sair":
                pg.quit()
                sys.exit()
        elif estado == "jogando":
            if evento.type == pg.KEYDOWN and evento.key == pg.K_ESCAPE:
                estado = "pausa"
                menu_pausa.indice = 0

        elif estado == "pausa":
            if evento.type == pg.KEYDOWN and evento == pg.K_ESCAPE:
                estado = "jogando"
            acao = menu_pausa.processar_evento(evento)
            if acao == "Continuar Jogando":
                estado = "jogando"
            elif acao == "Sair":
                pg.quit()
                sys.exit()

    # so atualiza os eventos do jogo enquanto o jogador estiver jogando de fato.
    if not pausado and estado == "jogando":
        player.update(dt, levels.solidos, levels.plataformas)

    canvas.fill(COR_FUNDO)  # desenha essa cor base para toda a tela

    if estado == "menu":
        menu.draw(canvas)
    elif estado == "jogando":
        levels.draw(canvas)  # criação do level na tela
        player.draw(canvas)  # criação do player na tela
    elif estado == "pausa":
        menu_pausa.draw(canvas)
    pg.display.flip()  # dispõe na tela o que foi desenhado.

    jw, jh = janela.get_size()
    esc = max(1, min(jw // LARGURA, jh // ALTURA))
    w, h = LARGURA * esc, ALTURA * esc
    janela.fill((0, 0, 0))   # faixas pretas se sobrar espaço
    janela.blit(pg.transform.scale(canvas, (w, h)),
                ((jw - w) // 2, (jh - h) // 2))
    pg.display.flip()
