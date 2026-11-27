import pygame as pg
from settings import(GRAVIDADE, LARGURA, ALTURA, VEL_MAX_QUEDA, COR_INIMIGO, VEL_INIMIGO)

#classe base para inimigos, servirá como base para variações
class Inimigo:
    def __init__(self, x, y, largura=20, altura=30, vida=1, velocidade=VEL_INIMIGO, cor=COR_INIMIGO):
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

#==========================================================================================================================================================================================================
#-----------------SENSORES DE IA(FERRAMENTAS QUE AUXILIARÃO NA PERCEPÇÃO DO AMBIENTE/PLAYER)---------------------------------------------------------------------------------------------------------------
##==========================================================================================================================================================================================================
    
    #projeta um pequeno retangulo na frente do inimigo para detectar se há chão
    def sensor_chao(self, solidos, plataformas):
        if self.direcao == 1:
            distancia_relativa = self.rect.width + 2
        else:
            distancia_relativa = -4
        sensor = pg.Rect(self.rect.x + distancia_relativa, self.rect.bottom + 2, 2, 4)
        for s in solidos + plataformas:
            if sensor.colliderect(s):
                return True
        return False

    #retorna a distância entre o inimigo e o centro do alvo (player) usando a fórmula de distância euclidiana
    def distancia_para(self, alvo):
        return pg.Vector2(self.rect.center).distance_to(alvo.rect.center)

    #função útil para atiradores e voadores
    #retorna um vetor unitário apontando na direção do alvo (player)
    def direcao_para(self, alvo):
        vetor = pg.Vector2(alvo.rect.center) - pg.Vector2(self.rect.center)
        if vetor.length() > 0:
            return vetor.normalize()
        else:
            return pg.Vector2(0, 0)

    #função para encarar alvo horizontalmente
    def olhar_para(self, alvo):
        if alvo.rect.centerx > self.rect.centerx:
            self.direcao = 1
        else:
            self.direcao = -1

#===========================================================================================================================
#---------Vida e interface-------------------------------------------------------------------------------------------------
#=========================================================================================================================== 

    #desconta HP e sinaliza morte
    def receber_dano(self, qtd=1):
        self.vida -= qtd
        if self.vida <= 0:
            self.vivo = False

    #detecta se o inimigo caiu em um buraco fora da área jogável
    def fora_da_tela(self):
        return self.rect.top > ALTURA + 200

    #método para implementar subclasses do inimigo
    def update(self, dt, solidos, plataformas, player, projeteis):
        raise NotImplementedError("O método update deve ser implementado nas subclasses de Inimigo.")

    #renderização base, provisória até que seja implementado os sprites
    def draw(self, tela):
        pg.draw.rect(tela, self.cor, self.rect)

#==========================================================================================================================
#----------------Primeira implementação concreta de Inimigo-------------------------------------------------
#=========================================================================================================================

class Patrulheiro(Inimigo):

    def update(self, dt, solidos, plataformas, player, projeteis):
        if self.no_chao and not self.sensor_chao(solidos, plataformas): #se tá pisando no chão e tem chão à frente
            self.direcao *= -1 #inverte a direção do inimigo

        #aplicação da física: define velocidade no eixo x, aplica gravidade e resolve colisões
        self.vel.x = self.direcao * self.velocidade 
        self.aplicar_gravidade(dt)
        bateu = self.mover_e_colidir(dt, solidos, plataformas)

        if bateu:
            self.direcao *= -1 #se bateu também inverte o sentido

        #define interação com o jogador
        #no momento, faz o player respawnar caso colida, pois ainda não possui HP
        if self.rect.colliderect(player.rect):
            player.respawn()
