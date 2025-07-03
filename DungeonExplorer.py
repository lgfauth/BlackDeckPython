import pyautogui
import time
import logging
import os
import pygetwindow as gw
import cv2
import numpy as np
from Utils import tempo_formatado_em_minutos, selecionar_janela, localizar_imagem
from Consts import CAMINHO_IMAGENS, BTN_PROXIMA_BATALHA, BTN_INICIAR_BATALHA, BTN_PROPAGANDA_INTRUSIVA, DELAY_VERIFICACAO, MAX_ITERATIONS, dungeons

class DungeonExplorer:
    def __init__(self):
        self.config = self.escolher_masmorra()
        self.coords = self.config['coords']
        self.scrolls = self.config['scrolls']
        self.battle_counter = 0
        self.tempo_inicial = time.time()

        wins = gw.getWindowsWithTitle('Black Deck')
        if wins:
            w = wins[0]
            if w.isMinimized:
                w.restore()
            try:
                w.activate()
            except:
                pass
            time.sleep(0.5)
            logging.info(f"Usando janela automática: {w.title}")
            self.area = (w.left, w.top, w.width, w.height)
        else:
            logging.warning('Não encontrou janela automática.')
            self.area = selecionar_janela()

        logging.info(f"Bot iniciado para masmorra: {self.config['name']}")

    def escolher_masmorra(self):
        print("Selecione a masmorra que deseja atacar:")
        for key, val in dungeons.items():
            print(f"  {key} - {val['name']}")
        choice = None
        while choice not in dungeons:
            choice = input("Digite o número da masmorra (1-4): ").strip()
            if choice not in dungeons:
                print("Opção inválida. Tente novamente.")
        config = dungeons[choice]
        logging.info(f"Masmorra selecionada: {config['name']}")
        return config

    def rolar_para_baixo(self, vezes=1):
        largura, altura = pyautogui.size()
        x = 250
        y = altura // 2
        for i in range(vezes):
            logging.info(f'Fazendo scroll {i+1}/{vezes} para exibir níveis…')
            pyautogui.moveTo(x, y)
            pyautogui.mouseDown()
            pyautogui.moveTo(x, y + 550, duration=0.5)
            pyautogui.mouseUp()
            time.sleep(2)

    def verificar_vitoria(self):
        return localizar_imagem(os.path.join(CAMINHO_IMAGENS, BTN_PROXIMA_BATALHA), 0.78, self.area) is not None

    def fechar_propaganda_intrusiva(self):
        caminho_btn = os.path.join(CAMINHO_IMAGENS, BTN_PROPAGANDA_INTRUSIVA)
        pos = localizar_imagem(caminho_btn, 0.78, self.area)
        if pos:
            x_ad, y_ad = pos
            logging.info(f'Propaganda intrusiva detectada em ({x_ad}, {y_ad}), fechando…')
            pyautogui.moveTo(x_ad, y_ad)
            pyautogui.mouseDown()
            pyautogui.mouseUp()
            time.sleep(DELAY_VERIFICACAO)

    def iniciar_bot(self):
        try:
            while True:
                time.sleep(DELAY_VERIFICACAO)
                self.rolar_para_baixo(self.scrolls)

                x_sel, y_sel = self.coords['selecionar_level']
                tentativas = 0

                while True:
                    pyautogui.moveTo(x_sel, y_sel)
                    pyautogui.mouseDown()
                    pyautogui.mouseUp()
                    time.sleep(0.5)

                    found = localizar_imagem(
                        os.path.join(CAMINHO_IMAGENS, BTN_INICIAR_BATALHA),
                        0.78,
                        self.area
                    )

                    if found:
                        logging.info(f'Entrada na masmorra confirmada após clique em ({x_sel}, {y_sel})')
                        break

                    y_sel += 7
                    tentativas += 1
                    logging.info(f'Entrada não confirmada. Ajustando Y para {y_sel} (tentativa {tentativas}/{MAX_ITERATIONS})')

                    if tentativas >= MAX_ITERATIONS:
                        logging.warning(f'Limite de {MAX_ITERATIONS} tentativas atingido. Reiniciando ciclo.')
                        break

                time.sleep(DELAY_VERIFICACAO)
                x_init, y_init = self.coords['iniciar_batalha']
                pyautogui.moveTo(x_init, y_init)
                pyautogui.mouseDown()
                pyautogui.mouseUp()
                self.battle_counter += 1
                logging.info('-------------------- // -------------------- // --------------------')
                logging.info(' ')
                logging.info(f'Batalha {self.battle_counter} iniciada em ({x_init}, {y_init})')
                logging.info(f'Tempo total de execução: {tempo_formatado_em_minutos(self.tempo_inicial)}')
                logging.info(' ')
                logging.info('-------------------- // -------------------- // --------------------')
                time.sleep(DELAY_VERIFICACAO)

                while not self.verificar_vitoria():
                    logging.info('Aguardando vitória...')
                    time.sleep(DELAY_VERIFICACAO)

                self.fechar_propaganda_intrusiva()

                logging.info('Preparando próxima fase...')
                time.sleep(DELAY_VERIFICACAO)
                x_phase, y_phase = self.coords['proxima_fase']
                pyautogui.moveTo(x_phase, y_phase)
                pyautogui.mouseDown()
                pyautogui.mouseUp()
                logging.info(f'Clicado em Iniciar Fase em ({x_phase}, {y_phase})')
                time.sleep(DELAY_VERIFICACAO)
        except KeyboardInterrupt:
            logging.info('Bot finalizado manualmente.')
            time.sleep(1)
            self.voltar_menu()

    def voltar_menu(self):
        logging.info("Retornando ao menu principal...")
        from Menu import menu_principal
        menu_principal()
        return

def executar_dungeon_explorer():
    bot = DungeonExplorer()
    bot.iniciar_bot()

if __name__ == '__main__':
    executar_dungeon_explorer()
