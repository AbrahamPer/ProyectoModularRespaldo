# # Ruta de la carpeta con los archivos CSV
# folder = "C:\Users\SERGIUS\Documents\Abraham\Proyecto modular\Archivos CSV"
#
# # Lista todos los archivos en la carpeta
# files = os.listdir(folder)

######################################################

# import chardet
#
# # Abrir el archivo en modo binario para detectar la codificación
# with open(r"C:\Users\SERGIUS\Documents\Abraham\Proyecto modular\Archivos CSV\Clientes.csv", 'rb') as file:
#     raw_data = file.read()
#     result = chardet.detect(raw_data)
#     encoding = result['encoding']
#
# print(f"La codificación detectada es: {encoding}")

######################################################

# import pandas as pd

# Leer el archivo CSV con la codificación original
# df = pd.read_csv(r"C:\Users\SERGIUS\Documents\Abraham\Proyecto modular\Archivos CSV\Abonos.csv", encoding='ascii')
# print(df)
# # Guardar el archivo CSV con la nueva codificación
# df.to_csv(r"C:\Users\SERGIUS\Documents\Abraham\Proyecto modular\Archivos CSV\AbonosASCII.csv", encoding='ascii', index=False)

######################################################

# import requests
# from bs4 import BeautifulSoup
#
# # URL de Google Finance para el tipo de cambio USD/MXN
# url = "https://www.google.com/finance/quote/USD-MXN"
#
# # Hacemos una solicitud GET a la página
# response = requests.get(url)
#
# # Verificamos que la solicitud fue exitosa
# if response.status_code == 200:
#     # Parseamos el contenido HTML de la página
#     soup = BeautifulSoup(response.content, 'html.parser')
#
#     # Extraemos el valor del tipo de cambio usando el selector adecuado
#     price_element = soup.find('div', {'class': 'YMlKec fxKbKc'})
#
#     if price_element:
#         # Obtenemos el texto del elemento
#         exchange_rate = price_element.text
#         print(f"El tipo de cambio actual de USD a MXN es: {exchange_rate}")
#     else:
#         print("No se pudo encontrar el tipo de cambio en la página.")
# else:
#     print(f"Error al acceder a la página: {response.status_code}")
#
# from datetime import datetime
#
# # Obtener la fecha y hora actuales
# fecha_actual = datetime.now()
#
# # # Formatear la fecha en el formato: Día-Mes-Año Hora:Minuto:Segundo
# # fecha_formateada = fecha_actual.strftime("%d-%m-%Y %H:%M:%S")
#
# # Formatear la fecha en el formato: Año-Mes-Día
# fecha_formateada = fecha_actual.strftime("%Y-%d-%m")
#
# # Mostrar la fecha formateada
# print("Fecha formateada:", fecha_formateada)

######################################################

# Leer el archivo CSV con pandas

# df = pd.read_csv(r"C:\Users\SERGIUS\Documents\Abraham\Proyecto modular\Archivos CSV\Lotes.csv") # Ya importado
# df = pd.read_csv(r"C:\Users\SERGIUS\Documents\Abraham\Proyecto modular\Archivos CSV\Balance.csv")
# df = pd.read_csv(r"C:\Users\SERGIUS\Documents\Abraham\Proyecto modular\Archivos CSV\Clientes.csv") # Ya importado
# df = pd.read_csv(r"C:\Users\SERGIUS\Documents\Abraham\Proyecto modular\Archivos CSV\Compras.csv") # Ya importado
# df = pd.read_csv(r"C:\Users\SERGIUS\Documents\Abraham\Proyecto modular\Archivos CSV\Dolar.csv")
# df = pd.read_csv(r"C:\Users\SERGIUS\Documents\Abraham\Proyecto modular\Archivos CSV\Abonos.csv") # Ya importado
# print(df)
# Crear una consulta SQL para insertar los datos
# for _, row in df.iterrows():
# sql = """INSERT INTO Gestion_de_lotes.Lotes (NoManzana, NoLote, Direccion, MtsCuadrados)  # Ya importado
#          VALUES (%s, %s, %s, %s)"""
# sql = """INSERT INTO Gestion_de_lotes.Clientes (IdCliente, Nombre, Domicilio, Telefono) # Ya importado
#          VALUES (%s, %s, %s, %s)"""
# sql = """INSERT INTO Gestion_de_lotes.Dolar (Fecha, Pasivos, PatrimonioNeto, Activos)
#          VALUES (%s, %s)"""
# sql = """INSERT INTO Gestion_de_lotes.Compras (NoManzana, NoLote, CostoPorMetroCuadrado, ImporteTotal, Fecha, IdCliente, FormaDePago) # Ya importado
#          VALUES (%s, %s, %s, %s, %s, %s, %s)"""
# sql = """INSERT INTO Gestion_de_lotes.Balance (Fecha, Pasivos, PatrimonioNeto, Activos)
#          VALUES (%s, %s)"""
# sql = """INSERT INTO Gestion_de_lotes.Abonos (Fecha, NoManzana, NoLote, NoAbono, CantidadAbonada, NoRecibo, Saldo) # Ya importado
#          VALUES (%s, %s, %s, %s, %s, %s, %s)"""

