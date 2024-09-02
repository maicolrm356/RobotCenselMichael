import logging
from datetime import datetime, timedelta
import psycopg2


#Hora_actual
hora_actual = datetime.now().strftime("%I:%M %p").lstrip('0')
print(hora_actual)
# Diccionario para los nombres de los meses en espanol
meses_en_espanol = {
    1: "enero", 2: "febrero", 3: "marzo", 4: "abril", 
    5: "mayo", 6: "junio", 7: "julio", 8: "agosto", 
    9: "septiembre", 10: "octubre", 11: "noviembre", 12: "diciembre"
}

# Obtener la fecha y hora actuales
fecha_actual = datetime.now()

# Formatear el mes y ano manualmente
mes_y_ano = f"{meses_en_espanol[fecha_actual.month]} {fecha_actual.year}"

#Fechas formulario filtrar
fecha_hoy = datetime.now().strftime("%d/%m/%Y")
#print(fecha_hoy)
fecha_desde = fecha_hoy
fecha_hasta = fecha_hoy
fecha_ayer = (datetime.now() - timedelta(days=1)).strftime("%d/%m/%Y")

fecha_ayer2 = (datetime.now() - timedelta(days=1)).strftime('%Y-%m-%d')

# LOGS
logging.basicConfig(
    filename='Errores.log',
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)


def conexion_postgres():
    conexion = psycopg2.connect(
                    host='10.1.1.4',
                    port='5432',
                    database='gamble',
                    user='postgres',
                    password='gambleconsuerte'
                )
    return conexion

