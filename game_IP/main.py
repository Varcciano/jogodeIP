import pygame as pg
import sys
from settings import LARGURA, ALTURA, FPS, COR_FUNDO
from player import Player 
from levels import Level1

pg.init()
tela = pg.display.set_mode((LARGURA, ALTURA))
relogio = pg.time.Clock()

levels = Level1()
player = Player(100, 300)

while True:
    dt = relogio.tick(FPS) / 1000

    for evento in pg.event.get():
        if evento.type == pg.QUIT:
            pg.quit()
            sys.exit()

    player.update(dt, levels.plataformas)

    tela.fill(COR_FUNDO)
    levels.draw(tela)
    player.draw(tela)
    pg.display.flip()
