import logging
import datetime


#Hora_actual
hora_actual = datetime.datetime.now().strftime("%I:%M %p")
#print(f'ejecucion a las: {hora_actual}')


# LOGS
logging.basicConfig(
    filename='Errores.log',
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)