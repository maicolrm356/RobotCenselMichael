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
from config import *

tupla_filtro = ( 
            'logo_reportes_web.png',
            'eventos.png', 
            'historico_de_eventos.png',
            'filtrar.png',) 

tupla_formulario = (    
            'buscar.png',
            'exportar.png',
            'exportar_a_csv.png')

horarios_procesos = [
    ('FALLO DE BATERIA / BATTERY FAILURE - LOW', 'baterias', '11:58 AM'), 
    ('baterias', '11:59 AM'), 
    ('intrusion', '2:25 PM'), 
    ('fallo_test', '2:26 AM'), 
    ('panico', '8:15 AM')]

#horarios = ['12:00 PM', '7:00 PM', '12:00 PM',  ]
# count: nos devuelve el numero de veces que se repite un elemento
# index: Nos devuelve la posicion de la primera aparicion de un elemento.c 

# TELEGRAM BOT
def mensaje_telegram(mensaje, ruta_imagen, nombre_imagen, carpeta, nombre_proceso, horario):
    TELEGRAM_BOT_TOKEN = '6232135002:AAGPl356BEAbpzSQlgomBQi45YBUZJk136Q'
    TELEGRAM_CHAT_ID = '7411433556'
    contenido_mensaje = hora_actual
    bot = telebot.TeleBot(TELEGRAM_BOT_TOKEN)
    if mensaje == 'inicio':
        contenido_mensaje += (f"\n\n!! SE INICIA PROCESO DE CENSEL A LAS {hora_actual} !!")
        bot.send_message(chat_id=TELEGRAM_CHAT_ID, text=contenido_mensaje)       
    elif mensaje == 'ingreso_censel':
        print("dentro del : ingreso_censel")
        contenido_mensaje += (f'\nSe ingresó al sistema de Censel correctamente')
        with open(ruta_imagen, 'rb') as img_file:
            img_data = img_file.read()
            bot.send_photo(chat_id=TELEGRAM_CHAT_ID, photo=img_data, caption=contenido_mensaje)
    elif mensaje == 'reportes_web':
        contenido_mensaje += (f'\nSe ingresó a <b>Reportes Web</b> correctamente')
        with open(ruta_imagen, 'rb') as img_file:
            img_data = img_file.read()
            bot.send_photo(chat_id=TELEGRAM_CHAT_ID, photo=img_data, caption=contenido_mensaje, parse_mode='HTML')
    elif mensaje == 'error_ruta_imagen':
        contenido_mensaje += (f'\nNo existe la imagen ({nombre_imagen}) en la carpeta: ({carpeta})')
        bot.send_message(chat_id=TELEGRAM_CHAT_ID, text=contenido_mensaje)
    elif mensaje == 'filtrando_proceso':
        contenido_mensaje += (f'\n Se filtra el proceso de {nombre_proceso} al horario: {horario}')
        with open(ruta_imagen, 'rb') as img_file:
            img_data = img_file.read()
        bot.send_photo(chat_id=TELEGRAM_CHAT_ID, photo=img_data, caption=contenido_mensaje, parse_mode='HTML')

def obtener_coordenadas_imagen_pantalla(ruta_imagen):
    try:
        coordenadas = pyautogui.locateOnScreen(ruta_imagen, confidence=0.9)
        #if coordenadas:
            #coordenadas = (coordenadas.left, coordenadas.top)
        print(f"Coordenadas imagen: {coordenadas}")
        return coordenadas
    except Exception:
        print(f"No hay Imagen.")
        return "error"

def obtener_ruta_imagenes(nombre_imagen):
    if "pantallazo" in nombre_imagen:
        carpeta = "screenshots"
    else:
        carpeta = "img"

    ruta_imagen = os.path.join(os.getcwd(), carpeta, nombre_imagen)
    if os.path.exists(ruta_imagen) and os.path.isfile(ruta_imagen): 
        print(f"la Ruta imagen: {ruta_imagen}"); 
        return ruta_imagen
    print(f"No existe la imagen ({nombre_imagen}) en la carpeta"); 
    return mensaje_telegram('error_ruta_imagen', ruta_imagen, nombre_imagen, carpeta, None, None)

def obtener_captura_pantalla(nombre_captura, carpeta):
    ruta_actual = os.getcwd()
    ruta_errores = os.path.join(ruta_actual, carpeta)
    
    nombre_base, extension = os.path.splitext(nombre_captura)
    nombre_modificado = f'{nombre_base}_pantallazo{extension}'
    print(nombre_modificado)
    
    ruta_captura = os.path.join(ruta_errores, nombre_modificado)
    print("FUNCION: OBTENER CAPTURA DE PANTALLA, RUTA IMAGEN: ", ruta_captura)
    try:
        pyautogui.screenshot(ruta_captura)
        print(f"Captura de pantalla exitosa --> Nombre: {nombre_captura} --> carpeta: {carpeta}")
        return ruta_captura
    except Exception as e:
        print(f" Error al capturar: {e}")

