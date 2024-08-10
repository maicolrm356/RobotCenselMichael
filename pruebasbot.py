import pyautogui
import time

pyautogui.hotkey('win', 'r')
time.sleep(2)
pyautogui.write('chrome --start-maximized', interval=0.1)
time.sleep(2)
pyautogui.press('enter')
time.sleep(1)
pyautogui.screenshot('prueba8.png')
#time.sleep(3)


# PANTALLAZOS
def comparar_imagenes(pantallazo):
    try:
        # Convertir la captura de pantalla a un formato que OpenCV pueda procesar (array de NumPy)
        screenshot_np = np.array(pantallazo)
        screenshot_cv = cv2.cvtColor(screenshot_np, cv2.COLOR_RGB2BGR)

        # Cargar la imagen de la carpeta para comparar
        ruta_imagen = r'C:\Users\auxsenadesarrollo\Desktop\RobotCenselMichael\img\navegador_abierto.png'
        image_to_compare = cv2.imread(ruta_imagen)

        # Asegurarse de que ambas imágenes tienen el mismo tamaño para la comparación
        if screenshot_cv.shape != image_to_compare.shape:
            logging.error('Las imagenes a comparar no tienen el mismo tamaño')
            return mensaje_telegram("error_tamaño_imagen", pantallazo)


        # Calcular la diferencia absoluta entre las dos imágenes
        difference = cv2.absdiff(screenshot_cv, image_to_compare)

        # Si todas las diferencias son 0, las imágenes son iguales
        if np.any(difference):
            return mensaje_telegram('error_imagen', pantallazo)
        else:
            return mensaje_telegram('comparacion_imagen_exitosa', pantallazo)
    except Exception as error:
            logging.error('Ocurrio un error al comparar las imagenes')
            mensaje_telegram("error_tamaño_imagen", pantallazo) 