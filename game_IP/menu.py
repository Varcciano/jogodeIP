from settings import LARGURA, COR_FUNDO, COR_TITULO, COR_TEXTO, COR_SELECIONADO, ALTURA
import pygame as pg
import os
PASTA = os.path.dirname(os.path.abspath(__file__))


class MenuPrincipal:
    def __init__(self, titulo, opcoes):
        self.titulo = titulo
        self.opcoes = opcoes
        self.indice = 0  # vai indicar a posição selicionada
        self.fonte_titulo = pg.font.Font(None, 64)
        self.fonte_opcao = pg.font.Font(None, 32)
        self.frames = []
        pasta_frames = os.path.join(PASTA, "assets", "fundo_animado")
        for i in range(48):
            caminho = os.path.join(pasta_frames, f"frame_{i:02d}.png")
            self.frames.append(pg.image.load(caminho).convert())

        self.frame_atual = 0
        self.ultima_troca = pg.time.get_ticks()
        self.intervalo = 80
    # desenha o menu na tela

    def draw(self, tela):
        agora = pg.time.get_ticks()
        if agora - self.ultima_troca >= self.intervalo:
            self.frame_atual = (self.frame_atual + 1) % len(self.frames)
            self.ultima_troca = agora

        fundo = pg.transform.scale(
            self.frames[self.frame_atual], (LARGURA, ALTURA))
        tela.blit(fundo, (0, 0))

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
