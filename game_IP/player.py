import pygame as pg
from settings import COR_PLAYER, GRAVIDADE, VEL_PULO

class Player:
    def __init__(self, x, y):
        self.rect = pg.Rect(x, y, 40, 70)
        self.pos = pg.Vector2(x, y) # posição atual
        self.vel = pg.Vector2(0, 0) # velocidade atual
        self.velocidade = 300
        self.no_chao = False # identificar pulo ou n
        
    def update(self, dt, plataformas):
        teclas = pg.key.get_pressed() # identificar pressionamento de tecla e qual tecla foi apertada

        # velocidade na horizontal (esquerda ou direita)
        self.vel.x = 0
        if teclas[pg.K_a] or teclas[pg.K_LEFT]: 
            self.vel.x -= self.velocidade
        if teclas[pg.K_d] or teclas[pg.K_RIGHT]:
            self.vel.x += self.velocidade
        
        # mecanica de pulo
        if(teclas[pg.K_SPACE] or teclas[pg.K_w]) and self.no_chao:
            self.vel.y = VEL_PULO

        # mecanica de gravidade pra o personagem voltar ao chão.
        self.vel.y += GRAVIDADE * dt

        # movimento na coordenada x e colisões
        self.pos.x += self.vel.x * dt
        self.rect.x = round(self.pos.x)
        for p in plataformas:
            if self.rect.colliderect(p):
                if self.vel.x > 0: # andando pra direita
                    self.rect.right = p.left
                elif self.vel.x < 0: # para a esquerda
                    self.rect.left = p.right
                self.pos.x = self.rect.x

        self.pos.y += self.vel.y * dt
        self.rect.y = round(self.pos.y)
        self.no_chao = False
        for p in plataformas:
            if self.rect.colliderect(p):
                if self.vel.y > 0: # ao cair até o chão 
                    self.rect.bottom = p.top
                    self.no_chao = True
                elif self.vel.y < 0: # no pulo e ao bater a cabeça.
                    self.rect.top = p.bottom
                self.vel.y = 0
                self.pos.y = self.rect.y

    # desenha os elementos postos no player e seus atributos na tela
    def draw(self, tela):
        pg.draw.rect(tela, COR_PLAYER, self.rect)