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


tupla_filtro = ( 
            'logo_reportes_web.png',
            'eventos.png', 
            'historico_de_eventos.png',
            'filtrar.png',) 

tupla_formulario = (    
            'buscar.png',
            'exportar.png',
            'exportar_a_csv.png')

# count: nos devuelve el numero de veces que se repite un elemento
# index: Nos devuelve la posicion de la primera aparicion de un elemento.c 

# TELEGRAM BOT
def mensaje_telegram(mensaje, ruta_imagen, nombre_imagen, carpeta):
    TELEGRAM_BOT_TOKEN = '6232135002:AAGPl356BEAbpzSQlgomBQi45YBUZJk136Q'
    TELEGRAM_CHAT_ID = '7411433556'
    contenido_mensaje = hora_actual
    bot = telebot.TeleBot(TELEGRAM_BOT_TOKEN)
    if mensaje == 'inicio':
        contenido_mensaje += (f"\n\n!! SE INICIA PROCESO DE CENSEL A LAS {hora_actual} !!")
        bot.send_message(chat_id=TELEGRAM_CHAT_ID, text=contenido_mensaje)       
    elif mensaje == 'ingreso_censel':
        print("dentro del : ingreso_censel")
        contenido_mensaje += (f'\nSe ingres� al sistema de Censel correctamente')
        with open(ruta_imagen, 'rb') as img_file:
            img_data = img_file.read()
            bot.send_photo(chat_id=TELEGRAM_CHAT_ID, photo=img_data, caption=contenido_mensaje)
    elif mensaje == 'reportes_web':
        contenido_mensaje += (f'\nSe ingres� a <b>Reportes Web</b> correctamente')
        with open(ruta_imagen, 'rb') as img_file:
            img_data = img_file.read()
            bot.send_photo(chat_id=TELEGRAM_CHAT_ID, photo=img_data, caption=contenido_mensaje, parse_mode='HTML')
    elif mensaje == 'error_ruta_imagen':
        contenido_mensaje += (f'\nNo existe la imagen ({nombre_imagen}) en la carpeta: ({carpeta})')
        bot.send_message(chat_id=TELEGRAM_CHAT_ID, text=contenido_mensaje)

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
    return mensaje_telegram('error_ruta_imagen', ruta_imagen, nombre_imagen, carpeta)


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
        print(f" Captura de pantalla exitosa --> Nombre: {nombre_captura} --> carpeta: {carpeta}")
        return ruta_captura
    except Exception as e:
        print(f" Error al capturar: {e}")

#def iniciar_filtro(img):
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
                mensaje_telegram(img, ruta_imagen, None, None)
                return True
            else:
                img = img + error
                print(img)
                mensaje_telegram(img, ruta_imagen, None, None)
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
                mensaje_telegram(img, ruta_imagen, None, None)
                return True
            else:
                img = img + error
                print(img)
                mensaje_telegram(img, ruta_imagen, None, None)
                return False

def iniciar_formulario():
    pyautogui.press('tab')
    pyautogui.write()
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
        ruta_imagen_logo = obtener_ruta_imagenes('logo_censel.png')
        coordenadas_ruta_imagen_logo = obtener_coordenadas_imagen_pantalla(ruta_imagen_logo)
        time.sleep(1)
        if coordenadas_ruta_imagen_logo:
            obtener_captura_pantalla('inicio_censel.png', 'img')
            ruta_imagen_inicio = obtener_ruta_imagenes('inicio_censel.png')
            mensaje_telegram('ingreso_censel', ruta_imagen_inicio, None, None)
            
        for img in tupla_filtro:
            iniciar_filtro(img)
    except Exception as error: 
        logging.error(' No se pudo inicar sesion: ')


def encontrar_imagen_en_pantalla(nombre_imagen):
    ruta_imagen = obtener_ruta_imagenes(nombre_imagen)
    coordenadas_ruta_imagen = obtener_coordenadas_imagen_pantalla(ruta_imagen)
    if coordenadas_ruta_imagen:
        for imagen in tupla_filtro:
            ruta_imagen_tupla = obtener_ruta_imagenes(imagen)
            if ruta_imagen_tupla:
                obtener_captura_pantalla(nombre_imagen, 'img')
                ruta_imagen_captura = obtener_ruta_imagenes(nombre_imagen)
                mensaje_telegram(nombre_imagen, ruta_imagen_captura)


#encontrar_imagen_en_pantalla('reportes_web.png')
iniciar_sesion()
