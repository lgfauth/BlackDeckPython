import time
from Utils import tempo_formatado_em_minutos, selecionar_janela
from Consts import *
import pyautogui
import pygetwindow as gw
import os
import cv2
import numpy as np
import logging

# Desativa o fail-safe padrão do pyautogui
pyautogui.FAILSAFE = False

# Coordenada de emergência para parar o bot manualmente
STOP_X, STOP_Y = 0, 0  # canto superior esquerdo

class EnergyFarmer:
    def __init__(self):
        global CONTADOR_ENERGIA
        
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

        x, y, w_, h_ = self.area
        self.close_region = (x, y + CLOSE_Y_OFFSET, w_, h_ - CLOSE_Y_OFFSET)

        self.templates = {}
        for fn in sorted(os.listdir(CAMINHO_IMAGENS)):
            if fn.lower().endswith('.png'):
                path = os.path.join(CAMINHO_IMAGENS, fn)
                img = cv2.imread(path)
                if img is not None:
                    h, w = img.shape[:2]
                    self.templates[fn] = (img, w, h)
                else:
                    logging.warning(f"Falha ao carregar template {fn}")

        self.close_templates = sorted(
            [fn for fn in self.templates if any(fn.startswith(pref) for pref in TEMPLATE_PREFIXES)],
            key=lambda f: (TEMPLATE_PREFIXES.index(f.split('_')[0] + '_'), int(f.split('_')[1].split('.')[0]))
        )
        self.close_index = 0

    def _capturar(self):
        img = pyautogui.screenshot(region=self.area)
        return cv2.cvtColor(np.array(img), cv2.COLOR_RGB2BGR)

    def _capturar_region(self, region):
        img = pyautogui.screenshot(region=region)
        return cv2.cvtColor(np.array(img), cv2.COLOR_RGB2BGR)

    def localizar(self, nome, precisao=PRECISAO):
        if nome not in self.templates:
            logging.debug(f"Template '{nome}' não carregado")
            return None
        tpl, tw, th = self.templates[nome]
        tela = self._capturar()
        res = cv2.matchTemplate(tela, tpl, cv2.TM_CCOEFF_NORMED)
        pts = list(zip(*np.where(res >= precisao)[::-1]))
        if pts:
            logging.debug(f"Template '{nome}' encontrado em {pts[0]}")
            return pts[0]
        logging.debug(f"Template '{nome}' não correspondeu")
        return None

    def clicar(self, nome):
        pt = self.localizar(nome)
        if not pt:
            return False
        x_, y_ = pt; tw, th = self.templates[nome][1:]
        cx = x_ + tw//2 + self.area[0]
        cy = y_ + th//2 + self.area[1]
        logging.debug(f"Clicando em '{nome}' em ({cx},{cy})")
        pyautogui.moveTo(cx, cy, duration=0.2)
        pyautogui.mouseDown()
        pyautogui.mouseUp()
        return True

    def navegar(self):
        global CONTADOR_ENERGIA

        if self.localizar(INDICADOR_AUTOBATTLE):
            logging.info('Tela pré-batalha detectada, clicando para voltar à tela principal...')
            self.clicar(INDICADOR_AUTOBATTLE)
            time.sleep(1)

        logging.info('Ciclo navegação: Loja')
        self.clicar(BTN_LOJA)
        time.sleep(0.5)
        logging.info('Ciclo navegação: Obter')
        if not self.localizar(BTN_OBTER):
            logging.warning("Botão 'Obter' não encontrado após abrir Loja. Reiniciando ciclo.")
            return False
        self.clicar(BTN_OBTER)
        time.sleep(DELAY_PADRAO)
        if self.localizar(INDICADOR_AUTOBATTLE):
            logging.info('Auto-battle presente: reiniciando ciclo')
            return False
        logging.info('Auto-battle ausente: iniciando fechamento')
        return True

    def fechar_propaganda(self):
        global CONTADOR_ENERGIA

        logging.info(f'Propaganda detectada: aguardando {AD_START_DELAY}s')
        time.sleep(AD_START_DELAY)
        inicio = time.time()
        count = len(self.close_templates)
        self.close_index = 0
        while time.time() - inicio < AD_TIMEOUT:
            mouse_x, mouse_y = pyautogui.position()
            if mouse_x == STOP_X and mouse_y == STOP_Y:
                logging.info("Interrupção manual detectada via posição do mouse. Retornando ao menu principal...")
                self.voltar_menu()
                return

            frame = self._capturar_region(self.close_region)
            if self.close_index >= count:
                self.close_index = 0
            fn = self.close_templates[self.close_index]
            logging.debug(f"Testando template '{fn}' para fechar popup")
            tpl, tw, th = self.templates[fn]
            res = cv2.matchTemplate(frame, tpl, cv2.TM_CCOEFF_NORMED)
            pts = list(zip(*np.where(res >= PRECISAO)[::-1]))
            if pts:
                px, py = pts[0]
                abs_x = px + tw//2 + self.close_region[0]
                abs_y = py + th//2 + self.close_region[1]
                logging.info(f"Clique em '{fn}' em ({abs_x},{abs_y})")
                pyautogui.moveTo(abs_x, abs_y, duration=0.2)
                pyautogui.mouseDown()
                pyautogui.mouseUp()
                time.sleep(0.5)

                if self.localizar(INDICADOR_AUTOBATTLE):
                    self.clicar(INDICADOR_AUTOBATTLE)
                if self.localizar(INDICADOR_AUTOBATTLE) or self.localizar(PRE_BATALHA):
                    tempo_gasto = int(time.time() - inicio)
                    CONTADOR_ENERGIA += 10
                    logging.info(f'-------------------- // -------------------- // --------------------')
                    logging.info(' ')
                    logging.info(f'Propaganda encerrada com sucesso em {tempo_gasto} segundos.')
                    logging.info(f'Energia total arrecadado: {CONTADOR_ENERGIA}')
                    logging.info(f'Tempo total de execução: {tempo_formatado_em_minutos(self.tempo_inicial)}')
                    logging.info(' ')
                    logging.info(f'-------------------- // -------------------- // --------------------')
                    time.sleep(DELAY_PADRAO)
                    return
            self.close_index += 1
        logging.info(f'Timeout de {AD_TIMEOUT}s atingido: retornando ao ciclo')

    def voltar_menu(self):
        logging.info("Retornando ao menu principal...")
        from Menu import menu_principal
        menu_principal()
        return

def executar_energy_farm():
    bot = EnergyFarmer()
    try:
        while True:
            if bot.navegar():
                bot.fechar_propaganda()
    except KeyboardInterrupt:
        logging.info('Bot encerrado manualmente')
