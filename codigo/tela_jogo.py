from constantes import *  
import motor_grafico as motor 

import random

def desenha_tela(janela, estado, altura_tela, largura_tela):

    motor.preenche_fundo(janela, PRETO)

    inicio_x = (largura_tela//2)-40  #Define centro da tela no eixo x
    inicio_y = (altura_tela//2)-15   #Define centro da tela no eixo y
    
    #faz tela verde no terminal
    for cod_y in range(len(estado['mapa'])):
        for cod_x in range(len(estado['mapa'][cod_y])):
            motor.desenha_string(janela, cod_x+inicio_x, cod_y+inicio_y, estado['mapa'][cod_y][cod_x], VERDE_ESCURO, PRETO)
        
    #Coloca blocos na tela verde
    for blocos in estado['blocos']:
        motor.desenha_string(janela, blocos['posicao'][0]+inicio_x, blocos['posicao'][1]+inicio_y, blocos['tipo'], MARROM_MAIS_ESCURO, blocos['cor'] )
    
    #Coloca monstros na tela verde
    for monstros in estado['monstros']:
        motor.desenha_string(janela, monstros['posicao'][0]+inicio_x, monstros['posicao'][1]+inicio_y, monstros['tipo'], VERDE_ESCURO, monstros['cor'] )
    
    #Coloca coração e espinho na tela verde
    for x in estado['objetos']:
        motor.desenha_string(janela, x['posicao'][0]+inicio_x, x['posicao'][1]+inicio_y, x['tipo'], VERDE_ESCURO, x['cor'] )
    
    #coloca jogador na tela verde
    pos_x = estado['pos_jogador'][0]
    pos_y = estado['pos_jogador'][1]
    motor.desenha_string(janela, pos_x+inicio_x, pos_y+inicio_y, JOGADOR, VERDE_ESCURO, AMARELO)

    #coloca coração encima da tela verde e coloca corações brancos quando perde vida
    var_auxiliar = 0
    for i in range(estado['vidas']):
        motor.desenha_string(janela, inicio_x+i, inicio_y-1, CORACAO,PRETO, VERMELHO)
        var_auxiliar = i

    if estado['vidas']< estado['max_vidas']:
        for i in range(estado['max_vidas']-estado['vidas']):
            motor.desenha_string(janela, inicio_x+var_auxiliar+1, inicio_y-1, CORACAO*(estado['max_vidas']-estado['vidas']),PRETO, BRANCO)
    
    #Desenha o nível atual que o jogador está encima da tela verde
    motor.desenha_string(janela, inicio_x, inicio_y-2, f'LEVEL: {estado['nivel_atual']}', PRETO, BRANCO)

    #Desenha o experiência atual do jogador e a experiência necessária para subir de LEVEL
    motor.desenha_string(janela, inicio_x+10, inicio_y-2, f'EXPERIÊNCIA: {estado['experiencia_jogador']}/{estado['max_experiencia_jogador']}', PRETO, BRANCO)
            
    #coloca mensagem abaixo da tela verde
    motor.desenha_string(janela, inicio_x, inicio_y+30, estado['mensagem'], PRETO, BRANCO )


    motor.mostra_janela(janela)


def atualiza_estado(estado, tecla):
    
    estado['mensagem'] = ''

    #Executa comandos enquanto a quantidade de vida for maior que 0
    if estado['vidas'] != 0:

        movimenta_personagem(estado, tecla)
        recebe_perde_coracao(estado)
        experiencia_jogador(estado)
        
        # Ao apertar a tecla 'i', o jogador deve ver o inventário
        if tecla == 'i':
            estado['tela_atual'] = TELA_INVENTARIO
            
        # Termina o jogo se o jogador apertar ESC ou 'q'
        elif tecla == motor.ESCAPE or tecla =='q':
            estado['tela_atual'] = SAIR

    #Se jogador perder tela de game over aparece       
    else:
        estado['tela_atual'] = TELA_GAME_OVER

#Função que faz o personagem se movimentar
def movimenta_personagem(estado, tecla):

    #Em todo loop o estado de batalha é retornado para False, para que os monstros possam se movimentar
    for monstro_batalha in estado["monstros"]:
        monstro_batalha["em_batalha"] = False

    #movimenta personagem para direita
    if tecla == 'DIREITA':
        estado['pos_jogador'][0] += 1
        if estado['pos_jogador'][0] == 80 or colisao_bloco_personagem(estado) or colisao_monstro_personagem(estado):
            if colisao_monstro_personagem(estado):
                ataca_perde_vida_jogador(estado)
            estado['pos_jogador'][0] -= 1

    #movimento personagem para esquerda
    if tecla == 'ESQUERDA':
        estado['pos_jogador'][0] -= 1
        if estado['pos_jogador'][0] == -1 or colisao_bloco_personagem(estado) or colisao_monstro_personagem(estado):
            if colisao_monstro_personagem(estado):
                ataca_perde_vida_jogador(estado)
            estado['pos_jogador'][0] += 1

    #movimento personagem para cima
    if tecla == 'CIMA':
        estado['pos_jogador'][1] -= 1
        if estado['pos_jogador'][1] == -1 or colisao_bloco_personagem(estado) or colisao_monstro_personagem(estado):
            if colisao_monstro_personagem(estado):
                ataca_perde_vida_jogador(estado)
            estado['pos_jogador'][1] += 1

    #movimento personagem para baixo
    if tecla == 'BAIXO':
        estado['pos_jogador'][1] += 1
        if estado['pos_jogador'][1] == 31 or colisao_bloco_personagem(estado) or colisao_monstro_personagem(estado):
            if colisao_monstro_personagem(estado):
                ataca_perde_vida_jogador(estado)
            estado['pos_jogador'][1] -= 1

    # Movimenta o monstro sem ser o que esta em batalha
    movimenta_monstro(estado)

#Função que faz ganhar coração caso passe pela vida extra e perde coração se passar por espinho
def recebe_perde_coracao(estado):
    #jogador pega vida extra ou é atingido por um espinho
    for coracao_espinho in estado['objetos']:
        if estado['pos_jogador'] == coracao_espinho['posicao'] and coracao_espinho['tipo'] == CORACAO:
            estado['objetos'].remove(coracao_espinho)
            if estado['vidas']<estado['max_vidas']:
                estado['vidas']+=1
                estado['mensagem'] = 'Você pegou uma vida!'
                break
            else:
                estado['mensagem'] = 'Você atingiu o limite máximo de vidas'
                break  
        elif estado['pos_jogador'] == coracao_espinho['posicao'] and coracao_espinho['tipo'] == ESPINHO: 
            estado['vidas']-=1
            estado['mensagem'] = 'Você perdeu uma vida!'
            break

#Função que impede jogador de atravessar blocos
def colisao_bloco_personagem(estado):
    for blocos in estado['blocos']:
        if blocos['tipo'] == PAREDE and estado['pos_jogador'] == blocos['posicao']:
            estado['mensagem'] = 'Você não pode se mover nessa direção'
            return True
    return False

#Função que da dano no monstro ou jogador perde uma vida
def ataca_perde_vida_jogador(estado):
    for monstro in estado['monstros']:
            if estado['pos_jogador'] == monstro['posicao']:
                if random.random()+estado['mult_forca'] < monstro['probabilidade_de_ataque']:
                    estado['vidas']-=1
                    estado['mensagem'] = 'Você perdeu uma vida pelo monstro!'
                else:
                    monstro['vidas']-=1
                    if monstro['vidas']==0:

                        #Vê qual tipo de monstro morreu
                        if monstro['tipo'] == MONSTRO_DIAGONAL:
                            estado['qtd_monstros_d']-=1
                        elif monstro['tipo'] == MONSTRO_VERTICAL:
                            estado['qtd_monstros_v']-=1
                        elif monstro['tipo'] == MONSTRO_HORIZONTAL:
                            estado['qtd_monstros_h']-=1

                        estado['monstros'].remove(monstro)
                        estado['mensagem'] = 'Você matou o monstro'

                    else:
                        estado['mensagem'] = f'Você atacou o monstro, ele agora tem {monstro['vidas']} vidas'

#Função que impede monstro de entrar no bloco
def colisao_bloco_em_monstro(pos_monstro, estado):
    for bloco in estado['blocos']:
        if pos_monstro == bloco['posicao']:
            return True
    return False

#Função que impede que monstro entre no coração ou espinho
def colisao_coracao_espinho_em_monstro(pos_monstro, estado):
    for objeto in estado['objetos']:
        if pos_monstro == objeto['posicao']:
            return True
    return False

#Função que impede que monstro entre em outro monstro
def colisao_monstro_monstro(nova_pos, lista_pos):
    return nova_pos in lista_pos

#Função que impede movimento do jogador no monstro
def colisao_monstro_personagem(estado):
    for monstro in estado['monstros']:
        if estado['pos_jogador'] == monstro['posicao']:
            monstro['em_batalha'] = True
            return True
    return False

#Função auxiliar da colisao_monstro_monstro que faz uma 
# lista das posições dos monstros para que seja possivel identificar quais posições já estao ocupadas
def lista_pos_monstro(estado):
    lista_pos = []
    for monstro in estado['monstros']:
        lista_pos.append(monstro['posicao'])
    lista_pos.append(estado['pos_jogador']) #Coloca posição do personagem na lista para que monstro não entre dentro dele
    return lista_pos

#Função que movimenta monstro
def movimenta_monstro(estado):
    lista_pos = lista_pos_monstro(estado)
    
    for monstro in estado['monstros']:

        if not monstro['em_batalha']:

            lista_pos.remove(monstro['posicao']) #Remove a posição do monstro que está sendo analisado para isso não ser sempre verdade
            nova_pos = monstro['posicao'].copy()

            if monstro['tipo'] == MONSTRO_DIAGONAL:
                nova_pos[0] += random.choice([-1, 1])
                nova_pos[1] += random.choice([-1, 1])

            elif monstro['tipo'] == MONSTRO_VERTICAL:
                nova_pos[1] += random.choice([-1, 1])

            elif monstro['tipo'] == MONSTRO_HORIZONTAL:
                nova_pos[0] += random.choice([-1, 1])
            
            if not colisao_bloco_em_monstro(nova_pos, estado) and not colisao_coracao_espinho_em_monstro(nova_pos, estado) and not colisao_monstro_monstro(nova_pos, lista_pos) and not colisao_monstro_personagem(estado):
                monstro['posicao'] = nova_pos

            lista_pos.append(monstro['posicao']) #Adiciona posição do monstro a lista novamente

#Função que verifica se jogador subiu de nível 
def experiencia_jogador(estado):
    if estado['nivel_atual']<estado['max_nivel']: #Condição que faz o jogador ganhar o jogo

        if estado['qtd_monstros_d'] == 0:      #Monstros que andam na diagonal(d) dão 5 de experiência
            estado['experiencia_jogador'] += 5
            estado['mensagem'] = f'Você ganhou 3 de experiência por matar o monstro, falta {estado['max_experiencia_jogador']-estado['experiencia_jogador']} pontos de experiência para subir de nível'
            estado['qtd_monstros_d'] = 1

        elif estado['qtd_monstros_v'] == 0:    #Monstros que andam na vertical(v) dão 3 de experiência
            estado['experiencia_jogador'] += 3
            estado['mensagem'] = f'Você ganhou 2 de experiência por matar o monstro, falta {estado['max_experiencia_jogador']-estado['experiencia_jogador']} pontos de experiência para subir de nível'
            estado['qtd_monstros_v'] = 1

        elif estado['qtd_monstros_h'] == 0:   #Monstros que andam na horizontal(h) dão 1 de experiência
            estado['experiencia_jogador'] += 1
            estado['mensagem'] = f'Você ganhou 1 de experiência por matar o monstro, falta {estado['max_experiencia_jogador']-estado['experiencia_jogador']} pontos de experiência para subir de nível'
            estado['qtd_monstros_h'] = 1
        
        #Quando jogador atinge a experiência esperada para o LEVEL dele 
        # o número de vidas aumenta ou a probabilidade de atacar o monstro de forma alternada
        if estado['experiencia_jogador']>=estado['max_experiencia_jogador']:   
            if estado['sobe_vida_forca_jogador']%2 == 0:
                estado['vidas'] += 1
                estado['nivel_atual'] +=1
                estado['mensagem'] = f'Você subiu para o nível {estado['nivel_atual']}, agora você tem 1 coração extra'
                estado['max_vidas'] += 1
            else:
                estado['mult_forca'] += 0.1
                estado['nivel_atual'] +=1
                estado['mensagem'] = f'Você subiu para o nível {estado['nivel_atual']}, agora você tem maiores chances de atacar um monstro'
            estado['max_experiencia_jogador'] += 3    #Experiência que o jogador deve acumular para subir de LEVEL no próximo turno
            estado['sobe_vida_forca_jogador'] += 1
    else:
        estado['tela_atual'] = TELA_VENCEDOR
                


                            
            
