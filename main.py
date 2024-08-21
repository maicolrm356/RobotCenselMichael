# coding: latin-1
# -*- coding: utf-8 -*-
import pyautogui
import pyperclip
import time
import logging
import telebot
import os
import numpy as np
from config import *

tupla_filtro = ( 
            'logo_censel.png',
            'logo_reportes_web.png',
            'eventos.png', 
            'historico_de_eventos.png',
            'filtrar.png',) 

tupla_postformulario = (    
            'buscar.png',
            'exportar.png',
            'exportar_a_csv.png')

horarios_procesos = [
    ('baterias', fecha_desde, fecha_hasta, '7:00 AM', '12:00', '19:00', 'FALLO DE BATERIA / BATTERY FAILURE - LOW'), #funciona
    ('baterias', fecha_desde, fecha_hasta, '7:00 AM', '00:00', '12:00', 'FALLO DE BATERIA / BATTERY FAILURE - LOW'), #funciona
    ('intrusion', fecha_ayer, fecha_hoy, '7:00 AM', '19:00', '07:00', 'INTRUSION - BUR'), #funciona
    ('fallo_test', fecha_ayer, fecha_hoy, hora_actual, '19:00', '07:00', 'FALLO DE TEST / TEST FAIL - FTS'),  #funciona
    ('panico', fecha_ayer, fecha_ayer, '7:00 AM', '00:00', '23:50', 'PANICO - PAN') #funciona
    ]
# count: nos devuelve el numero de veces que se repite un elemento
# index: Nos devuelve la posicion de la primera aparicion de un elemento.c 

# TELEGRAM BOT
def mensaje_telegram(mensaje, ruta_imagen, nombre_imagen, carpeta, nombre_proceso, horario, img):
    TELEGRAM_BOT_TOKEN = '6232135002:AAGPl356BEAbpzSQlgomBQi45YBUZJk136Q'
    TELEGRAM_CHAT_ID = '7411433556'
    contenido_mensaje = hora_actual
    bot = telebot.TeleBot(TELEGRAM_BOT_TOKEN)
    if mensaje == 'inicio':
        contenido_mensaje += (f"\n!! SE INICIA PROCESO DE CENSEL A LAS {hora_actual} !!")
        bot.send_message(chat_id=TELEGRAM_CHAT_ID, text=contenido_mensaje)       
    elif mensaje == 'ingreso_censel':
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
    elif mensaje == img:
        contenido_mensaje += (f'\nSe ingresó a <b>{mensaje}</b> correctamente')
        with open(ruta_imagen, 'rb') as img_file:
            img_data = img_file.read()
        bot.send_photo(chat_id=TELEGRAM_CHAT_ID, photo=img_data, caption=contenido_mensaje, parse_mode='HTML')
    elif mensaje == 'no hay eventos':
        contenido_mensaje += (f'\n No se encontraron registros al momento de hacer el filtro en el proceso de <b>{nombre_proceso}</b>  \nSe cancela la ejecucion del proceso')
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
        logging.error(f'No se encontro la imagen {ruta_imagen} en la pantalla')
        logging.error(Exception)
        logging.error('Error en la funcion: obtener_coordenadas_imagen_pantalla.')
        return "error"

def obtener_ruta_imagenes(nombre_imagen):    
    try:                                     
        if "pantallazo" in nombre_imagen:
            carpeta = "screenshots"
        else:
            carpeta = "img"

        ruta_imagen = os.path.join(os.getcwd(), carpeta, nombre_imagen)
        
        if os.path.exists(ruta_imagen) and os.path.isfile(ruta_imagen): 
            return ruta_imagen
        
        print(f"No existe la imagen ({nombre_imagen}) en la carpeta ({carpeta})"); 
        logging.error(f"No existe la imagen ({nombre_imagen}) en la carpeta ({carpeta})")
        return mensaje_telegram('error_ruta_imagen', ruta_imagen, nombre_imagen, carpeta, None, None, None)
    except Exception as e:
        logging.error(e)
        logging.error('Error en la funcion: obtener_ruta_imagenes.')

def obtener_captura_pantalla(nombre_captura, carpeta):
    ruta_actual = os.getcwd()
    ruta_errores = os.path.join(ruta_actual, carpeta)
    nombre_base, extension = os.path.splitext(nombre_captura)
    nombre_modificado = f'{nombre_base}_pantallazo{extension}'
    
    ruta_captura = os.path.join(ruta_errores, nombre_modificado)
    try:
        pyautogui.screenshot(ruta_captura)
        print(f"Captura de pantalla exitosa --> Nombre: {nombre_captura} --> carpeta: {carpeta}")
        return ruta_captura
    except Exception as e:
        logging.error(f" Error al capturar: {e}")
        logging.error(f'Error con la ruta de la captura: {ruta_captura}')
        logging.error('Error en la funcion: obtener_captura_pantalla')

