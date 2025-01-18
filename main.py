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
import warnings
warnings.simplefilter("ignore", UserWarning)
from psycopg2 import sql, extras
import glob
import pandas
import io
# Hola como estas
# intentos = 1
# maximos_intentos = 4

tupla_inicar_sesion = (
            'eliminar_sesion.png',
            'email.png',
            'abandonar.png',
            'email.png',
            # 'cancelar_chrome.png',            
            )

tupla_filtro = (
            'logo_censel.png',
            'logo_reportes_web.png',
            'eventos.png', 
            'reporte_eventos_por_fecha.png',            
            'filtros.png',) 

tupla_postformulario = (    
            'exportar.png',
            'exportar_a_csv.png',)

horarios_procesos = [
    #nombre_proceso                 hora_ejecucion  hora_desde hora_hasta          codigo_alarma                    columnas_excel1    columnas_excel2      columnas_excel3         columnas_excel4    columnas_excel5     tabla                         
    ('baterias1',  fecha_hoy, fecha_hoy,   '7:00 PM', '12:00', '07:00', 'FALLO DE BATERIA / BATTERY FAILURE - LOW', 'cue_ncuenta', '',                  '',                    '',                    '',        'registro_codigo_seguridad'),
    ('baterias2',  fecha_hoy, fecha_hoy,   '12:00 PM','00:00',  '12:00', 'FALLO DE BATERIA / BATTERY FAILURE - LOW', 'cue_ncuenta', '',                  '',                    '',                    '',        'registro_codigo_seguridad'),
    ('intrusion',  fecha_ayer,  fecha_hoy,  '7:00 AM', '19:00', '05:30', 'INTRUSION - BUR',                          'cue_ncuenta', 'rec_czona',         'rec_tFechaProceso',   'rec_tFechaRecepcion', '_puerto', 'seg_control_novedades'),
    ('fallo_test', fecha_ayer,  fecha_hoy,  '7:30 AM', '19:00', '07:00', 'FALLO DE TEST / TEST FAIL - FTS',          'cue_ncuenta', 'rec_tFechaProceso', 'rec_tFechaRecepcion', 'tablaDatos',          '',        'seg_control_novedades'),
    ('panico',     fecha_ayer,  fecha_ayer, '6:30 AM', '00:00', '23:50', 'PANICO SILENCIOSO / PANIC SILENCE - DUR',  'cue_ncuenta', 'rec_czona',         'rec_tFechaProceso',   'rec_tFechaRecepcion', '_puerto', 'seg_control_novedades') #funciona
    ] #hora_actual
# count: nos devuelve el numero de veces que se repite un elemento
# index: Nos devuelve la posicion de la primera aparicion de un elemento.c 

# TELEGRAM BOT
def msm_telegram (mensaje, ruta_imagen=None):
    TELEGRAM_BOT_TOKEN = '6232135002:AAGPl356BEAbpzSQlgomBQi45YBUZJk136Q'
    TELEGRAM_CHAT_ID = '7411433556'
    bot = telebot.TeleBot(TELEGRAM_BOT_TOKEN)
    if ruta_imagen:
        with open(ruta_imagen, 'rb') as img_file:
            img_data = img_file.read()
            bot.send_photo(chat_id=TELEGRAM_CHAT_ID, photo=img_data, caption=mensaje ,parse_mode='HTML')
    else:
        bot.send_message(chat_id=TELEGRAM_CHAT_ID, text=mensaje, parse_mode='HTML')


def obtener_coordenadas_imagen_pantalla(nombre_imagen):
    try:
        coordenadas = pyautogui.locateOnScreen(nombre_imagen, confidence=0.9)
        print(coordenadas)
        if coordenadas:
            print(f"Ruta imagen {nombre_imagen}. Coordenadas: {coordenadas}")
            logging.info(f"Ruta imagen {nombre_imagen}. Coordenadas: {coordenadas}")
            return coordenadas
        else:
            return None
    except Exception as e:
        logging.error(f'No se encontro la imagen {nombre_imagen} en la pantalla')
        logging.error(e)
        logging.error('Error en la funcion: obtener_coordenadas_imagen_pantalla.')

