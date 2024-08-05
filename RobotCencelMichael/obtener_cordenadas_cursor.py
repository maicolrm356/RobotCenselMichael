import pyautogui
import time

print('espere 5 segundos')
time.sleep(5)

coordenadas = pyautogui.position()
print('Las coordenadas del cursos son: ', coordenadas)
