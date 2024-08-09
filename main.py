# coding: latin-1
# -*- coding: utf-8 -*-
import pyautogui
import pyperclip
import time
import datetime
import logging
import requests
import telebot
import os
import cv2
import numpy as np
import os

#Hora_actual
hora_actual = datetime.datetime.now().strftime("%I:%M:%p")
print(f'ejecucion a las: {hora_actual}')

# LOGS
logging.basicConfig(
    filename='errores.log',
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

log_directory = r"C:\Users\auxsenadesarrollo\Desktop\RobotCenselMichael/errores"  # Cambia esta ruta segÃºn tus necesidades

if not os.path.exists(log_directory): 
    os.makedirs(log_directory)

# TELEGRAM BOT
def mensaje_telegram(mensaje):
    TELEGRAM_BOT_TOKEN = '6232135002:AAGPl356BEAbpzSQlgomBQi45YBUZJk136Q' #TOKEN CHAT TELEGRAM DE REPORTE DE ALARMAS
    TELEGRAM_CHAT_ID = '7411433556'
    hora_actual = datetime.datetime.now().strftime("%I:%M:%p")
    bot = telebot.TeleBot(TELEGRAM_BOT_TOKEN)
    contenido_mensaje = hora_actual
    pantallazo = pyautogui.screenshot('abrir_navegador.png')
    if mensaje == 'inicio':
        contenido_mensaje += (f"\n\n!! SE INICIA PROCESO DE CENSEL A LAS {hora_actual} !!")
        bot.send_message(chat_id=TELEGRAM_CHAT_ID, text=contenido_mensaje)
    elif mensaje == 'error_imagen':
        contenido_mensaje += (f"\nLas imagenes a comparar no coinciden.")
        bot.send_photo(chat_id=TELEGRAM_CHAT_ID, photo=pantallazo, caption=contenido_mensaje)
    elif mensaje == 'error_tamaño_imagen':
        contenido_mensaje += (f'\nLas imagenes a comparar no tienen el mismo tamaño, por favor validar el contenido.')
# PANTALLAZOS
def comparar_imagenes():
    try:
        pantallazo = pyautogui.screenshot('abrir_navegador.png') #Cambiar pantallazos dependiendo del equipo
        # Convertir la captura de pantalla a un formato que OpenCV pueda procesar (array de NumPy)
        screenshot_np = np.array(pantallazo)
        screenshot_cv = cv2.cvtColor(screenshot_np, cv2.COLOR_RGB2BGR)

        # Cargar la imagen de la carpeta para comparar
        ruta_imagen = r'C:\Users\auxsenadesarrollo\Desktop\RobotCenselMichael\img\image.png'
        image_to_compare = cv2.imread(ruta_imagen)

        # Asegurarse de que ambas imágenes tienen el mismo tamaño para la comparación
        if screenshot_cv.shape != image_to_compare.shape:
            logging.error('Las imagenes a comparar no tienen el mismo tamaño')
            return mensaje_telegram("error_tamaño_imagen")


        # Calcular la diferencia absoluta entre las dos imágenes
        difference = cv2.absdiff(screenshot_cv, image_to_compare)

        # Si todas las diferencias son 0, las imágenes son iguales
        if np.any(difference):
            return mensaje_telegram('error_imagen')
        
    except Exception as error:
            logging.error('Ocurrio un error al comparar las imagenes')
            mensaje_telegram("error_tamaño_imagen")




def iniciar_proceso():
    try:
        # ABRIR NAVEGADOR
        logging.info (f"SE INICIA PROCESO A LAS {hora_actual}")
        mensaje_telegram('inicio')
        pyautogui.hotkey('win', 'r')
        time.sleep(2)
        pyautogui.write('chrome --start-maximized', interval=0.1)
        time.sleep(2)
        pyautogui.press('enter')
        time.sleep(2)
        comparar_imagenes()

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



#pantallazo = pyautogui.screenshot('abrir_navegador.png') #Cambiar pantallazos dependiendo del equipo