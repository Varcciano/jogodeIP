import pygame as pg
from settings import LARGURA, ALTURA, COR_CHAO, COR_PLATAFORMA

# Desenha o chão inicial do jogo
class Level1:
    def __init__(self):
        # todos as estruturas que não são possiveis de atravessar.
        self.solidos = [pg.Rect(0, ALTURA - 20, LARGURA, 20)]

        self.plataformas = [ #plataformas que são atravessaveis de lado e por baixo, so pra teste
            pg.Rect(50, 200, 75, 8),
            pg.Rect(150, 150, 75, 8),
            pg.Rect(250, 100, 75, 8),
            pg.Rect(250, 200, 75, 8),
            pg.Rect(360, 165, 75, 8),
        ]
    def draw(self, tela):
        for s in self.solidos:
            pg.draw.rect(tela, COR_CHAO, s)
        for p in self.plataformas:
            pg.draw.rect(tela, COR_PLATAFORMA, p)

    
