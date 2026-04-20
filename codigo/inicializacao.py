from random import randint

from constantes import *  # Você pode usar as constantes definidas em constantes.py, se achar útil
                          # Por exemplo, usar a constante CORACAO é o mesmo que colocar a string '❤'
                          # diretamente no código


def gera_posicao_desocupada(posicoes_ocupadas, largura_mapa, altura_mapa):
    
    x = randint(1, largura_mapa-2)
    y = randint(1, altura_mapa-2)
    
    if [x,y] not in posicoes_ocupadas:
        posicoes_ocupadas.append([x, y])
        return [x, y]
    else:
        return gera_posicao_desocupada(posicoes_ocupadas, largura_mapa, altura_mapa)


def gera_objetos(quantidade, tipo, cor, largura_mapa, altura_mapa, posicoes_ocupadas):

    objetos = []
    if tipo == MONSTRO_DIAGONAL:
        for i in range(quantidade):
            posicao = gera_posicao_desocupada(posicoes_ocupadas, largura_mapa, altura_mapa)
            objetos.append({
                'tipo': tipo,
                'posicao': posicao,
                'cor': cor,
                'em_batalha': False,
                'vidas': 5,
                'probabilidade_de_ataque': 0.6
            })
    elif tipo == MONSTRO_VERTICAL:
        for i in range(quantidade):
            posicao = gera_posicao_desocupada(posicoes_ocupadas, largura_mapa, altura_mapa)
            objetos.append({
                'tipo': tipo,
                'posicao': posicao,
                'cor': cor,
                'em_batalha': False,
                'vidas': 3,
                'probabilidade_de_ataque': 0.45
            })
    elif tipo == MONSTRO_HORIZONTAL:
        for i in range(quantidade):
            posicao = gera_posicao_desocupada(posicoes_ocupadas, largura_mapa, altura_mapa)
            objetos.append({
                'tipo': tipo,
                'posicao': posicao,
                'cor': cor,
                'em_batalha': False,
                'vidas': 1,
                'probabilidade_de_ataque': 0.2
            })
    else:
        for i in range(quantidade):
            posicao = gera_posicao_desocupada(posicoes_ocupadas, largura_mapa, altura_mapa)
            objetos.append({
                'tipo': tipo,
                'posicao': posicao,
                'cor': cor,
            })
    
    return objetos


