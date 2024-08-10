# coding: latin-1
# -*- coding: utf-8 -*-
import pyautogui
import pyperclip
import time
import logging
import telebot
import os
#import cv2
import numpy as np
from config import logging
from config import hora_actual


# LOGS
#log_directory = r"C:\Users\auxsenadesarrollo\Desktop\RobotCenselMichael/errores"  # Cambia esta ruta segÃºn tus necesidades
'''
if not os.path.exists(log_directory): 
    os.makedirs(log_directory)
'''
# TELEGRAM BOT
def mensaje_telegram(mensaje, pantallazo):
    TELEGRAM_BOT_TOKEN = '6232135002:AAGPl356BEAbpzSQlgomBQi45YBUZJk136Q' #TOKEN CHAT TELEGRAM DE REPORTE DE ALARMAS
    TELEGRAM_CHAT_ID = '7411433556'
    bot = telebot.TeleBot(TELEGRAM_BOT_TOKEN)
    contenido_mensaje = hora_actual
    #pantallazo = pyautogui.screenshot('abrir_navegador.png')
    if mensaje == 'inicio':
        contenido_mensaje += (f"\n\n!! SE INICIA PROCESO DE CENSEL A LAS {hora_actual} !!")
        bot.send_message(chat_id=TELEGRAM_CHAT_ID, text=contenido_mensaje)
    elif mensaje == 'error_imagen':
        contenido_mensaje += (f"\nLas imagenes a comparar no coinciden.")
        bot.send_photo(chat_id=TELEGRAM_CHAT_ID, photo=pantallazo, caption=contenido_mensaje)
        contenido_mensaje += ('Imagen de referencia:')
        bot.send_photo(chat_id=TELEGRAM_CHAT_ID, photo=r'C:\Users\auxsenadesarrollo\Desktop\RobotCenselMichael\img\navegador_abierto.png', caption=contenido_mensaje)
    elif mensaje == 'error_tamaño_imagen':
        contenido_mensaje += (f'\nLas imagenes a comparar no tienen el mismo tamaño, por favor validar el contenido.')
        bot.send_photo(chat_id=TELEGRAM_CHAT_ID, photo=pantallazo, text=contenido_mensaje)        
    elif mensaje == 'comparacion_imagen_exitosa':
        contenido_mensaje += (f'\nSe abrió el navegador correctamente')
        bot.send_photo(chat_id=TELEGRAM_CHAT_ID, photo=pantallazo, text=contenido_mensaje)

def obtener_coordenadas_imagen_pantalla(ruta_imagen):
    try:
        coordenadas = pyautogui.locateOnScreen(ruta_imagen, confidence=0.9)
        print(f"Coordenadas imagen: {coordenadas}")
        return coordenadas
    except Exception:
        print(f"No hay Imagen.")
        return "error"

def obtener_ruta_imagenes(nombre_imagen):
    ruta_imagen = os.path.join(os.getcwd(), "img", nombre_imagen)
    if os.path.exists(ruta_imagen) and os.path.isfile(ruta_imagen): 
        print(f"la Ruta imagen: {ruta_imagen}"); 
        return ruta_imagen
    print(f"No existe la imagen ({nombre_imagen}) en la carpeta"); 
    return False


def iniciar_proceso():
    try:
        # ABRIR NAVEGADOR
        logging.info (f"SE INICIA PROCESO A LAS {hora_actual}")
        mensaje_telegram('inicio', None)
        pyautogui.hotkey('win', 'r')
        time.sleep(2)
        pyautogui.write('chrome --start-maximized', interval=0.1)
        time.sleep(2)
        pyautogui.press('enter')
        time.sleep(2)
        #comparar_imagenes(pantallazo)

        # ABRIR CENSEL  
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
        time.sleep(5)
        ruta_imagen_logo = obtener_ruta_imagenes('logo.png')
        coordenadas_ruta_imagen_logo = obtener_coordenadas_imagen_pantalla(ruta_imagen_logo)
        time.sleep(1)
        print(coordenadas_ruta_imagen_logo)
        #pyautogui.click(coordenadas_ruta_imagen_logo)
        # INGRESAR A REPORTES WEB
        #time.sleep(5)
        #pyautogui.press('tab')
        #time.sleep(2)

        #pyautogui.press('enter')
        #time.sleep(4)
    except Exception as error: 
        logging.error(' No se pudo inicar sesion: ')

iniciar_proceso()
