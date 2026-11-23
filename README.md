# JogodeIP
## V2
foi adicionado uma distinção entre objetos solidos (que não podem ser atravessados de forma alguma)
e plataformas que podem ser atravessaveis quando de lado ou por baixo delas. Basicamente foi um conjunto 
de funções de colliderect() (função que identifica a sobreposição de objetos na tela) da biblioteca pygame 
juntamente com atributos "top" e "bottom" para identificar quando o personagem esta de fato acimada plataforma
e com os pés nela.

Foi implementado a mecânica de descer as plataformas (ESPAÇO + S no teclado).

Correção de bugs de limite do mapa, limite de velocidade horz e vert do personagem.

Correção da mecânica de pulos que antes permitia segurar as teclas de pular para "spammar" os pulos,
agora eles são únitarios ea após um pulo é preciso apertar novamente a tecla para pular, a maneira que isso foi
feito foi a partir da ideia de transição de borda, uma váriavel que identifica quando ocorreu o pulo e se ocorrer
ela se torna True (pode ser false tambem so inverte a lógica) evitando que o player dê outro pulo pois o pulo so é permitido
quando a variável é False e ela so volta a ser False após o player ter "aterrisado".

No mais foi feita uma reorganização da escala principal do jogo e de sintaxe do código pra ficar mais organizado e melhor
de trabalhar.
Estamos trabalhando...
