from constantes import *  # Você pode usar as constantes definidas em constantes.py, se achar útil
                          # Por exemplo, usar a constante CORACAO é o mesmo que colocar a string '❤'
                          # diretamente no código
import motor_grafico as motor  # Utilize as funções do arquivo motor_grafico.py para desenhar na tela
                               # Por exemplo: motor.preenche_fundo(janela, [0, 0, 0]) preenche o fundo de preto

def desenha_tela(janela, estado,  altura_tela, largura_tela):
    motor.preenche_fundo(janela, VERMELHO)
    
    inicio_primeiro_caracter_x = (largura_tela//2)-50 #Define centro da tela no eixo x
    
    #Coloca frase da tela inicial na tela
    for caracter in estado['frase_tela_inicial']:
        motor.desenha_string(janela, caracter['posicao'][0]+inicio_primeiro_caracter_x, caracter['posicao'][1], caracter['tipo'], PRETO, caracter['cor'] )
    motor.mostra_janela(janela)

def atualiza_estado(estado, tecla):
    if tecla == 'ESPACO':
        estado['tela_atual'] = TELA_INSTRUCOES
    elif tecla == motor.ESCAPE:
        estado['tela_atual'] = SAIR