def obtener_ruta_imagenes(nombre_imagen):    
    try:                                     
        if "pantallazo" in nombre_imagen:
            carpeta = "screenshots"
        elif "mp4" in nombre_imagen:
            carpeta = "grabaciones"
        else:   
            carpeta = "img"

        ruta_imagen = os.path.join(os.getcwd(), carpeta, nombre_imagen)
        
        if os.path.exists(ruta_imagen) and os.path.isfile(ruta_imagen): 
            return ruta_imagen
        else:
            logging.error(f"No existe la imagen ({nombre_imagen}) en la carpeta ({carpeta})")
            # return mensaje_telegram('error_ruta_imagen', ruta_imagen, nombre_imagen, carpeta, None, None, None, None, None, None, None)
            return msm_telegram(f'\nNo existe la imagen ({nombre_imagen}) en la carpeta: ({carpeta}) \n{ruta_imagen}')
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

def iniciar_filtro(img, tupla=None):
    try:
        time.sleep(8)
        ruta_imagen = obtener_ruta_imagenes(img)
        time.sleep(1)
        coordenadas_imagen = obtener_coordenadas_imagen_pantalla(ruta_imagen)
        if coordenadas_imagen:  
            print('coordenadas imagen', coordenadas_imagen)
            pyautogui.moveTo(coordenadas_imagen)
            time.sleep(1)
            ruta_captura = obtener_captura_pantalla(img, 'screenshots')
            ruta_captura = obtener_ruta_imagenes(ruta_captura)
            time.sleep(8)
            if img == 'eventos.png':
                pyautogui.doubleClick(coordenadas_imagen)
            pyautogui.click(coordenadas_imagen)
            time.sleep(5)
            if img == 'logo_reportes_web.png':
                time.sleep(20)
            msm_telegram(f'Se encontro {img} en la pantalla', ruta_captura)
            return True
        else:
            if tupla != 'iniciar_sesion':
                    ruta_captura = obtener_captura_pantalla(img, 'screenshots')
                    ruta_captura = obtener_ruta_imagenes(ruta_captura)
                    msm_telegram(f'No se encontro la imagen: {img} en la pantalla. \nSe cierra el navegador y se inicia el proceso nuevamente.', ruta_captura)
                    os.system("taskkill /F /IM chrome.exe")
                    time.sleep(2)
                    iniciar_sesion()
    except Exception as e: 
        logging.error(f'Ocurrio un error al tratar de encontrar la imagen en la pantalla y dar click: {e}')
        logging.error('Ocurrio un error en la funcion: iniciar_filtro.')
        logging.error(f'Parametro recibido en iniciar_filtro: {img}')


