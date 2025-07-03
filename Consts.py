import os
import sys

BASE_PATH = getattr(sys, '_MEIPASS', os.path.abspath("."))
CAMINHO_IMAGENS = os.path.join(BASE_PATH, 'imgs')

BTN_LOJA = 'btn_loja.png'
BTN_OBTER = 'btn_obter.png'
INDICADOR_AUTOBATTLE = 'auto_batalha.png'
PRE_BATALHA = 'auto_battle.png'
BTN_PROXIMA_BATALHA = 'btn_proxima_batalha.png'
BTN_INICIAR_BATALHA = 'btn_iniciar_batalha.png'
BTN_PROPAGANDA_INTRUSIVA = 'propaganda.png'

TEMPLATE_PREFIXES = ['close_', 'cross_', 'avancar_']

MAX_ITERATIONS = 15
CLOSE_Y_OFFSET = 45
PRECISAO = 0.8
DELAY_PADRAO = 2
DELAY_VERIFICACAO = 1
AD_START_DELAY = 5
AD_TIMEOUT = 150

CONTADOR_ENERGIA = 0



# Parâmetros para cada masmorra (4 opções)
dungeons = {
    '1': {
        'name': 'Vórtice Abismal',
        'scrolls': 2,                         # número de rolagens necessárias para a surigr o nível 25 da masmorra selecionada
        'coords': {
            'selecionar_level': (500, 1305),  # ponto base para clicar nível, na seleção de nível da masmorra
            'iniciar_batalha': (670, 1960),   # ponto para clicar no botão iniciar batalha da fase selecionada
            'proxima_fase': (955, 1830)       # ponto para clicar no botão próxima fase após vitória
        }
    },
    '2': {
        'name': 'Caverna dos Goblins',
        'scrolls': 2,
        'coords': {
            'selecionar_level': (500, 875),
            'iniciar_batalha': (670, 1960),
            'proxima_fase': (955, 1830)
        }
    },
    '3': {
        'name': 'Covil do Dragão',
        'scrolls': 2,
        'coords': {
            'selecionar_level': (520, 1095),
            'iniciar_batalha': (670, 1960),
            'proxima_fase': (955, 1830)
        }
    },
    '4': {
        'name': 'Capturas de Cristal',
        'scrolls': 0,
        'coords': {
            'selecionar_level': (650, 1780),
            'iniciar_batalha': (670, 1960),
            'proxima_fase': (955, 1830)
        }
    }
}