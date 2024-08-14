import pyautogui
import os

tupla_imagenes = ('logo_censel.png', 
            'logo_reportes_web.png',
            'eventos.png', 
            'historico_de_eventos.png',
            'filtrar.png', 'buscar.png',
            'exportar.png',
            'exportar_a_csv.png')

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
    return print('error_ruta_imagen', ruta_imagen, nombre_imagen, carpeta)

def obtener_coordenadas_imagen_pantalla(ruta_imagen):
    try:
        coordenadas = pyautogui.locateOnScreen(ruta_imagen, confidence=0.9)
        if coordenadas:
            coordenadas = (coordenadas.left, coordenadas.top)
            print(f"Coordenadas imagen: {coordenadas}")
        return coordenadas
    except Exception:
        print(f"No hay Imagen.")
        return "error"
    
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
        for img in tupla_imagenes:
            iniciar_filtro(img)
        ruta_imagen_logo = obtener_ruta_imagenes('logo_censel.png')
        coordenadas_ruta_imagen_logo = obtener_coordenadas_imagen_pantalla(ruta_imagen_logo)
        time.sleep(1)
        if coordenadas_ruta_imagen_logo:
            obtener_captura_pantalla('inicio_censel.png', 'img')
            ruta_imagen_inicio = obtener_ruta_imagenes('inicio_censel.png')
            mensaje_telegram('ingreso_censel', ruta_imagen_inicio)
    except Exception as error: 
        logging.error(' No se pudo inicar sesion: ')

def iniciar_filtro(img):
    ruta_imagen = obtener_ruta_imagenes(img)
    print("RUTA IMAGEN" + ruta_imagen)
    coordenadas_ruta_imagen = obtener_coordenadas_imagen_pantalla(ruta_imagen)
        if coordenadas_ruta_imagen:
            print(coordenadas_ruta_imagen)
            pyautogui.click(coordenadas_ruta_imagen)
            time.sleep(5)
            ruta_captura = obtener_captura_pantalla(img, 'screenshots')
            ruta_imagen = obtener_ruta_imagenes(ruta_captura)
            
            if ruta_imagen:
                mensaje_telegram('reportes_web', ruta_imagen, None, None)
obtener_ruta_imagenes()
obtener_coordenadas_imagen_pantalla()