def procesar_archivo_excel(descargas_path='~/Downloads', tabla=None, nombre_proceso=None, col1=None, col2=None, col3=None, col4=None, col5=None):
    try:
        conexion = conexion_postgres()
        cur = conexion.cursor()
        msm_telegram('Se conecto correctamente a la base de datos')
        # mensaje_telegram('Se conecto correctamente a la base de datos.', None, None, None, None, None, None, None, None, None, None)
    except Exception as e:
        msm_telegram(f'ocurrio un error al intentar conectar con la base de datos. \n{e}')
        # mensaje_telegram('ocurrio un error al intentar conectar con la base de datos.', None, None, None, None, None, None, e, None, None, None)
        logging.error(f'ocurrio un error al intentar conectar con la base de datos: {e}')
        msm_telegram(f'Se finaliza la ejecucion.')
        exit()
    try:
        #ir a la carpeta descargas
        print('dentro de la funcion: procesar_archivo_excel')
        
        descargas_path = os.path.expanduser(descargas_path)
        #Todos los archivos tipo excel en la carpeta descargas
        archivos_excel_en_descargas = glob.glob(os.path.join(descargas_path, '*.xlsx'))

        if archivos_excel_en_descargas:
            archivo_excel = max(archivos_excel_en_descargas, key=os.path.getctime)
            msm_telegram(f'Se encontro el archivo excel correctamente \n{archivo_excel}')
            # mensaje_telegram('Se encontro el archivo excel correctamente.', None, None, None, None, None, None, None,  archivo_excel, None, None)
    except Exception as e:
        msm_telegram(f'Ocurrio un error al encontrar la ruta del archivo excel: \n{e}')
        # mensaje_telegram('Ocurrio un error al encontrar la ruta del archivo excel: ', None, None, None, None, None, None, e, None, None, None)
        logging.error(f'Ocurrio un error al encontrar la ruta del archivo excel: {e}')
    
    try:
        # leer archivo excel
        excel = pandas.read_excel(archivo_excel)
        
        output = io.StringIO()
        
        #seleccionar columna
        contador = 0
        
        estado_gestion = '1'
        if nombre_proceso == 'baterias1' or nombre_proceso == 'baterias2':
            cue_ncuenta = excel[col1]
            cue_ncuenta_sin_duplicados = set(cue_ncuenta)
            tipo = 2
            try:
                for codigo_seguridad in cue_ncuenta_sin_duplicados:
                    output.write(f"{codigo_seguridad},{fecha_ayer},{tipo}\n")
                    contador += 1
                    
                output.seek(0)    
                cur.copy_from(output, tabla, sep=',', columns=('codigo_seguridad','fecha','tipo'), null='NULL')
                conexion.commit()
                msm_telegram(f'se insertaron {contador} valores en {nombre_proceso}')
                # mensaje_telegram('insercion', None, None, None, nombre_proceso, None, None, None, None, contador, None)
            except Exception as e:
                msm_telegram(f'Ocurrio un error al intentar insertar en la base de datos en el proceso: {nombre_proceso} \n{e}')
                # mensaje_telegram('error', None, None, None, nombre_proceso, None, None, e, None, None, None)
                logging.error(f'Ocurrio un error en procesar_archivo_excel en el proceso: {nombre_proceso}')
                logging.error(f'{e}')
                print(f'error: {e}')
        elif nombre_proceso == 'intrusion' or nombre_proceso == 'panico':
            if nombre_proceso == 'intrusion': tipo_novedad = '1' 
            else: tipo_novedad = '2' #panico
            cue_ncuenta = excel[col1]
            rec_czona = excel[col2]
            rec_tFechaProceso = excel[col3]
            rec_tFechaRecepcion = excel[col4]
            _puerto = excel[col5]
            try:
                for cue_ncuenta, rec_czona, rec_tFechaProceso, rec_tFechaRecepcion, _puerto in zip(cue_ncuenta, rec_czona, rec_tFechaProceso, rec_tFechaRecepcion, _puerto):
                    
                    if rec_czona:
                        try:
                            rec_czona = int(rec_czona)
                        except ValueError:
                            rec_czona = 'NULL'
                    else:
                        rec_czona = 'NULL'
                    
                    output.write(f'{nombre_proceso.upper()},{tipo_novedad},{rec_czona},{_puerto},{rec_tFechaProceso},{rec_tFechaRecepcion},{cue_ncuenta},{estado_gestion},{fecha_ayer}\n')
                    contador += 1
                output.seek(0)
                cur.copy_from(output, tabla, sep=',', columns=('nombre_novedad', 'tipo_novedad', 'tipo_sensor', 'puerto_nov', 'fecha_proceso', 'fecha_recepcion', 'codigo_abonado', 'estado_gestion', 'fecha_novedad'), null='NULL')
                conexion.commit()
                msm_telegram(f'se insertaron {contador} valores en {nombre_proceso}')
                # mensaje_telegram('insercion', None, None, None, nombre_proceso, None, None, None, None, contador, None)
            except Exception as e:
                msm_telegram(f'Ocurrio un error al intentar insertar en la base de datos en el proceso: {nombre_proceso} \n{e}')
                # mensaje_telegram('error', None, None, None, nombre_proceso, None, None, e, None, None, None)
                print('Error:', e)
                logging.error(f'Ocurrio un error en procesar_archivo_excel en el proceso: {nombre_proceso}')
                logging.error(f'{e}')
        elif nombre_proceso == 'fallo_test':
            cue_ncuenta = excel[col1]
            rec_tFechaProceso = excel[col2]
            rec_tFechaRecepcion = excel[col3]
            tablaDatos = excel[col4]
            tipo_novedad = 4
            tipo_sensor = 0
            
            try:    
                for cue_ncuenta, rec_tFechaProceso, rec_tFechaRecepcion, tablaDatos in zip(cue_ncuenta, rec_tFechaProceso, rec_tFechaRecepcion, tablaDatos):
                    
                    output.write(f'{nombre_proceso.upper()},{tipo_novedad},{tipo_sensor},{tablaDatos},{rec_tFechaProceso},{rec_tFechaRecepcion},{cue_ncuenta},{estado_gestion},{fecha_ayer}\n')
                    contador += 1

                output.seek(0)
                cur.copy_from(output, tabla, sep=',', columns=('nombre_novedad', 'tipo_novedad', 'tipo_sensor', 'puerto_nov', 'fecha_proceso', 'fecha_recepcion', 'codigo_abonado', 'estado_gestion', 'fecha_novedad'), null='NULL')
                conexion.commit()
                msm_telegram(f'se insertaron {contador} valores en {nombre_proceso}')
                # mensaje_telegram('insercion', None, None, None, nombre_proceso, None, None, None, None, contador, None)
            except Exception as e:
                msm_telegram(f'Ocurrio un error al intentar insertar en la base de datos en el proceso: {nombre_proceso} \n{e}')
                # mensaje_telegram('error', None, None, None, nombre_proceso, None, None, e, None, None, None)
                logging.error(f'Ocurrio un error en procesar_archivo_excel en el proceso: {nombre_proceso}')
                logging.error(f'{e}')
                print('Error:', e)
                logging.error(f'Ocurrio un error en procesar_archivo_excel en el proceso: {nombre_proceso}')
                logging.error(f'{e}')
    except Exception as e:
        msm_telegram(f'ocurrio un error al intentar abrir el archivo excel \n{archivo_excel} \n{e}')
        # mensaje_telegram('ocurrio un error al intentar abrir el archivo excel', None, None, None, None, None, None, e, archivo_excel, None, None)
    finally:
        cur.close()
        conexion.close()
        output.close()
        msm_telegram('Se cierra la conexion a la base de datos y se finaliza el proceso correctamente')
        # mensaje_telegram('Se cierra la conexion a la base de datos y se finaliza el proceso correctamente', None, None, None, None, None, None, None, None, None, None)
        fin = time.time()
        duracion = fin-inicio
        duracion_minutos = round(duracion / 60, 2)
        
        try:
            os.remove(archivo_excel)
            msm_telegram(f'Se elimina el archivo excel correctamente \n{archivo_excel}')
            # mensaje_telegram(f'Se elimina el archivo excel correctamente \n{archivo_excel}', None, None, None, None, None, None, None, archivo_excel, None, None)
        except Exception as e:
            msm_telegram(f'Ocurrio un error al intentar eliminar el archivo excel \n{archivo_excel}\n{e}')
            # mensaje_telegram(f'Ocurrio un error al intentar eliminar el archivo excel \n{archivo_excel}\n{e}', None, None, None, None, None, None, e, archivo_excel, None, None)
        # mensaje_telegram(f'el proceso duro: {duracion_minutos} minutos', None, None, None, None, None, None, None, None, None, None)
        msm_telegram(f'el proceso duro: {duracion_minutos} minutos')
        #ruta_video = detener_grabacion()
        #ruta_video = obtener_ruta_imagenes('grabacion.mp4')
        #print('ruta de la grabacion: ', ruta_video)

