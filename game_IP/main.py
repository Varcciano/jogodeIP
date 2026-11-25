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
from colecionaveis import Sucata
# ===================================================

pg.init() # inicializa a biblioteca pygame.
larg_monitor, alt_monitor = pg.display.get_desktop_sizes()[0]
escala_inicial = max(1, min(int(larg_monitor * 0.9) // LARGURA, int(alt_monitor * 0.85) // ALTURA))
tamanho_janela = (LARGURA * escala_inicial, ALTURA * escala_inicial)
janela = pg.display.set_mode(tamanho_janela, pg.RESIZABLE)
canvas = pg.Surface((LARGURA, ALTURA)) # jogo vai rolar visualmente aqui
tela_cheia = False
relogio = pg.time.Clock() # relogio pra contar o tempo
pausado = False # utilizado para freezar o jogo quando for minizado, pra n ficar rodando em segunda instância

levels = Level1() # cria um objeto da classe Level1 da pasta de levels.py.
player = Player(50, 150) # cria um objeto da classe Player da pasta de player.py.

# Lista com todas as sucatas que existem na fase agora.
# Cada Sucata(x, y) é um objeto novo, com seu próprio rect.
# Coloquei algumas em cima das plataformas e uma no chão pra testar.
lista_sucatas = [
    Sucata(80, 180),    # em cima da plataforma 1
    Sucata(180, 130),   # em cima da plataforma 2
    Sucata(280, 80),    # em cima da plataforma 3 (a mais alta)
    Sucata(390, 145),   # em cima da plataforma 5
    Sucata(300, 238),   # no chão
]

# Contador de sucata que o jogador já pegou. Começa em 0.
# (Por enquanto coloquei aqui no main.py pra não mexer no player.py no momento.)
sucata_total = 0

while True: # sequencia lógica da run do jogo: eventos -> atualização das lógicas -> desenhamento -> disposição do que foi desenhado.

    dt = relogio.tick(FPS) / 1000 # dt é o delta time, extremamente importante: é o tempo que passou desde o último frame
    # importante para calcular quantidade de px / s, seja velocidade ou até mesmo aceleração
    # o relogio.tick(FPS) basicamente faz uma sincronização do jogo com os frames por segundo. Ele da um valor em ms
    # por isso dividimos por 1000, pra trabalhar o dt em seg.
    dt = min(dt, 1 / 30) # evita que o retangulo bugue para fora da tela ao minimizar a janela ou sair da tela.

    for evento in pg.event.get(): # pega todo tipo de evento que estiver rolando na tela. seja fechar, aperta tecla, clicar...
        if evento.type == pg.QUIT:
            pg.quit()
            sys.exit() # fecha a tela e a instância do jogo
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
    
    if not pausado: # so atualiza os eventos do jogo enquanto o jogador estiver jogando de fato. 
        player.update(dt, levels.solidos, levels.plataformas)

        # --- COLETA DE SUCATA ---
        # Passa por cada sucata da lista, uma de cada vez.
        for sucata in lista_sucatas:

            # verifica se o jogador encontou no retangulo da sucata. Tee o mesmo colliderect que o arquivo player,py usa nos sólidos,
            if player.rect.colliderect(sucata.rect):
                sucata.coletar() # diz que a moeda foi coletada
                sucata_total += sucata.valor # soma o valor da sucata ao contador
                print('Sucata:', sucata_total) # print temporário para teste

        # lista nova das sucatas que ainda não foram coletadas
        nova_lista_sucatas = []
        for sucata in lista_sucatas:
            if not sucata.coletado:
                nova_lista_sucatas.append(sucata)
        lista_sucatas = nova_lista_sucatas

    canvas.fill(COR_FUNDO) # desenha essa cor base para toda a tela
    levels.draw(canvas) # criação do level na tela
    
    for sucata in lista_sucatas: # desenha cada sucata que ainda não foi coletada
        sucata.draw(canvas)
    
    player.draw(canvas) # criação do player na tela
    pg.display.flip() # dispõe na tela o que foi desenhado.

    jw, jh = janela.get_size()
    esc = max(1, min(jw // LARGURA, jh // ALTURA))
    w, h = LARGURA * esc, ALTURA * esc
    janela.fill((0, 0, 0))   # faixas pretas se sobrar espaço
    janela.blit(pg.transform.scale(canvas, (w, h)), ((jw - w) // 2, (jh - h) // 2))
    pg.display.flip()
    
