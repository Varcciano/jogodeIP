import pygame as pg
from settings import TAM_COLETAVEL, COR_SUCATA, VALOR_SUCATA

# Classe BASE: tudo que é colecionável tem em comum:
# um retângulo (posição + tamanho), uma cor e se já foi pego
class Colecionavel:
    
    def __init__(self, x, y, cor):
        
        # Retângulo do item: guarda POSIÇÃO (x, y) e TAMANHO (largura, altura).
        # Usado pra desenhar o item e pra detectar se o player encostou nele.
        self.rect = pg.Rect(x, y, TAM_COLETAVEL, TAM_COLETAVEL)
        # cor do quadrado
        self.cor = cor
        self.coletado = False  # quando virar True, o main.py remove o item

    # aciona quando o jogador encostar no item
    def coletar(self):
        self.coletado = True

    # desenha o item na tela
    # tela é o canvas, a superfice onde vamos desenhar no main.py
    def draw(self, tela):
        pg.draw.rect(tela, self.cor, self.rect)


# Sucata HERDA de Colecionavel: ganha rect, cor, coletar() e draw().
class Sucata(Colecionavel):
    
    def __init__(self, x, y):
        super().__init__(x, y, COR_SUCATA)  # chama o __init__ da classe base
        self.valor = VALOR_SUCATA