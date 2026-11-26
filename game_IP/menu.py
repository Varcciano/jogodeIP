import pygame as pg
from settings import LARGURA, COR_FUNDO, COR_TITULO, COR_TEXTO, COR_SELECIONADO


class MenuPrincipal:
    def __init__(self, titulo, opcoes):
        self.titulo = titulo
        self.opcoes = opcoes
        self.indice = 0  # vai indicar a posição selicionada
        self.fonte_titulo = pg.font.Font(None, 64)
        self.fonte_opcao = pg.font.Font(None, 32)

    # desenha o menu na tela
    def draw(self, tela):
        tela.fill(COR_FUNDO)

        titulo = self.fonte_titulo.render(self.titulo, True, COR_TITULO)
        tela.blit(titulo, titulo.get_rect(center=(LARGURA//2, 80)))

        for i, texto in enumerate(self.opcoes):
            cor = COR_SELECIONADO if i == self.indice else COR_TEXTO
            surf = self.fonte_opcao.render(texto, True, cor)
            tela.blit(surf, surf.get_rect(center=(LARGURA // 2, 150 + i * 40)))

    def processar_evento(self, evento):
        if evento.type == pg.KEYDOWN:
            if evento.key in (pg.K_UP, pg.K_w):
                self.indice = (self.indice - 1) % len(self.opcoes)

            elif evento.key in (pg.K_DOWN, pg.K_s):
                self.indice = (self.indice + 1) % len(self.opcoes)
            elif evento.key == pg.K_RETURN:
                return self.opcoes[self.indice]

        return None