def recorrer_formulario_filtrar():
    try:
        horario_encontrado = False
        pyautogui.press('tab')
        time.sleep(1)
        pyautogui.write(mes_y_ano, interval=0.1)
        time.sleep(1)
        pyautogui.press('tab')
        pyautogui.press('tab')
        for nombre_proceso, fecha_desde, fecha_hasta, hora_ejecucion, hora_desde, hora_hasta, codigo_alarma, col1, col2, col3, col4, col5, tabla in horarios_procesos:
        # PROCESo 2
            if hora_ejecucion == hora_actual:
                horario_encontrado = True
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
                break
            else:
                logging.error(f'El horario {hora_ejecucion} no coincide con la hora actual {hora_actual}')
                print(f'El horario {hora_ejecucion} no coincide con la hora actual {hora_actual}')
                msm_telegram(f'\n La hora de ejecucion: {hora_ejecucion} del proceso de {nombre_proceso} no coincide con la hora actual, favor validar.')
        
        if horario_encontrado == True:
            iniciar_filtro('buscar.png')
            ruta_captura = obtener_captura_pantalla('filtrando_proceso.png', 'screenshots')
            msm_telegram(f'\n Se filtra el proceso de {nombre_proceso} al horario: {hora_ejecucion}')
            time.sleep(5)
            no_hay_eventos = obtener_ruta_imagenes('no_hay_eventos.png')
            coordenadas_no_hay_eventos = obtener_coordenadas_imagen_pantalla(no_hay_eventos)
            if coordenadas_no_hay_eventos:
                print(f'no hay eventos, nombre proceso: {nombre_proceso}')
                logging.error(f'no hay eventos, nombre proceso: {nombre_proceso}')
                ruta_captura = obtener_captura_pantalla('no_hay_eventos.png', 'screenshots')
                msm_telegram(f'\n No se encontraron registros al momento de hacer el filtro en el proceso de <b>{nombre_proceso}</b>  \nSe cancela la ejecucion del proceso', ruta_captura)
                logging.error(f'No se encontraron eventos para descargar el archivo excel en el proceso de {nombre_proceso}, mensaje enviado al telegram')
                print(f'No se encontraron eventos para descargar el archivo excel en el proceso de {nombre_proceso}, mensaje enviado al telegram')
                logging.error('Se cancela la ejecucion del proceso censel')
                os.system("taskkill /f /im chrome.exe")
            else:
                for img in tupla_postformulario:
                    iniciar_filtro(img)
                    if img == 'exportar_a_csv.png':
                        time.sleep(2)
                        os.system("taskkill /f /im chrome.exe")
                        print('Se finaliza el proceso en la pagina de censel y se cierra el navegador.')
                        msm_telegram(f'\n Se finaliza el proceso en la pagina de censel y se cierra el navegador. \n-Se inicia con el procesamiento de la informacion en el archivo excel')
                        print('nombre_proceso: ', nombre_proceso)
                        print('tabla: ', tabla)
                        procesar_archivo_excel(tabla=tabla, nombre_proceso=nombre_proceso, col1=col1, col2=col2, col3=col3, col4=col4, col5=col5)
                        print('antes del exit.')
                        exit()
        else: 
            msm_telegram('Ningun horario es valido para ejecutar el proceso. \nSe cierra el navegador.')
            os.system("taskkill /f /im chrome.exe")
            exit()
    except Exception as e:
        logging.error(f'Error en la funcion: recorrer_formulario_filtrar: {e}')

