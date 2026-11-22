import pygame as pg
from settings import COR_PLAYER, GRAVIDADE, VEL_PULO

class Player:
    def __init__(self, x, y):
        self.rect = pg.Rect(x, y, 40, 70) # (retângulo) corpo prótotipo do player para colisão e para referencial. 
        self.pos = pg.Vector2(x, y) # vai ser usado para posição e representa a posição atual
        self.vel = pg.Vector2(0, 0) # vai ser usado para velocidade e representa a velocidade atual
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
        # toda ideia de mudança de posição partem de uma mesma premissa:
        # primeiro a velocidade altera conforme aperto da tecla de movimento.
        # segundo a posição é incrementada pela velocidade "60 vezes por segundo"
        # terceiro a posição é arredondada e atualiza a coordenada do retângulo na tela "60 vezes por segundo"
        
        # movimento na coordenada x e colisões
        self.pos.x += self.vel.x * dt
        self.rect.x = round(self.pos.x)
        for p in plataformas:
            if self.rect.colliderect(p): # colliderect é uma função para identificar sobreposições entre formas na tela
                # a ideia é usar para identificar a colisão de superfícies.

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
