import pyautogui
import os

def obtener_captura_pantalla(nombre_captura, carpeta):
    ruta_actual = os.getcwd()
    ruta_errores = os.path.join(ruta_actual, carpeta)
    ruta_imagen = os.path.join(ruta_errores, nombre_captura)
    try:
        pyautogui.screenshot(ruta_imagen)
        print(f" Captura de pantalla exitosa --> Nombre: {nombre_captura} --> carpeta: {carpeta}")
        return ruta_imagen
    except Exception as e:
        print(f" Error al capturar: {e}")
        mensaje_telegram('error_captura', None)
obtener_captura_pantalla('Prueba.png', 'img')