def iniciar_sesion():
    try:
        logging.info (f"SE INICIA PROCESO A LAS {hora_actual}")
        msm_telegram(f"!! SE INICIA PROCESO DE CENSEL A LAS {hora_actual} !!")
        pyautogui.hotkey('win', 'r')
        time.sleep(2)
        pyautogui.write('chrome --incognito --start-maximized', interval=0.01)
        time.sleep(2)
        pyautogui.press('enter')
        time.sleep(2)
        
        # ABRIR CENSEL  
        time.sleep(2)
        pyautogui.hotkey('ctrl', 'l')
        time.sleep(2)
        pyautogui.write("censelc.ultrasecuritysolution.com", interval=0.01)
        time.sleep(1)
        pyautogui.press('enter')
        time.sleep(2)

        # si habia una sesion abierta
        for img in tupla_inicar_sesion:
            iniciar_filtro(img, 'iniciar_sesion')
        
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
    except Exception as e: 
        logging.error('No se pudo inicar sesion: ')
        msm_telegram(f'No se pudo iniciar sesion \n{e}')


#procesar_archivo_excel(r'C:\Users\auxsenadesarrollo\Downloads\reportehistoricohtml.xlsx','replica_registro_codigos_seguridad', 'baterias')
# replica_seg_control_novedades
iniciar_sesion()
# procesar_archivo_excel()