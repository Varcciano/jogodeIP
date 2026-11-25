"""
Aqui serão dispostas todas as constantes que seram utilizadas para funcionamento do jogo
desde proporções até quantidade ou intensidades, ou IDs de cores, enfim tudo o que a gente quer que seja
por padrão uma quantidade x, a gente põe aqui e importa para os outros arquivos principalemente o de player.py
e de inimigos.py.
"""
# Proporções de tela e FPS do game
ESCALA = 1
LARGURA = 480
ALTURA = 270
FPS = 60
#

# Cor do player e da tela de fundo. 
COR_FUNDO = (20, 25, 35)
COR_PLAYER = (0, 200, 255)
COR_CHAO = (60, 80, 110)
COR_PLATAFORMA = (90, 130, 160)
#

# Física do game
GRAVIDADE = 900
VEL_PULO = -325
VEL_MAX_QUEDA = 500
TEMPO_DESCER = 0.2
VEL_DESCER = 75

# Colecionáveis
TAM_COLETAVEL = 8          # tamanho (px) do quadradinho do item (moeda)
COR_SUCATA = (255, 200, 60) # cor amarela para a moeda
VALOR_SUCATA = 1           # quanto cada sucata (moeda) vale