######################################################

# cursor.execute(sql, tuple(row))
# cursor.execute("delete from Gestion_de_lotes.Balance where IdBalance = 1 ")

# Consulta de datos en una tabla.
# consulta = "select * from Gestion_de_lotes.Abonos"
# cursor.execute(consulta)
# info = cursor.fetchall()
# for registro in info:
#     print(registro)

######################################################

# Obtención de un resultado a partir de una operación
# consulta = "SELECT SUM(ImporteTotal) FROM Gestion_de_lotes.Compras"
# # Ejecutar la consulta
# cursor.execute(consulta)
#
# # Obtener el resultado de la suma
# resultado = cursor.fetchone()
#
# # Imprimir el resultado
# print(f"La suma de los importes es: {resultado[0]}")

######################################################


import mysql.connector  # Para la conexión con la base de datos MySQL
from mysql.connector import Error  # Para manejar errores de conexión

# Conectar a la base de datos MySQL
try:
    connection = mysql.connector.connect(
        host='localhost',
        database='gestion_de_lotes',
        user='root',
        password='mysql24$^ui(yuAs'
    )

    if connection.is_connected():  # Si la conexión ha sido exitosa
        cursor = connection.cursor()
        connection.autocommit = False
        # Realizar un cambio en la base de datos
        consulta_update = "UPDATE Gestion_de_lotes.Prueba SET NUMERO2 = 99 WHERE NUMERO1 = 1;"
        cursor.execute(consulta_update)

        # Confirmar temporalmente el cambio para que sea visible
        connection.commit()  # Esto es necesario para que los cambios sean visibles
        print("Cambio ejecutado, presione Enter para ver si el cambio tuvo efecto en la base de datos.")

        # Espera la entrada del usuario
        print("Funciona?")
        input()  # El programa se detendrá hasta que el usuario presione Enter

        # Revertir los cambios, deshacer lo hecho
        connection.rollback()  # Esto revertirá el cambio realizado por el UPDATE

        print("Los cambios han sido revertidos. La base de datos ha vuelto a su estado original.")

        cursor.close()
        connection.close()
        print("Conexión a MySQL cerrada")

except Error as e:
    print("(1)Error al conectar a MySQL", e)
######################################################
# import inspect
#

# class MiClase:
#     def funcion_a(self):
#         self.funcion_compartida()
#
#     def funcion_b(self):
#         self.funcion_compartida()
#
#     def terceras(self):
#         self.funcion_compartida()
#
#     def funcion_compartida(self):
#         llamador = inspect.stack()[1].function
#         if llamador == "funcion_a":
#             print("Código para 'funcion_a'")
#         elif llamador == "funcion_b":
#             print("Código para 'funcion_b'")
#         elif llamador == "terceras":
#             print("Terceras")
#
# obj = MiClase()
# obj.funcion_a()  # Salida: Código para 'funcion_a'
# obj.funcion_b()  # Salida: Código para 'funcion_b'
# obj.terceras()



