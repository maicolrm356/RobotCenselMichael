from datetime import datetime, timedelta


# fecha = (datetime.now() - timedelta(days=1)).strftime('%Y-%m-%d')
fecha_ayer = (datetime.now() - timedelta(days=1)).strftime("%d")

fecha = (datetime.now() - timedelta(days=1)).strftime('%Y-%m-%d')


print(fecha_ayer)
print(fecha)
