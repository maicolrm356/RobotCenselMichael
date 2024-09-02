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
import win32com.client
import warnings
warnings.simplefilter("ignore", UserWarning)
from psycopg2 import sql, extras
import glob
#import psycopg2
import pandas

tupla_inicar_sesion = (
            'cancelar_chrome.png',
            'eliminar_sesion.png',
            'email.png',
            'abandonar.png',
            'email.png',
            )

tupla_filtro = (
            'logo_censel.png',
            'logo_reportes_web.png',
            'eventos.png', 
            'reporte_eventos_por_fecha.png',
            'filtros.png',) 

tupla_postformulario = (    
            'buscar.png',
            'exportar.png',
            'exportar_a_csv.png',)

horarios_procesos = [
    #nombre_proceso                 hora_ejecucion  hora_desde hora_hasta          codigo_alarma                    columnas_excel1    columnas_excel2      columnas_excel3         columnas_excel4    columnas_excel5     tabla                         
    ('baterias1',  fecha_desde, fecha_hasta,'5:07 PM', '00:00', '12:00', 'FALLO DE BATERIA / BATTERY FAILURE - LOW', 'cue_ncuenta', '',                  '',                    '',                    '',        'replica_registro_codigos_seguridad'),
    ('baterias2',  fecha_desde, fecha_hasta,'5:qw PM','12:00', '00:00', 'FALLO DE BATERIA / BATTERY FAILURE - LOW',  'cue_ncuenta', '',                  '',                    '',                    '',        'replica_registro_codigos_seguridad'),
    ('intrusion',  fecha_ayer,  fecha_hoy,  '8:05 AM', '19:00', '07:00', 'INTRUSION - BUR',                          'cue_ncuenta', 'rec_czona',         'rec_tFechaProceso',   'rec_tFechaRecepcion', '_puerto', 'replica_seg_control_novedades'),
    ('fallo_test', fecha_ayer,  fecha_hoy,  '8:10 AM', '19:00', '07:00', 'FALLO DE TEST / TEST FAIL - FTS',          'cue_ncuenta', 'rec_tFechaProceso', 'rec_tFechaRecepcion', 'tablaDatos',          '',        'replica_seg_control_novedades'),
    ('panico',     fecha_ayer,  fecha_ayer, '6:08 PM', '00:00', '23:50', 'PANICO SILENCIOSO / PANIC SILENCE - DUR',  'cue_ncuenta', 'rec_czona',         'rec_tFechaProceso',   'rec_tFechaRecepcion', '_puerto', 'replica_seg_control_novedades') #funciona
    ] #hora_actual
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
    elif mensaje == 'horarios_diferentes':
        contenido_mensaje += (f'\n La hora de ejecucion: {horario} del proceso de {nombre_proceso} no coincide con la hora actual, favor validar.')
        bot.send_message(chat_id=TELEGRAM_CHAT_ID, text=contenido_mensaje)
    elif mensaje == 'cerrar_chrome':
        contenido_mensaje += (f'\n Se finaliza el proceso en la pagina de censel y se cierra el navegador. \n\n Se inicia con el procesamiento de la iformacion en el archivo excel')
        bot.send_message(chat_id=TELEGRAM_CHAT_ID, text=contenido_mensaje)
    elif mensaje == 'sesion_encontrada':
        contenido_mensaje += (f'Se encontro una sesion abierta en el aplicativo de censel. \nSe cierra sesion y se inicia nuevamente.')
        with open(ruta_imagen, 'rb') as img_file:
            img_data = img_file.read()
        bot.send_photo(chat_id=TELEGRAM_CHAT_ID, photo=img_data, caption=contenido_mensaje, parse_mode='HTML')