def inicializa_estado():
    # Cria lista de listas, cada uma com 50 espaços em branco
    # Você pode mudar esta lista, inclusive seu tamanho, à vontade
    mapa = [
        [' '] * 80,
        [' '] * 80,
        [' '] * 80,
        [' '] * 80,
        [' '] * 80,
        [' '] * 80,
        [' '] * 80,
        [' '] * 80,
        [' '] * 80,
        [' '] * 80,
        [' '] * 80,
        [' '] * 80,
        [' '] * 80,
        [' '] * 80,
        [' '] * 80,
        [' '] * 80,
        [' '] * 80,
        [' '] * 80,
        [' '] * 80,
        [' '] * 80,
        [' '] * 80,
        [' '] * 80,
        [' '] * 80,
        [' '] * 80,
        [' '] * 80,
        [' '] * 80,
        [' '] * 80,
        [' '] * 80,
        [' '] * 80,
        [' '] * 80
    ]
    
    
    largura_mapa = len(mapa[0])
    altura_mapa = len(mapa)
    
    # Você pode colocar o jogador em outro lugar, se preferir
    pos_jogador = [largura_mapa//2, altura_mapa//2]  # Meio do mapa
    
    posicoes_ocupadas = [pos_jogador]

    #Desenha nome do jogo na tela
    frase_tela_inicial = []
    with open('frases_telas/tela_inicial.txt', 'r') as frase:
        conteudo = frase.read()
        frase = conteudo.split('\n')
        for y in range(len(frase)):
            for x in range(len(frase[y])):
                if frase[y][x] == '#':
                    frase_tela_inicial.append({
                        'tipo': CARACTER,
                        'posicao': [x, y],
                        'cor': PRETO
                    })

    #Desenha instruções do jogo na tela
    frase_tela_instrucoes = []
    with open('frases_telas/tela_instruções.txt', 'r') as frase:
        conteudo = frase.read()
        frase = conteudo.split('\n')
        for y in range(len(frase)):
            for x in range(len(frase[y])):
                if frase[y][x] == '#':
                    frase_tela_instrucoes.append({
                        'tipo': CARACTER,
                        'posicao': [x, y],
                        'cor': PRETO
                    })
    
    #Desenha instruções do jogo na tela
    frase_tela_game_over = []
    with open('frases_telas/tela_game_over.txt', 'r') as frase:
        conteudo = frase.read()
        frase = conteudo.split('\n')
        for y in range(len(frase)):
            for x in range(len(frase[y])):
                if frase[y][x] == '#':
                    frase_tela_game_over.append({
                        'tipo': CARACTER,
                        'posicao': [x, y],
                        'cor': PRETO
                    })

    #Desenha instruções do jogo na tela
    frase_tela_vencedor = []
    with open('frases_telas/tela_vencedor.txt', 'r') as frase:
        conteudo = frase.read()
        frase = conteudo.split('\n')
        for y in range(len(frase)):
            for x in range(len(frase[y])):
                if frase[y][x] == '#':
                    frase_tela_vencedor.append({
                        'tipo': CARACTER,
                        'posicao': [x, y],
                        'cor': PRETO
                    })

    #Le arquivo do mapa_blocos e adiciona esses blocos na lista criada(blocos_colocados)
    blocos_colocados = []
    with open('frases_telas/mapa.txt', 'r') as mapa:
        conteudo = mapa.read()
        mapa = conteudo.split('\n')
        for y in range(len(mapa)):
            for x in range(len(mapa[y])):
                if [x, y] not in posicoes_ocupadas:
                    if mapa[y][x] == '#':
                        blocos_colocados.append({
                        'tipo': PAREDE,
                        'posicao': [x,y],
                        'cor': MARROM_ESCURO,
                        })
                        posicoes_ocupadas.append([x,y])
    
    #Cria coração e espinho                    
    objetos = []
    objetos += gera_objetos(15, CORACAO, VERMELHO, largura_mapa, altura_mapa, posicoes_ocupadas)
    objetos += gera_objetos(10, ESPINHO, VERDE_CLARO, largura_mapa, altura_mapa, posicoes_ocupadas)
    
    #Cria monstros
    monstros = []
    monstros += gera_objetos(8, MONSTRO_DIAGONAL, AZUL, largura_mapa, altura_mapa, posicoes_ocupadas) 
    monstros += gera_objetos(8, MONSTRO_VERTICAL, VERMELHO, largura_mapa, altura_mapa, posicoes_ocupadas) 
    monstros += gera_objetos(8, MONSTRO_HORIZONTAL, LARANJA, largura_mapa, altura_mapa, posicoes_ocupadas)

    return {
    'tela_atual': TELA_INICIAL,
    'pos_jogador': pos_jogador,
    'vidas': 5,  # Quantidade atual de vidas do jogador - ele pode perder vidas ao colidir com espinhos ou ganhar vidas ao pegar corações
    'max_vidas': 5,  # Quantidade máxima de vidas que o jogador pode ter - o valor da chave 'vidas' nunca pode ser maior que o valor da chave 'max_vidas'
    'experiencia_jogador': 0, #Experiência atual jogador
    'max_experiencia_jogador': 1, #Máximo experência que jogador pode alcançar a cada turno
    'sobe_vida_forca_jogador': 0, #Aumenta max_vidas ou probabilidade de jogador atacar monstro de forma intercalada
    'mult_forca': 0, #Multiplicador de força do jogador usado na função ataca_perde_vida_jogador
    'nivel_atual': 0,
    'max_nivel': 5, #Nível necessário para jogador ganhar o jogo
    'objetos': objetos,
    'mapa': mapa,
    'blocos': blocos_colocados,
    'frase_tela_inicial': frase_tela_inicial, #Lista de dícionários que escreve Death Maze (nome do jogo)
    'frase_tela_instruções': frase_tela_instrucoes, #Lista de dícionários que escreve as instruções das teclas do jogo
    'frase_tela_game_over': frase_tela_game_over, #Lista de dícionários que escreve GAME OVER!
    'frase_tela_vencedor': frase_tela_vencedor,
    'monstros': monstros,
    'qtd_monstros_d': 1, #Chave que auxilia na visualização de quanto experiência o jogador vai receber por matar um monstro que anda na diagonal
    'qtd_monstros_v': 1, #Chave que auxilia na visualização de quanto experiência o jogador vai receber por matar um monstro que anda na diagonal 
    'qtd_monstros_h': 1, #Chave que auxilia na visualização de quanto experiência o jogador vai receber por matar um monstro que anda na diagonal
    'mensagem': 'JOGO INICIADO! ALCANCE O NÍVEL 5 PARA GANHAR O JOGO',  # Use esta mensagem para mostrar mensagens ao jogador, como "Você perdeu uma vida" ou "Você ganhou uma vida"
}


