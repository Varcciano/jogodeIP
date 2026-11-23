import pygame as pg
from settings import (COR_PLAYER, GRAVIDADE, VEL_PULO, LARGURA, ALTURA, VEL_MAX_QUEDA,
                      TEMPO_DESCER, VEL_DESCER)

class Player:
    def __init__(self, x, y):
        self.spawn = pg.Vector2(x, y) # coordenada de spawn para ser feito o respawn quando necessario.
        self.rect = pg.Rect(x, y, 20, 35) # (retângulo) corpo prótotipo do player para colisão e para referencial. 
        self.pos = pg.Vector2(x, y) # vai ser usado para posição e representa a posição atual
        self.vel = pg.Vector2(0, 0) # vai ser usado para velocidade e representa a velocidade atual
        self.velocidade = 150
        self.no_chao = False # identificar pulo ou n
        self.na_plataforma = False # vai se tornar verdadeiro quando o objeto for atravessável
        self.tempo_descer = 0
        self.pulo_antes = False
        self.w_antes = False
        
    def update(self, dt, solidos, plataformas):
        # teclas
        teclas = pg.key.get_pressed() # identificar pressionamento de tecla e qual tecla foi apertada
        esq = teclas[pg.K_a] or teclas[pg.K_LEFT]
        dir = teclas[pg.K_d] or teclas[pg.K_RIGHT]
        baixo = teclas[pg.K_s] or teclas[pg.K_DOWN]
        espaco = teclas[pg.K_SPACE]
        w = teclas[pg.K_w]

        espaco_apertou = espaco and not self.pulo_antes
        w_apertou = w and not self.w_antes
        self.pulo_antes = espaco
        self.w_antes = w

        descer = baixo and espaco_apertou
        pulo = (espaco_apertou and not baixo) or w_apertou
        # ========================================
        # velocidade na horizontal (esquerda ou direita)
        self.vel.x = (dir - esq) * self.velocidade
        if self.tempo_descer > 0:
            self.tempo_descer -= dt

        if descer and self.no_chao and self.na_plataforma:
            self.tempo_descer = TEMPO_DESCER
            self.vel.y = VEL_DESCER
            self.no_chao = False
        
        # mecanica de pulo
        if pulo and self.no_chao:
            self.vel.y = VEL_PULO

        # mecanica de gravidade pra o personagem voltar ao chão.
        self.vel.y += GRAVIDADE * dt
        self.vel.y = min(self.vel.y, VEL_MAX_QUEDA) # limite de velocidade na queda do player

        # toda ideia de mudança de posição partem de uma mesma premissa:
        # primeiro a velocidade altera conforme aperto da tecla de movimento.
        # segundo a posição é incrementada pela velocidade "60 vezes por segundo"
        # terceiro a posição é arredondada e atualiza a coordenada do retângulo na tela "60 vezes por segundo"
        
        # movimento na coordenada x, e colisões em sólidos no eixo x
        self.pos.x += self.vel.x * dt
        self.pos.x = max(0, min(self.pos.x, LARGURA - self.rect.width)) # evita que o retangulo saia do escopo da tela.
        self.rect.x = round(self.pos.x)
        for s in solidos:
            if self.rect.colliderect(s): # colliderect é uma função para identificar sobreposições entre formas na tela
                # a ideia é usar para identificar a colisão de superfícies.

                if self.vel.x > 0:
                    self.rect.right = s.left
                elif self.vel.x < 0:
                    self.rect.left = s.right
                self.pos.x = self.rect.x

        # movimentos na coordenada y, colisões em solidos no eixo y e plataformas
        fundo_antes = self.rect.bottom
        self.pos.y += self.vel.y * dt
        self.rect.y = round(self.pos.y)

        for s in solidos:
            if self.rect.colliderect(s):
                if self.vel.y > 0:
                    self.rect.bottom = s.top
                elif self.vel.y < 0:
                    self.rect.top = s.bottom
                self.vel.y = 0
                self.pos.y = self.rect.y

        for p in plataformas:
            if (self.vel.y > 0 and self.tempo_descer <= 0 and fundo_antes <=  p.top and self.rect.colliderect(p)):
                self.rect.bottom = p.top
                self.vel.y = 0
                self.pos.y = self.rect.y

        apoio = self._apoio(solidos, plataformas)
        self.no_chao = apoio is not None and self.vel.y >= 0
        self.na_plataforma = (apoio == "plataforma")

        if self.rect.top > ALTURA + 200:
            self.respawn()
        
        if self.no_chao:
            self.vel.y = 0
            self.pos.y = self.rect.y

    def _apoio(self, solidos, plataformas):
        sensor = self.rect.move(0, 1)
        for s in solidos:
            if sensor.colliderect(s):
                return "solido"
        if self.tempo_descer <= 0:
            for p in plataformas:
                if sensor.colliderect(p) and self.rect.bottom <= p.top:
                    return "plataforma"
        return None

    def respawn(self):
        self.pos.update(self.spawn)
        self.rect.topleft = (round(self.pos.x), round(self.pos.y))
        self.vel.update(0, 0)
        self.tempo_descer = 0

    # desenha os elementos postos no player e seus atributos na tela
    def draw(self, tela):
        pg.draw.rect(tela, COR_PLAYER, self.rect)