def obtener_coordenadas_imagen_pantalla(ruta_imagen):
    try:
        coordenadas = pyautogui.locateOnScreen(ruta_imagen, confidence=0.9)
        #if coordenadas:
            #coordenadas = (coordenadas.left, coordenadas.top)
        logging.info(f"Ruta imagen {ruta_imagen}. Coordenadas: {coordenadas}")
        return coordenadas
    except Exception:
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
        logging.info(f"Captura de pantalla exitosa --> Nombre: {nombre_captura} --> carpeta: {carpeta}")
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
                time.sleep(2)
                pyautogui.click(coordenadas_ruta_imagen)
                time.sleep(2)
                logging.info(f'Se hizo click en: {img}')
                ruta_captura = obtener_captura_pantalla(img, 'screenshots')
                ruta_imagen = obtener_ruta_imagenes(ruta_captura)
                if ruta_imagen:
                    mensaje_telegram(img, ruta_imagen, None, None, None, None, img)
                    return True
                else:
                    img = img + error
                    mensaje_telegram(img, ruta_imagen, None, None, None, None, img)
                    return False
        elif img == 'abandonar.png':
            ruta_imagen = obtener_ruta_imagenes(img)
            coordenadas_ruta_imagen = obtener_coordenadas_imagen_pantalla(ruta_imagen)
            if coordenadas_ruta_imagen:
                time.sleep(2)
                logging.info(f'Se hizo click en: {img}')
                ruta_captura = obtener_captura_pantalla(img, 'screenshots')
                ruta_imagen = obtener_ruta_imagenes(ruta_captura)
                if ruta_imagen:
                    mensaje_telegram(img, ruta_imagen, None, None, None, None, img)
                    iniciar_sesion()
                    return True
                else:
                    img = img + error
                    mensaje_telegram(img, ruta_imagen, None, None, None, None, img)
                    return False
        else:
            ruta_imagen = obtener_ruta_imagenes(img)
            coordenadas_ruta_imagen = obtener_coordenadas_imagen_pantalla(ruta_imagen)
            if coordenadas_ruta_imagen:
                time.sleep(2)
                pyautogui.doubleClick(coordenadas_ruta_imagen)
                time.sleep(2)
                logging.info(f'Se hizo click en: {img}')
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
        logging.error(f'Ocurrio un error al tratar de encontrar la imagen en la pantalla y dar click: {e}')
        logging.error('Ocurrio un error en la funcion: iniciar_filtro.')
        logging.error(f'Parametro recibido en iniciar_filtro: {img}')

