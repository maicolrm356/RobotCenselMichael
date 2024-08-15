import pyautogui
import time
from config import *
from main import obtener_captura_pantalla

horarios_procesos = [('baterias', '10:15 AM'), ('baterias', '10:16 AM'), ('intrusion', '8:05 AM'), ('fallo_test', '8:10 AM'), ('panico', '8:15 AM')]

def recorrer_formulario_filtrar():
    hola = '5:53 PM'
    pyautogui.press('tab')
    pyautogui.write(mes_y_ano, interval=0.1)
    time.sleep(1)
    pyautogui.press('tab')
    pyautogui.press('tab')
    #iniciar_formulario()
    print("hOLA")
    for nombre_proceso, horario in horarios_procesos:
    # PROCESo
        if  horario == hora_actual:
            ruta_captura = obtener_captura_pantalla('filtrando_proceso.png', 'screenshots')
            print(ruta_captura)
            