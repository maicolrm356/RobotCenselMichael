import psycopg2
import io


# Sample data as a list of tuples
data = [
    ("'value1'", 'NULL', "value3"),
    ("value4", "value5", "value6"),
    ("value7", "value8", "value9"),
]

# Convert data to CSV format as a string
output = io.StringIO()
for row in data:
    output.write(','.join(row) + '\n')

content = output.getvalue()
print(content)
output.write("'VALOR',NULL,'valor2'\n")

content = output.getvalue()
print(content)

# Move the buffer cursor to the beginning of the string
output.seek(0)

# Connect to the PostgreSQL database
# conn = psycopg2.connect("dbname=your_db user=your_user password=your_password host=your_host")
# cur = conn.cursor()

# Use copy_from to load the data into the table
#cur.copy_from(output, 'your_table', sep='\t')

# Commit the transaction
# conn.commit()

# # Close the cursor and connection
# cur.close()
# conn.close()

import psycopg2
#from io import StringIO
import io


# Sample CSV data
#csv_data = StringIO("""
#1,John,Doe,1990-01-01
#2,Jane,,NULL
#3,Bob,Smith,1985-12-12
#""")
output = io.StringIO()

prueba=''
output.write('INTRUSION,1,'+prueba+',RECEPTORA IPRS-512 PARADOX ,9/4/2024 6:27:05 AM,9/4/2024 6:24:39 AM,2988,,1,,2024-09-03\n')


print(output.getvalue())

output.seek(0)

# Connect to PostgreSQL
conn = psycopg2.connect("dbname=gamble host=10.1.1.4 port=5432 user=postgres password=gambleconsuerte")
cur = conn.cursor()


#    'nombre_novedad','tipo_novedad','tipo_sensor','puerto_nov','fecha_proceso','fecha_recepcion','codigo_abonado','usuario_gestion','estado_gestion','ticket','fecha_novedad'
# Use copy_from with custom NULL representation
cur.copy_from(output, 'replica_seg_control_novedades', sep=',', columns=('nombre_novedad','tipo_novedad','tipo_sensor','puerto_nov','fecha_proceso','fecha_recepcion','codigo_abonado','usuario_gestion','estado_gestion','ticket','fecha_novedad'), null='') 

conn.commit()
cur.close()
conn.close()
output.close()