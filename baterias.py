# coding: latin-1
# -*- coding: utf-8 -*-
import pyautogui
import pyperclip
import time
import logging
import requests
import telebot
from config import TELEGRAM_TOKEN
from config import logging
    

# TELEGRAM BOT  

bot = telebot.TeleBot(TELEGRAM_TOKEN) 

def enviar_mensaje_telegram(mensaje):
    TELEGRAM_BOT_TOKEN = '6869640482:AAGA8NqVWAScgGuZap-flJ10LT3ht1q_OnE'
    TELEGRAM_CHAT_ID = '6317428116'
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
        logging.info('??SE INICIA PROCESO ??REPORTE BATERIAS????')
        print('??SE INICIA PROCESO ??REPORTE BATERIAS????')
        enviar_mensaje_telegram('??SE INICIA PROCESO ??REPORTE BATERIAS????')
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
        
iniciar_proceso() 