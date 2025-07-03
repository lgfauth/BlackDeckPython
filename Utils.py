import pyautogui
import time
import logging
import os
import pygetwindow as gw
import cv2
import numpy as np
import time

TEMPO_INICIAL = time.time()

def tempo_formatado_em_minutos(tempo_inicial):
    segundos = int(time.time() - tempo_inicial)
    if segundos < 60:
        return "1 minuto"
    minutos = segundos // 60
    if minutos < 60:
        return f"{minutos} minutos"
    horas = minutos // 60
    minutos_restantes = minutos % 60
    return f"{horas}h {minutos_restantes}min"

def selecionar_janela():
    janelas = gw.getAllTitles()
    print("Selecione a janela desejada:")
    janelas_validas = [j for j in janelas if j.strip()]
    for i, nome in enumerate(janelas_validas):
        print(f"{i + 1}. {nome}")
    while True:
        try:
            idx = int(input("Digite o número da janela: ")) - 1
            if 0 <= idx < len(janelas_validas):
                win = gw.getWindowsWithTitle(janelas_validas[idx])[0]
                if win.isMinimized:
                    win.restore()
                try:
                    win.activate()
                except:
                    pass
                time.sleep(0.5)
                return (win.left, win.top, win.width, win.height)
        except ValueError:
            print("Entrada inválida. Tente novamente.")

def capturar_tela(area=None):
    img = pyautogui.screenshot(region=area)
    return cv2.cvtColor(np.array(img), cv2.COLOR_RGB2BGR)

def localizar_imagem(caminho_img, precisao=0.8, area=None):
    if not os.path.isfile(caminho_img):
        logging.warning(f"Imagem não encontrada: {caminho_img}")
        return None
    tela = capturar_tela(area)
    tpl = cv2.imread(caminho_img)
    if tpl is None:
        logging.warning(f"Erro ao carregar imagem: {caminho_img}")
        return None
    res = cv2.matchTemplate(tela, tpl, cv2.TM_CCOEFF_NORMED)
    loc = np.where(res >= precisao)
    for pt in zip(*loc[::-1]):
        h, w = tpl.shape[:2]
        cx = pt[0] + w // 2 + (area[0] if area else 0)
        cy = pt[1] + h // 2 + (area[1] if area else 0)
        return (cx, cy)
    return None
