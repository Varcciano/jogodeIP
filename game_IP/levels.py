import pygame as pg
from settings import LARGURA, ALTURA

# Desenha o chão inicial do jogo
class Level1:
    def __init__(self):
        self.plataformas = [pg.Rect(0, ALTURA - 40, LARGURA, 40)]

    def draw(self, tela):
        for p in self.plataformas:
            pg.draw.rect(tela, (60, 80, 110), p)

# TESTANDO CLONE DE REPOSITÓRIO    