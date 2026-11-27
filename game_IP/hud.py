import pygame as pg
from settings import (COR_HUD_TEXTO, TAM_FONTE_HUD, MARGEM_HUD,
                      COR_SUCATA, TAM_COLETAVEL)

# ============================================================
# HUD: as informações fixas na tela
# (contador de sucata, e depois vida, armadura, arma...).
# ============================================================
class HUD:
    def __init__(self):
        # Cria a fonte UMA vez só, aqui no início.
        # None = usa a fonte padrão do pygame; o 2º valor é o tamanho.
        # Não criamos a fonte dentro do draw porque o draw roda 60x por
        # segundo, e criar fonte todo frame deixaria o jogo pesado.
        self.fonte = pg.font.Font(None, TAM_FONTE_HUD)

    # Desenha o HUD. Recebe a tela e o valor que precisa mostrar.
    # (o HUD só MOSTRA o número, quem guarda o número é o main.py)
    def draw(self, tela, sucata_total):

        # Ícone: um quadradinho da mesma cor e tamanho da sucata.
        # Assim o jogador associa "quadrado amarelo = sucata".
        # Fica no canto superior esquerdo, respeitando a margem.
        icone = pg.Rect(MARGEM_HUD, MARGEM_HUD, TAM_COLETAVEL, TAM_COLETAVEL)
        pg.draw.rect(tela, COR_SUCATA, icone)

        # render() transforma o texto em imagem.
        #  - f"x {sucata_total}" -> f-string: troca {sucata_total} pelo valor
        #    (se for 3, vira "x 3")
        #  - False -> sem suavização (antialias). Em pixel art, bordas
        #    nítidas ficam mais bonitas que bordas borradas.
        #  - COR_HUD_TEXTO -> cor das letras
        texto = self.fonte.render(f"x {sucata_total}", False, COR_HUD_TEXTO)

        # blit() cola a imagem do texto na tela, na posição (x, y).
        #  - x: logo à direita do ícone (+4 px de respiro)
        #  - y: alinhado ao centro vertical do ícone
        #    (centery = y do meio do ícone; subtraímos metade da altura
        #    do texto para o texto ficar centralizado nele)
        tela.blit(texto, (icone.right + 4,
                          icone.centery - texto.get_height() // 2))