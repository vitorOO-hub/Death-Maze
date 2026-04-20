import motor_grafico
import tela_inventario
import tela_jogo
import tela_inicial
import tela_instruções
import tela_game_over
import tela_vencedor
from constantes import SAIR, TELA_INVENTARIO, TELA_JOGO, TELA_INICIAL, TELA_INSTRUCOES, TELA_GAME_OVER, TELA_VENCEDOR
from inicializacao import inicializa_estado


def jogo(janela, altura_tela, largura_tela):
    estado = inicializa_estado()

    while estado['tela_atual'] != SAIR:

        if estado['tela_atual'] == TELA_INICIAL:
            tela_inicial.desenha_tela(janela, estado, altura_tela, largura_tela)
            tecla_apertada = motor_grafico.pega_tecla_apertada(janela)
            tela_inicial.atualiza_estado(estado, tecla_apertada)

        elif estado['tela_atual'] == TELA_INSTRUCOES:
            tela_instruções.desenha_tela(janela, estado, altura_tela, largura_tela)
            tecla_apertada = motor_grafico.pega_tecla_apertada(janela)
            tela_instruções.atualiza_estado(estado, tecla_apertada)

        elif estado['tela_atual'] == TELA_JOGO:
            tela_jogo.desenha_tela(janela, estado, altura_tela, largura_tela)
            tecla_apertada = motor_grafico.pega_tecla_apertada(janela)
            tela_jogo.atualiza_estado(estado, tecla_apertada)
        
        elif estado['tela_atual'] == TELA_INVENTARIO:
            tela_inventario.desenha_tela(janela, estado, altura_tela, largura_tela)
            tecla_apertada = motor_grafico.pega_tecla_apertada(janela)
            tela_inventario.atualiza_estado(estado, tecla_apertada)

        elif estado['tela_atual'] == TELA_GAME_OVER:
            tela_game_over.desenha_tela(janela, estado, altura_tela, largura_tela)
            tecla_apertada = motor_grafico.pega_tecla_apertada(janela)
            tela_game_over.atualiza_estado(estado, tecla_apertada)
        
        elif estado['tela_atual'] == TELA_VENCEDOR:
            tela_vencedor.desenha_tela(janela, estado, altura_tela, largura_tela)
            tecla_apertada = motor_grafico.pega_tecla_apertada(janela)
            tela_vencedor.atualiza_estado(estado, tecla_apertada)

motor_grafico.chama_funcao_jogo(jogo)