def iniciar_filtro(img):
    error = '_error'
    if not img == 'eventos.png':
        ruta_imagen = obtener_ruta_imagenes(img)
        print("RUTA IMAGEN" + ruta_imagen)
        coordenadas_ruta_imagen = obtener_coordenadas_imagen_pantalla(ruta_imagen)
        if coordenadas_ruta_imagen:
            print("Coordenadas_ruta_imagen_INCIAR FILTRO:", coordenadas_ruta_imagen)
            time.sleep(1)
            pyautogui.click(coordenadas_ruta_imagen)
            time.sleep(5)
            ruta_captura = obtener_captura_pantalla(img, 'screenshots')
            ruta_imagen = obtener_ruta_imagenes(ruta_captura)
            if ruta_imagen:
                mensaje_telegram(img, ruta_imagen, None, None, None, None)
                return True
            else:
                img = img + error
                print(img)
                mensaje_telegram(img, ruta_imagen, None, None, None, None)
                return False
    else:
        ruta_imagen = obtener_ruta_imagenes(img)
        print("RUTA IMAGEN" + ruta_imagen)
        coordenadas_ruta_imagen = obtener_coordenadas_imagen_pantalla(ruta_imagen)
        if coordenadas_ruta_imagen:
            print("Coordenadas_ruta_imagen_INCIAR FILTRO:", coordenadas_ruta_imagen)
            time.sleep(1)
            pyautogui.doubleClick(coordenadas_ruta_imagen)
            time.sleep(5)
            ruta_captura = obtener_captura_pantalla(img, 'screenshots')
            ruta_imagen = obtener_ruta_imagenes(ruta_captura)
            if ruta_imagen:
                mensaje_telegram(img, ruta_imagen, None, None, None, None)
                return True
            else:
                img = img + error
                print(img)
                mensaje_telegram(img, ruta_imagen, None, None, None, None)
                return False

def recorrer_formulario_filtrar():
    hola = '5:53 PM'
    pyautogui.press('tab')
    pyautogui.write(mes_y_ano, interval=0.1)
    time.sleep(1)
    pyautogui.press('tab')
    pyautogui.press('tab')
    #iniciar_formulario()
    for nombre_proceso, horario in horarios_procesos:
    # PROCESo 2
        if  horario == hora_actual:
            pyautogui.write(fecha_desde, interval=0.1)
            pyautogui.press('tab')
            pyautogui.write('00:00', interval=0.1)
            pyautogui.press('tab')
            pyautogui.write(fecha_hasta, interval=0.1)
            pyautogui.press('tab')
            pyautogui.write('12:00', interval=0.1)
            pyautogui.typewrite(['tab'] * 6)
            pyautogui.write('FALLO DE BATERIA / BATTERY FAILURE - LOW', interval=0.1)
            ruta_captura = obtener_captura_pantalla('filtrando_proceso.png', 'screenshots')
            mensaje_telegram('filtrando_proceso', ruta_captura, None, None, nombre_proceso, horario)
            pyautogui.press('tab')
        
        for img in tupla_formulario:
                iniciar_filtro(img)

def iniciar_sesion():
    try:
        # ABRIR NAVEGADOR
        logging.info (f"SE INICIA PROCESO A LAS {hora_actual}")
        #mensaje_telegram('inicio', None)
        pyautogui.hotkey('win', 'r')
        time.sleep(2)
        pyautogui.write('chrome --start-maximized', interval=0.1)
        time.sleep(2)
        pyautogui.press('enter')
        time.sleep(2)

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
        ruta_imagen_logo = obtener_ruta_imagenes('logo_censel.png')
        coordenadas_ruta_imagen_logo = obtener_coordenadas_imagen_pantalla(ruta_imagen_logo)
        time.sleep(1)
        if coordenadas_ruta_imagen_logo:
            obtener_captura_pantalla('inicio_censel.png', 'img')
            ruta_imagen_inicio = obtener_ruta_imagenes('inicio_censel.png')
            mensaje_telegram('ingreso_censel', ruta_imagen_inicio, None, None, None, None)
            
        for img in tupla_filtro:
            iniciar_filtro(img)
        
        recorrer_formulario_filtrar() 
    except Exception as error: 
        logging.error(' No se pudo inicar sesion: ')



iniciar_sesion()
