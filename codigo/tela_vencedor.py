from constantes import *  
import motor_grafico as motor  

def desenha_tela(janela, estado, altura_tela, largura_tela):
    motor.preenche_fundo(janela, VERMELHO)
    
    inicio_primeiro_caracter_x = (largura_tela//2)-55 #Define centro da tela no eixo x
    inicio_primeiro_caracter_y = (altura_tela//2)-15  #Define centro da tela no eixo y
    
    #Coloca frase da tela inicial na tela
    for caracter in estado['frase_tela_vencedor']:
        motor.desenha_string(janela, caracter['posicao'][0]+inicio_primeiro_caracter_x, caracter['posicao'][1]+inicio_primeiro_caracter_y, caracter['tipo'], PRETO, caracter['cor'] )
    motor.mostra_janela(janela)

def atualiza_estado(estado, tecla):
    if tecla == 'ESPACO':
        estado['tela_atual'] = SAIR