def procesar_archivo_excel(descargas_path='~/Downloads', tabla=None, nombre_proceso=None, col1=None, col2=None, col3=None, col4=None, col5=None):
    try:
        conexion = conexion_postgres()
        cur = conexion.cursor()
        print('conexion a la base de datos: exitosa')
    except Exception as e:
        print('error en la conexion: ', e)
    try:
        #ir a la carpeta descargas
        print('dentro de la funcion: procesar_archivo_excel')
        
        descargas_path = os.path.expanduser(descargas_path)
        #Todos los archivos tipo excel en la carpeta descargas
        archivos_excel_en_descargas = glob.glob(os.path.join(descargas_path, '*.xlsx'))

        if archivos_excel_en_descargas:
            archivo_excel = max(archivos_excel_en_descargas, key=os.path.getctime)
            print(archivo_excel)
    except Exception as e:
        print('Ocurrio un error al encontrar la ruta del archivo excel: ', e)
    
    try:
        print('abrir archivo excel')
        # leer archivo excel
        excel = pandas.read_excel(archivo_excel)
        print('nombre_proceso antes del if: ',nombre_proceso)
        print('nombre de la tabla a ingresar los datos en la base de datos:', tabla)
        
        #seleccionar columna
        contador = 0
        if nombre_proceso == 'baterias1' or nombre_proceso == 'baterias2':
            print('primer if')
            cue_ncuenta = excel[col1]
            cue_ncuenta_sin_duplicados = set(cue_ncuenta)
            
            print('cue_cuenta:')
            for valor in cue_ncuenta_sin_duplicados:
                sentencia = f"INSERT INTO {tabla} (codigo_seguridad, fecha, tipo) VALUES ('{valor}', '{fecha_ayer}', '2')"
                cur.execute(sentencia)
                contador += 1
            conexion.commit()
            print(sentencia)
            print('numero de valores insertados: ', contador)
        elif nombre_proceso == 'intrusion' or nombre_proceso == 'panico':
            print('dentro del if: intrusion o panico')
            cue_ncuenta = excel[col1]
            rec_czona = excel[col2]
            rec_tFechaProceso = excel[col3]
            rec_tFechaRecepcion = excel[col4]
            _puerto = excel[col5]
            print('antes del for')
            try:
                for cue_ncuenta, rec_czona, rec_tFechaProceso, rec_tFechaRecepcion, _puerto in zip(cue_ncuenta, rec_czona, rec_tFechaProceso, rec_tFechaRecepcion, _puerto):
                    #cue_ncuenta, rec_czona, rec_tFechaProceso, rec_tFechaRecepcion, _puerto, = valor
                    
                    valores = {
                        "nombre_novedad": f"'{nombre_proceso.upper()}'" if nombre_proceso else 'NULL',
                        "tipo_novedad": "'1'",
                        "tipo_sensor": f"'{rec_czona}'" if rec_czona.strip() else 'NULL',
                        "puerto_nov": f"'{_puerto}'" if _puerto.strip() else 'NULL',
                        "fecha_proceso": f"'{rec_tFechaProceso}'" if rec_tFechaProceso.strip() else 'NULL',
                        "fecha_recepcion": f"'{rec_tFechaRecepcion}'" if rec_tFechaRecepcion.strip() else 'NULL',
                        "codigo_abonado": f"'{cue_ncuenta}'" if cue_ncuenta else 'NULL',
                        "estado_gestion": "'1'",
                        "estado_gestion": "'1'",
                        "fecha_novedad": f"'{fecha_ayer}'"
                        }
                    
                    columnas = ", ".join(valores.keys())
                    valores_sql = ", ".join(valores.values())
    
                    sentencia = f"INSERT INTO {tabla} ({columnas}) VALUES ({valores_sql})"
                    cur.execute(sentencia)
                    contador += 1
                conexion.commit()
                print(sentencia)
                print('valores insertados: ', contador)
                print('en: ', nombre_proceso)
            except Exception as e:
                print(f'ocurrio un error en {nombre_proceso}:', e)

        elif nombre_proceso == 'fallo_test':
            print('ultimo if')
            cue_ncuenta = excel[col1]
            rec_tFechaProceso = excel[col2]
            rec_tFechaRecepcion = excel[col3]
            tablaDatos = excel[col4]
        try:    
                for cue_ncuenta, rec_tFechaProceso, rec_tFechaRecepcion, tablaDatos in zip(cue_ncuenta, rec_tFechaProceso, rec_tFechaRecepcion, tablaDatos):
                    
                    valores = {
                            "nombre_novedad": f"'{nombre_proceso.upper()}'" if nombre_proceso else 'NULL',
                            "tipo_novedad": "'4'",
                            "tipo_sensor": "'0'",
                            "puerto_nov": f"'{tablaDatos}'" if tablaDatos.strip() else 'NULL',
                            "fecha_proceso": f"'{rec_tFechaProceso}'" if rec_tFechaProceso.strip() else 'NULL',
                            "fecha_recepcion": f"'{rec_tFechaRecepcion}'" if rec_tFechaRecepcion.strip() else 'NULL',
                            "codigo_abonado": f"'{cue_ncuenta}'" if cue_ncuenta else 'NULL',
                            "estado_gestion": "'1'",
                            "fecha_novedad": f"'{fecha_ayer}'"
                            }
                    
                    columnas = ", ".join(valores.keys())
                    valores_sql = ", ".join(valores.values())
        
                    sentencia = f"INSERT INTO {tabla} ({columnas}) VALUES ({valores_sql})"
                    cur.execute(sentencia)
                    contador += 1
                conexion.commit()
                print(sentencia)
                print('valores insertados: ', contador)
                print('en: ', nombre_proceso)
        except Exception as e:
            print(f'ocurrio un error en {nombre_proceso}:', e)        
    except Exception as e:
        print('Ocurrio un error al abrir el archivo excel')