def iniciar_filtro(img):
    try:
        error = '_error'
        if not img == 'eventos.png':
            ruta_imagen = obtener_ruta_imagenes(img)
            coordenadas_ruta_imagen = obtener_coordenadas_imagen_pantalla(ruta_imagen)
            if coordenadas_ruta_imagen:
                time.sleep(5)
                pyautogui.click(coordenadas_ruta_imagen)
                time.sleep(5)
                ruta_captura = obtener_captura_pantalla(img, 'screenshots')
                ruta_imagen = obtener_ruta_imagenes(ruta_captura)
                if ruta_imagen:
                    mensaje_telegram(img, ruta_imagen, None, None, None, None, img)
                    return True
                else:
                    img = img + error
                    mensaje_telegram(img, ruta_imagen, None, None, None, None, img)
                    return False
        else:
            ruta_imagen = obtener_ruta_imagenes(img)
            coordenadas_ruta_imagen = obtener_coordenadas_imagen_pantalla(ruta_imagen)
            if coordenadas_ruta_imagen:
                time.sleep(1)
                pyautogui.doubleClick(coordenadas_ruta_imagen)
                time.sleep(5)
                ruta_captura = obtener_captura_pantalla(img, 'screenshots')
                ruta_imagen = obtener_ruta_imagenes(ruta_captura)
                if ruta_imagen:
                    mensaje_telegram(img, ruta_imagen, None, None, None, None, img)
                    return True
                else:
                    img = img + error
                    mensaje_telegram(img, ruta_imagen, None, None, None, None, img)
                    return False
    except Exception as e:
        logging.error(f'Ocurrio un error en el filtro: {e}')
        logging.error('Ocurrio un error en la funcion: iniciar_filtro.')
        logging.error(f'Parametro recibido en iniciar_filtro: {img}')

def recorrer_formulario_filtrar():
    try:
        pyautogui.press('tab')
        pyautogui.write(mes_y_ano, interval=0.1)
        time.sleep(1)
        pyautogui.press('tab')
        pyautogui.press('tab')
        print('hola')
        for nombre_proceso, fecha_desde, fecha_hasta, hora_ejecucion, hora_desde, hora_hasta, codigo_alarma in horarios_procesos:
        # PROCESo 2
            print('hola2')            
            if  hora_ejecucion == hora_actual:
                print('proceso: ', nombre_proceso)
                time.sleep(1)
                pyautogui.write(fecha_desde, interval=0.1)            
                time.sleep(1)
                pyautogui.press('tab')
                pyautogui.write(hora_desde, interval=0.1)
                time.sleep(1)
                
                pyautogui.press('tab')
                pyautogui.write(fecha_hasta, interval=0.1)
                time.sleep(1)
                
                pyautogui.press('tab')
                pyautogui.write(hora_hasta, interval=0.1)
                time.sleep(1)
                
                pyautogui.typewrite(['tab'] * 5)
                pyautogui.write(codigo_alarma, interval=0.1)
                time.sleep(1)
                pyautogui.press('down')
                pyautogui.press('enter')
                time.sleep(1)
                ruta_captura = obtener_captura_pantalla('filtrando_proceso.png', 'screenshots')
                mensaje_telegram('filtrando_proceso', ruta_captura, None, None, nombre_proceso, hora_ejecucion, None)

        print('hola3')
        iniciar_filtro(tupla_postformulario[0])
        no_hay_eventos = obtener_ruta_imagenes('no_hay_eventos.png')
        coordenadas_no_hay_eventos = obtener_coordenadas_imagen_pantalla(no_hay_eventos)

        if coordenadas_no_hay_eventos:
            print('Hola4')
            ruta_captura = obtener_captura_pantalla('no_hay_eventos.png', 'screenshots')
            mensaje_telegram('no hay eventos', ruta_captura, None, None, nombre_proceso, None, None)
            logging.error(f'No se encontraron eventos para descargar el archivo excel en el proceso de {nombre_proceso}, mensaje enviado al telegram')
            logging.error('Se cancela la ejecucion del proceso censel')
        else:
            print('ejecuntando tupla_postforulario')
            for img in tupla_postformulario:
                iniciar_filtro(img)
    except Exception as e:
        logging.error(f'Error en la funcion: recorrer_formulario_filtrar: {e}')

def iniciar_sesion():
    try:
        # ABRIR NAVEGADOR
        logging.info (f"SE INICIA PROCESO A LAS {hora_actual}")
        mensaje_telegram('inicio', None, None, None, None, None, None)
        pyautogui.hotkey('win', 'r')
        time.sleep(2)
        pyautogui.write('chrome --start-maximized', interval=0.01)
        time.sleep(2)
        pyautogui.press('enter')
        time.sleep(2)

        # ABRIR CENSEL  
        time.sleep(2)
        pyautogui.write("http://161.10.252.131:8080/", interval=0.01)
        time.sleep(1)
        pyautogui.press('enter')
        time.sleep(2)

        # INICIAR SESION
        pyperclip.copy('@')
        pyautogui.hotkey('tab')
        pyautogui.write('oscartorres', interval=0.01)
        time.sleep(2)
        # pegar el @
        pyautogui.hotkey('ctrl', 'v')
        time.sleep(2)
        pyautogui.write('consuerte.com', interval=0.01)
        pyautogui.hotkey('tab')
        time.sleep(2)
        pyautogui.write('Oscar1007420377', interval=0.01)
        time.sleep(2)
        pyautogui.hotkey('tab')
        pyautogui.press('enter')

        time.sleep(10)
        for img in tupla_filtro:
            iniciar_filtro(img)
        
        recorrer_formulario_filtrar() 
    except Exception as error: 
        logging.error(' No se pudo inicar sesion: ')



iniciar_sesion()
