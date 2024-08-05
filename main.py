# coding: latin-1
# -*- coding: utf-8 -*-
import pyautogui
import pyperclip
import time
import datetime
import logging
import requests

#Hora_actual
hora_actual = datetime.datetime.now().strftime("%I:%M:%p")
print(hora_actual)


# LOGS
logging.basicConfig(
    filename='Hola.log',
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

# TELEGRAM BOT
TELEGRAM_BOT_TOKEN = '6232135002:AAGPl356BEAbpzSQlgomBQi45YBUZJk136Q'
TELEGRAM_CHAT_ID = '7411433556'
def mensaje_telegram(mensaje):
    url = f'https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage'
    data = {'chat_id': TELEGRAM_CHAT_ID, 'text': mensaje}
    response = requests.post(url, data=data)
    if response.status_code == 200:
        logging.info("Mensaje enviado a Telegram.")
    else:
        logging.error("Error al enviar mensaje a Telegram:", response.text)        

def iniciar_proceso():
    try:
        # ABRIR NAVEGADOR
        logging.info('')
        mensaje_telegram('SE INICIA PROCESO')
        pyautogui.hotkey('win', 'r')
        time.sleep(2)
        pyautogui.write('chrome --start-maximized', interval=0.1)
        time.sleep(2)
        pyautogui.press('enter')

        # INGRESAR A CENSEL  
        time.sleep(2)
        pyautogui.write("http://161.10.252.131:8080/", interval=0.1)
        time.sleep(1)
        pyautogui.press('enter')
        time.sleep(2)

        # INICIAR SESION
        pyperclip.copy('@')
        pyautogui.hotkey('tab')
        pyautogui.write('oscartorres', interval=0.1)
        time.sleep(2)
        # pegar el @
        pyautogui.hotkey('ctrl', 'v')
        time.sleep(2)
        pyautogui.write('consuerte.com', interval=0.1)
        pyautogui.hotkey('tab')
        time.sleep(2)
        pyautogui.write('Oscar1007420377', interval=0.1)
        time.sleep(2)
        pyautogui.hotkey('tab')
        pyautogui.press('enter')

        # INGRESAR A REPORTES WEB
        time.sleep(3)
        pyautogui.press('tab')
        time.sleep(2)
        pyautogui.press('enter')
        time.sleep(4)
    except Exception as error: 
        print(' No se pudo inicar sesion: ')
    finally:
        logging.info('Se ingreso la censel correctamente')    
        
#iniciar_proceso()