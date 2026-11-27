import pygame as pg
from settings import(GRAVIDADE, LARGURA, ALTURA, VEL_MAX_QUEDA, COR_INIMIGO, VEL_INIMIGO)

#classe base para inimigos, servirá como base para variações
class Inimigo:
    def __init__(self, x, y, largura=30, altura=15, vida=1, velocidade=VEL_INIMIGO, cor=COR_INIMIGO):
        self.spawn = pg.Vector2(x, y) #coordenada de spawn
        self.pos = pg.Vector2(x, y) #posição exata
        self.vel = pg.Vector2(0, 0) #vetor de velocidade atual
        self.rect = pg.Rect(x, y, largura, altura) #caixa de hitbox do inimigo

        self.vida = vida #vida do inimigo
        self.vivo = True #booleano pra saber se o inimigo está vivo
        self.velocidade = velocidade #velocidade do inimigo
        self.cor = cor #cor do inimigo

        self.direcao = 1 #sentido horizontal do movimento para a direita
        self.no_chao = False #começa como false pois inimigo pode nascer no ar

        #variáveis mortas, nesse prototipo inicial. Serão usadas futuramente:
        self.estado = 'patrulha' #estado que o inimigo se encontra, definido por uma string
        self.timer = 0.0 #controlar intervalos de tempo do inimigo

    def aplicar_gravidade(self, dt): #função que aplica a gravidade no inimigo
        self.vel.y += GRAVIDADE * dt
        self.vel.y = min(self.vel.y, VEL_MAX_QUEDA)

    def mover_e_colidir(self, dt, solidos, plataformas, colidir_plataformas=True):#função que move e colide o inimigo
        bateu_parede = False

        #eixo x:
        self.pos.x += self.vel.x * dt
        self.rect.x = round(self.pos.x)

#------------------esse bloco vai criar uma parede invisivel caso a camêra vá seguindo o jogador (scrolling pelo mapa)-----------------------
        #remover caso o mapa tenha scrolling
        #definição de limites laterais para o inimigo
        if self.rect.left <= 0: #verificar se inimigo ultrapassou a extremidade esquerda da tela
            self.rect.left = 0 #empurra o inimigo para dentro do limite
            bateu_parede = True #sinaliza que inimigo bateu no limite
        elif self.rect.right >= LARGURA: #mesma coisa só que para a direita, usando a largura importada
            self.rect.right = LARGURA #inimigo dentro do limite
            bateu_parede = True #sinaliza que inimigo bateu no limite
#--------------------------------------------------------------------------------------------------------------------------------------------

        for s in solidos: #verifica colisão com os sólidos
            if self.rect.colliderect(s): #se colidiu com algum sólido
                if self.vel.x > 0: #se estiver indo para a direita
                    self.rect.right = s.left #empurra o inimigo para a esquerda do sólido
                elif self.vel.x < 0: #se estiver indo para a esquerda
                    self.rect.left = s.right #empurra o inimigo para a direita do sólido
                bateu_parede = True #sinaliza que inimigo bateu em um sólido

        self.pos.x = self.rect.x #atualiza a posição exata do inimigo

        #eixo y:
        fundo_antes = self.rect.bottom #guarda a posição do fundo antes da gravidade puxar
        self.pos.y += self.vel.y * dt
        self.rect.y = round(self.pos.y)
        self.no_chao = False #só fica true se encostar no piso, reseta a flag

        for s in solidos: #colisão com blocos sólidos(chão e tetos)
            if self.rect.colliderect(s):
                if self.vel.y > 0: #inimigo caindo
                    self.rect.bottom = s.top #apoia no topo do sólido
                    self.no_chao = True #sinaliza que inimigo está no chão
                elif self.vel.y < 0: #inimigo subindo
                    self.rect.top = s.bottom #empurra o inimigo para baixo do sólido
                self.vel.y = 0 #zera velocidade do inimigo no eixo y
                self.pos.y = self.rect.y #atualiza a posição exata do inimigo

        #implementa a mecanica de plataformas que podem ser atravessadas de baixo para cima e sustentam o inimigo em cima delas
        if colidir_plataformas: 
            for p in plataformas:
                if self.vel.y > 0 and fundo_antes <= p.top and self.rect.colliderect(p): #inimigo caindo, fundo antes da gravidade puxar acima da plataforma e colidiu com a plataforma
                    self.rect.bottom = p.top #apoia no topo da plataforma
                    self.vel.y = 0 #zera velocidade vertical
                    self.pos.y = self.rect.y #atualiza a posição exata do inimigo
                    self.no_chao = True #sinalizando que inimigo está no chão

        return bateu_parede #função retorna se inimigo bateu em algum sólido ou parede invisível, para que a IA do inimigo possa mudar de direção
 