def recorrer_formulario_filtrar():
    try:
        pyautogui.press('tab')
        pyautogui.write(mes_y_ano, interval=0.1)
        time.sleep(1)
        pyautogui.press('tab')
        pyautogui.press('tab')
        for nombre_proceso, fecha_desde, fecha_hasta, hora_ejecucion, hora_desde, hora_hasta, codigo_alarma, col1, col2, col3, col4, col5, tabla in horarios_procesos:
        # PROCESo 2
            if  hora_ejecucion == hora_actual:
                logging.info(f'Proceso a ejecutar: {nombre_proceso}, Hora ejecucion: {hora_ejecucion}, Hora actual: {hora_actual}')
                print('nombre_proceso:')
                print('hora ejecucion:', hora_ejecucion)
                print('hora actual: ', hora_actual)            
                print('proceso: ', nombre_proceso, 'fecha_desde: ', fecha_desde, 'fecha_hasta: ', fecha_hasta, 'hora_ejecucion:', hora_ejecucion, 'hora_desde: ', hora_desde, 'hora_hasta:', hora_hasta, 'codigo_alarma: ', codigo_alarma)
                time.sleep(1)
                pyautogui.write(fecha_desde, interval=0.01)            
                time.sleep(1)
                pyautogui.press('tab')
                pyautogui.write(hora_desde, interval=0.01)
                time.sleep(1)
                
                pyautogui.press('tab')
                pyautogui.write(fecha_hasta, interval=0.01)
                time.sleep(1)
                
                pyautogui.press('tab')
                pyautogui.write(hora_hasta, interval=0.01)
                time.sleep(1)
                
                pyautogui.typewrite(['tab'] * 5)
                pyautogui.write(codigo_alarma, interval=0.01)
                time.sleep(1)
                pyautogui.press('down')
                pyautogui.press('enter')
                time.sleep(20)
                ruta_captura = obtener_captura_pantalla('filtrando_proceso.png', 'screenshots')
                mensaje_telegram('filtrando_proceso', ruta_captura, None, None, nombre_proceso, hora_ejecucion, None)
                break
            else:
                logging.error(f'El horario {hora_ejecucion} no coincide con la hora actual {hora_actual}')
                print(f'El horario {hora_ejecucion} no coincide con la hora actual {hora_actual}')
                mensaje_telegram('horarios_diferentes', None, None, None, nombre_proceso, hora_ejecucion, None)
        if ruta_captura:
            print('fuera del for, pero dentro del otro if')
            iniciar_filtro(tupla_postformulario[0])
            time.sleep(10)
            no_hay_eventos = obtener_ruta_imagenes('no_hay_eventos.png')
            coordenadas_no_hay_eventos = obtener_coordenadas_imagen_pantalla(no_hay_eventos)
            if coordenadas_no_hay_eventos != 'error':
                print(f'no hay eventos, nombre proceso: {nombre_proceso}')
                logging.error(f'no hay eventos, nombre proceso: {nombre_proceso}')
                ruta_captura = obtener_captura_pantalla('no_hay_eventos.png', 'screenshots')
                mensaje_telegram('no hay eventos', ruta_captura, None, None, nombre_proceso, None, None)
                logging.error(f'No se encontraron eventos para descargar el archivo excel en el proceso de {nombre_proceso}, mensaje enviado al telegram')
                print(f'No se encontraron eventos para descargar el archivo excel en el proceso de {nombre_proceso}, mensaje enviado al telegram')
                logging.error('Se cancela la ejecucion del proceso censel')
                os.system("taskkill /f /im chrome.exe")
            else:
                print('ejecuntando tupla_postforulario')
                for img in tupla_postformulario:
                    iniciar_filtro(img)
                    if img == 'exportar_a_csv.png':
                        time.sleep(2)
                        os.system("taskkill /f /im chrome.exe")
                        print('Se finaliza el proceso en la pagina de censel y se cierra el navegador.')
                        mensaje_telegram('cerrar_chrome', None, None, None, None, None ,None)
                        print('nombre_proceso: ', nombre_proceso)
                        print('tabla: ', tabla)
                        procesar_archivo_excel(tabla=tabla, nombre_proceso=nombre_proceso, col1=col1, col2=col2, col3=col3, col4=col4, col5=col5)
                        print('antes del exit.')
                        # exit()
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
        print('Hola mundo')
        
        # ABRIR CENSEL  
        time.sleep(2)
        pyautogui.write("censelc.ultrasecuritysolution.com", interval=0.01)
        time.sleep(1)
        pyautogui.press('enter')
        time.sleep(2)

        # si habia una sesion abierta
        for img in tupla_inicar_sesion:
            iniciar_filtro(img)
        
            # INICIAR SESION
        time.sleep(2)
        pyperclip.copy('@')
        #pyautogui.hotkey('tab')
        pyautogui.write('oscartorres', interval=0.01)
        time.sleep(2)
        # pegar el @
        pyautogui.hotkey('ctrl', 'v')
        time.sleep(2)
        pyautogui.write('consuerte.com', interval=0.01)
        pyautogui.hotkey('tab')
        time.sleep(2)
        pyautogui.write('Oscar13579', interval=0.01)
        time.sleep(2)
        pyautogui.hotkey('tab')
        pyautogui.press('enter')

        time.sleep(10)
        for img in tupla_filtro:
            logging.info('Se inicia ingreso a reportes web')
            iniciar_filtro(img)
        
        recorrer_formulario_filtrar() 
    except Exception as error: 
        logging.error(' No se pudo inicar sesion: ')


#procesar_archivo_excel(r'C:\Users\auxsenadesarrollo\Downloads\reportehistoricohtml.xlsx','replica_registro_codigos_seguridad', 'baterias')
# replica_seg_control_novedades
iniciar_sesion()
# procesar_archivo_excel()