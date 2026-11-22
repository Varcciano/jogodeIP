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
# ===================================================

pg.init() # inicializa a biblioteca pygame.
tela = pg.display.set_mode((LARGURA, ALTURA)) # cria a tela/interface do jogo
relogio = pg.time.Clock() # relogio pra contar o tempo

levels = Level1() # cria um objeto da classe Level1 da pasta de levels.py.
player = Player(100, 300) # cria um objeto da classe Player da pasta de player.py.

while True: # sequencia lógica da run do jogo: eventos -> atualização das lógicas -> desenhamento -> disposição do que foi desenhado.

    dt = relogio.tick(FPS) / 1000 # dt é o delta time, extremamente importante: é o tempo que passou desde o último frame
    # importante para calcular quantidade de px / s, seja velocidade ou até mesmo aceleração
    # o relogio.tick(FPS) basicamente faz uma sincronização do jogo com os frames por segundo. Ele da um valor em ms
    # por isso dividimos por 1000, pra trabalhar o dt em seg.

    for evento in pg.event.get(): # pega todo tipo de evento que estiver rolando na tela. seja fechar, aperta tecla, clicar...
        if evento.type == pg.QUIT:
            pg.quit()
            sys.exit() # fecha a tela e a instância do jogo

    player.update(dt, levels.plataformas)

    tela.fill(COR_FUNDO) # desenha essa cor base para toda a tela
    levels.draw(tela) # criação do level na tela
    player.draw(tela) # criação do player na tela
    pg.display.flip() # dispõe na tela o que foi desenhado.
