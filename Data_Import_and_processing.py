import csv  # Para el manejo de archivos CSV a la hora de importar datos
import subprocess  # Para limpiar la pantalla después de cada operación.
import pandas as pd  # Para el formato de la información a la hora de imprimir detalles de la base de datos
import requests  # Para acceder a la página web Google Finance para obtener el precio del dólar
from bs4 import BeautifulSoup  # Para la revisión y extracción de información de archivos html y xml de páginas web
from datetime import datetime  # Para la extracción de la fecha actual del sistema operativo a la hora de actualizar
# el precio del dólar
import mysql.connector  # Para la conexión con la base de datos MySQL
from mysql.connector import Error  # Para lanzar un mensaje de error en caso de no poder acceder a la base de datos
from Expert_System import ExpertSystem  # Clase del proyecto en donde está el sistema experto
from Payment_Options import PaymentOptions  # Clase del proyecto en donde están las formas posibles de pago


# Funciones básicas

def update_dollar_price(cursor):
    # Actualización del precio del dólar cada vez que se ejecuta el programa

    current_date = datetime.now()  # Fecha y hora actuales
    formatted_date = current_date.strftime("%Y-%m-%d")  # Formateo de la fecha en el formato: Año-Mes-Día
    url = "https://www.google.com/finance/quote/USD-MXN"  # URL de Google Finance para el tipo de cambio USD/MXN
    response = requests.get(url)  # Hacemos una solicitud GET a la página
    if response.status_code == 200:  # Verificamos que la solicitud fue exitosa
        soup = BeautifulSoup(response.content, 'html.parser')  # Parseamos el contenido HTML de la página
        price_element = soup.find('div', {'class': 'YMlKec fxKbKc'})  # Extraemos el valor del tipo de cambio
        # usando el selector adecuado
        if price_element:  # Si efectivamente hay un dato en el campo buscado previamente
            global exchange_rate  # Ponemos la variable en donde se almacena el valor del dólar como global para la
            # inicialización del sistema experto.
            exchange_rate = price_element.text  # Obtenemos el texto del elemento
            print("Actualizando precio del dólar...")
            dollar_price_query = (f"UPDATE gestion_de_lotes.dolar SET Fecha = '{formatted_date}', "
                                  f"PrecioEnPesos = {exchange_rate} LIMIT 1")  # Se actualiza el valor del campo
            # correspondiente de la tabla del dólar en la base de datos
            cursor.execute(dollar_price_query)  # Ejecución de la consulta
            connection.commit()  # Aplicación de los cambios
            # Ruta del archivo CSV del dólar
            dollar_file_route = r'C:\Users\SERGIUS\Documents\Abraham\Proyecto modular\Archivos CSV\Dolar.csv'
            try:
                # Leer el archivo CSV y almacenar las filas
                with open(dollar_file_route, mode='r', newline='') as csv_file:
                    reader_csv = csv.reader(csv_file)
                    rows = list(reader_csv)  # Convertir el contenido a una lista para modificarlo

                # Modificar la primera fila con los nuevos datos
                rows[1] = [formatted_date, exchange_rate]  # Modifica la fila 1 (índice 0 suele ser el encabezado)

                # Escribir el archivo CSV con las filas actualizadas
                with open(dollar_file_route, mode='w', newline='') as csv_file:
                    writer_csv = csv.writer(csv_file)
                    writer_csv.writerows(rows)  # Sobrescribir el archivo con las filas modificadas
                print("Precio del dólar actualizado con éxito en la base de datos y en el CSV.")
            except FileNotFoundError:  # Si el archivo no ha sido encontrado en la ruta especificada
                print("Archivo no encontrado.")  # Impresión del mensaje de error
        else:  # Si no hay un dato en el campo accedido durante el webscraping
            print("No se pudo encontrar el tipo de cambio en la página.")  # Impresión del mensaje correspondiente
    else:  # Si no se pudo acceder a la página
        print(f"Error al acceder a la página: {response.status_code}")  # Impresión del mensaje correspondiente


def sum_of_settled_amounts(cursor):
    # Consulta correspondiente para la suma de los importes finiquitados
    query = "SELECT SUM(PrecioTotal) FROM Gestion_de_lotes.Lotes WHERE Estatus = 'Comprado'"
    cursor.execute(query)  # Ejecutar la consulta
    result = cursor.fetchone()  # Obtener el resultado de la suma
    print(f"Resultado bruto: {result}")  # Impresión del resultado de la consulta
    formatted_result = f"${result[0]:,.2f}"  # Formateo del resultado para que muestre el número con dos decimales
    print(f"La suma de los importes es: {formatted_result}\n")  # Imprimir el resultado
    print("Presione Enter para continuar...")
    input()
    subprocess.call("cls", shell=True)


def sum_of_payments_for_lots_to_be_sold(cursor):
    query = "SELECT SUM(CantidadAbonada) FROM Gestion_de_lotes.Abonos"  # Consulta correspondiente
    cursor.execute(query)  # Ejecutar la consulta
    result = cursor.fetchone()  # Obtener el resultado de la suma
    print(f"Resultado bruto: {result}")  # Impresión del resultado de la consulta
    formatted_result = f"${result[0]:,.2f}"  # Formateo del resultado para que muestre el número con dos decimales
    print(f"La suma de los abonos es: {formatted_result}")  # Imprimir el resultado
    print("Presione Enter para continuar...")
    input()
    subprocess.call("cls", shell=True)


def client_consultation(cursor):
    print("Clientes registrados: \n")  # Impresión informativa
    query = "SELECT IdCliente, Nombre FROM Gestion_de_lotes.Clientes"  # Consulta para imprimir los ID y los nombres
    # de los clientes registrados
    cursor.execute(query)  # Ejecución de la consulta
    info = cursor.fetchall()  # Obtención de cada uno de los registros de la tabla
    for row in info:  # Impresión de cada uno de los registros
        print(row)
    while True:  # Bucle infinito que se cicla cada vez que haya una entrada errónea del usuario
        option = input("\nIngrese el ID del cliente cuya información quiera consultar: ")
        if option.isnumeric():  # Si lo que digitó el usuario es un número
            if int(option) < (len(info) + 1):  # Si el número introducido está en el rango del número
                # disponible de registros en la tabla
                # Consulta auxiliar para imprimir los datos del cliente especificado
                auxQuery = f"SELECT * FROM Gestion_de_lotes.Clientes WHERE IdCliente = {option}"
                cursor.execute(auxQuery)  # Ejecución de la consulta auxiliar
                info = cursor.fetchall()  # Obtención del resultado
                for row in info:  # Impresión de los datos
                    print(row)
                break  # Salida del bucle
            else:  # Si el ID no existe en la tabla
                print("El cliente no existe, intente de nuevo.")  # Impresión del mensaje de error correspondiente
        else:  # Si lo que introdujo el usuario no es un número como tal
            print("Opción no válida. Intente de nuevo.")  # Impresión del mensaje correspondiente
    print("Presione Enter para continuar...")
    input()
    subprocess.call("cls", shell=True)


def lot_consultation(cursor):
    lot_number = input("Introduzca el número de lote: ")  # Preguntar por el número de lote
    block_number = input("Ahora introduzca el número de la manzana en la que se ubica: ")  # Manzana del lote
    # Mostrar la información correspondiente
    query = "SELECT * FROM Gestion_de_lotes.Lotes WHERE NoManzana = " + block_number + " and NoLote = " + lot_number
    cursor.execute(query)  # Ejecución de la consulta
    info = cursor.fetchall()  # Obtención de los datos del lote
    for row in info:  # Impresión de los datos del lote
        print(row)
    print("Presione Enter para continuar...")
    input()
    subprocess.call("cls", shell=True)


# Esta función está nada más para hacer ajustes de información en las bases de datos por si se requiere
def info_adjustment(cursor, connection):
    # Ruta del archivo correspondiente
    df = pd.read_csv(r"C:\Users\SERGIUS\Documents\Abraham\Proyecto modular\Archivos CSV\Lotes.csv")
    print(df)  # Impresión de los datos en formato bruto para confirmar que los datos se leyeron
    for _, row in df.iterrows():  # Bucle para recorrer cada registro
        # Consulta para insertar los datos en la tabla correspondiente
        sql = """INSERT INTO Gestion_de_lotes.Lotes (NoManzana, NoLote, Direccion, MtsCuadrados, CostoMetroCuadrado,
        PrecioTotal, Estatus) VALUES (%s, %s, %s, %s, %s, %s, %s)"""
        cursor.execute(sql, tuple(row))  # Ejecución de la consulta
        connection.commit()  # Guardado de los cambios en la base de datos
    subprocess.call("cls", shell=True)


# En este método se eliminó el parámetro del sistema experto por motivos de diseño
def lot_purchase(cursor):
    print("Lista de lotes disponibles:\n")
    # Consulta para obtener la información de los lotes disponibles
    query = "SELECT * FROM Gestion_de_lotes.Lotes WHERE Estatus = 'Disponible'"
    cursor.execute(query)  # Ejecución de la consulta
    info = cursor.fetchall()  # Obtención de la información
    columns = cursor.column_names  # Obtención de los nombres de las columnas
    column_width = []  # Generación de un arreglo vacío para almacenar el ancho de columna

    for index, column in enumerate(columns):  # Bucle que recorre cada una de las columnas
        # Obtención de la anchura de cada una de las columnas
        max_width = max(len(str(fila[index])) for fila in info) if info else 0
        column_width.append(max(max_width, len(column)))  # Incluir el tamaño obtenido al arreglo

    for index, column in enumerate(columns):  # Segundo bucle para recorrer las columnas
        print(column.ljust(column_width[index]), end="\t")  # Impresión de las columnas ajustando su tamaño
    print()

    for row in info:  # Bucle para recorrer toda la información recolectada por la consulta previa
        for index, data in enumerate(row):  # Bucle anidado para la impresión de los registros
            print(str(data).ljust(column_width[index]), end="\t")  # Impresión de cada registro con el ajuste de tamaño
        print()
    print("\n¿Cuál lote se quiere comprar?")

    # Después de desplegar los lotes se piden los datos correspondientes
    no_manzana = int(input("Introduzca el número de manzana: "))
    no_lote = int(input("Introduzca el número de lote: "))
    # while True:
    #     client = input("Ingrese el nombre del comprador: ")
    #     proceed = input(f"¿Seguro que este es el nombre del comprador?: {client}\nSí <1>     No <Cualquier tecla>")
    #     if proceed == "1":
    #         break
    # Obtención de los detalles del lote de la base de datos mediante la consulta correspondiente
    query = (f"SELECT MtsCuadrados, CostoMetroCuadrado, PrecioTotal FROM Gestion_de_lotes.Lotes WHERE NoManzana = "
             f"{no_manzana} AND NoLote = {no_lote}")
    cursor.execute(query)  # Ejecución de la consulta
    lot_details = cursor.fetchone()  # Se usa fetchone() ya que se busca un lote en específico
    ################################################
    # if lot_details:  # Si hay detalles en el registro especificado
    #     mts_cuadrados, costo_metro_cuadrado, precio_total = lot_details  # Inicialización de las variables restantes
    #     # para el entrenamiento
    #     recommendation = rule_system.recommend_action(no_manzana, no_lote, mts_cuadrados, costo_metro_cuadrado,
    #                                                   precio_total)  # Instancia del sistema experto con cada uno de los
    #     # datos del registro
    #     print("\nRecomendación del sistema experto:")
    #     print(recommendation)  # Dependiendo del precio del dólar se da la recomendación correspondiente
    # else:
    #     # Si el lote que se quiere analizar no se encuentra en la base de datos mostrar el siguiente mensaje
    #     print("Lote no encontrado.")
    ################################################
    proceeding = input("¿Quiere proceder? Sí <1>    No <Cualquier tecla>")
    if proceeding == "1":  # Si se quiere proceder después de saber la recomendación
        while True:  # Bucle infinito que repite la solicitud del precio por metro cuadrado en caso de que se ingrese
            # un dato inválido
            try:
                price_per_square_meter = float(input("¿Cuál es el precio por metro cuadrado que se pactó?: "))
                break
            except ValueError:
                print("Ingrese un número válido.")
        aux_query = "SELECT Nombre FROM Gestion_de_lotes.Clientes"  # Consulta auxiliar para obtener los nombres
        # registrados
        cursor.execute(aux_query)  # Ejecución de la consulta auxiliar
        customer_names = list(cursor.fetchall())
        customer_names_formatted = [element[0] for element in customer_names]  # Conversión de la tupla de nombres
        # a una lista y eliminación de los caracteres indeseados para evitar conflicto en coincidencias
        print("Estos son los clientes registrados: \n")
        print(customer_names_formatted)
        customer_name = input("Ingrese el nombre del cliente: ")  # Ingreso del nombre del cliente
        if customer_name not in customer_names_formatted:  # Si el nombre que se ingresó no está registrado
            print("El cliente no está registrado. ")  # Mensaje de advertencia de que el cliente no está
            # en la base de datos
            address = input("Ingrese su domicilio: ")  # Ingreso del domicilio
            phone_number = input("Ingrese su número de teléfono: ")  # Ingreso del número de teléfono
            # Consulta para insertar los datos del nuevo cliente
            client_insert_query = (f"INSERT INTO Gestion_de_lotes.Clientes (Nombre, Domicilio, Telefono) VALUES "
                                   f"(\"{customer_name}\", \"{address}\", \"{phone_number}\")")
            cursor.execute(client_insert_query)  # Ejecución de la consulta
            connection.commit()  # Guardado de los cambios
            # Consulta para conseguir el ID del cliente que se registró
            id_client_query = f"SELECT IdCliente FROM Gestion_de_lotes.Clientes WHERE Nombre = \"{customer_name}\""
            cursor.execute(id_client_query)  # Ejecución de la consulta
            client_id = cursor.fetchone()[0]  # Guardado del ID mediante el uso de un índice
        else:
            # Consulta para conseguir el ID del cliente en la base de datos
            id_client_query = f"SELECT IdCliente FROM Gestion_de_lotes.Clientes WHERE Nombre = \"{customer_name}\""
            cursor.execute(id_client_query)  # Ejecución de la consulta
            client_id = cursor.fetchone()[0]  # Guardado del ID mediante el uso de un índice
        payment_method = PaymentOptions()  # Se crea un objeto que contiene los modos de pago
        while True:  # Repetir la impresión del submenú hasta que el usuario decida salir
            print("Posibles formas de pago:\n")
            print("De contado              <1>")
            print("Anticipo, parcialidades <2>")
            print("En especie              <3>")
            print("Salir     <Cualquier tecla>\n")
            choice = input("Seleccione uno: ")  # Decisión del usuario
            if choice == "1":  # Si se va a pagar de contado se invoca el método correspondiente de la clase
                payment_method.cash_payment(cursor, no_lote, no_manzana, price_per_square_meter, client_id)
                break
            elif choice == "2":  # Si se va a pagar por abonos se invoca el método correspondiente de la clase
                payment_method.payment_by_installments(cursor, no_lote, no_manzana, price_per_square_meter, client_id)
                break
            elif choice == "3":  # Si se va a pagar en especie se invoca el método correspondiente de la clase
                payment_method.payment_in_kind(cursor, no_lote, no_manzana, price_per_square_meter, client_id)
                break
            else:  # Si el usuario quiere salir el bucle se detendrá y regresará al menú principal
                break

    # # Imprimir los nombres de las columnas
    # print("\t".join(columnas))  # Usamos '\t' para separar por tabulación
    # # Imprimir las filas de la tabla sin paréntesis ni comas
    # for fila in info:
    #     fila_sin_comas = "\t".join(map(str, fila))  # Convertimos a cadena y separamos por tabulación
    #     print(fila_sin_comas)
    print("Presione Enter para continuar...")
    input()
    subprocess.call("cls", shell=True)


def balance_consultation(cursor):
    print("---------Consulta de saldo--------")
    # Solicitud de los datos necesarios
    lot_number = input("Introduzca el número de lote: ")
    block_number = input("Ahora introduzca el número de la manzana en la que se ubica: ")
    # Consulta correspondiente
    query = ("SELECT Saldo FROM Gestion_de_lotes.Abonos WHERE NoManzana = " + block_number + " and NoLote = " +
             lot_number + " and NoAbono = (SELECT MAX(NoAbono) FROM Gestion_de_lotes.Abonos WHERE NoManzana = " +
             block_number + " and NoLote = " + lot_number + ")")  # Dentro de esta consulta hay una sub-consulta
    # que obtiene el saldo actual del lote en proceso de compra
    cursor.execute(query)  # Ejecución de la consulta
    balance = cursor.fetchone()  # Se obtiene el dato, es decir, el monto faltante a pagar para liquidar la compra y
    # luego se imprime
    print("El saldo del lote número " + lot_number + " de la manzana " + block_number + " es: $" + balance[0])
    print("Presione Enter para continuar...")
    input()
    subprocess.call("cls", shell=True)


def main_menu(cursor):
    # rule_system = ExpertSystem(float(exchange_rate))  # Instancia del sistema experto
    # # Cada vez que se ejecuta el programa se entrena el sistema experto con los datos dentro del archivo Lotes.csv
    # rule_system.train_model(r"C:\Users\SERGIUS\Documents\Abraham\Proyecto modular\Archivos CSV\Lotes.csv")
    while True:  # Bucle infinito que se ejecuta hasta que el usuario quiera salir del programa
        print("\n\nIniciar la compra de lote: (1)")
        print("Consultar un lote: (2)")
        print("Consultar la sumatoria de los importes finiquitados: (3)")
        print("Consultar la sumatoria de los abonos de los lotes en proceso de compra: (4)")
        print("Consultar el saldo de un lote: (5)")
        print("Consultar los datos de un cliente: (6)")
        print("Modificar el dato de algún registro: (7)")
        print("Salir (Cualquier tecla)\n")
        election = input("Seleccione la operación que quiera realizar: ")
        if election == "1":  # Si se quiere registrar la compra de un lote se llama a la función "compra de lote"
            lot_purchase(cursor)
            subprocess.call("cls", shell=True)
        elif election == "2":  # Si se quiere consultar los datos de un lote en específico se llama a la función
            # "Consulta de lote"
            lot_consultation(cursor)
            subprocess.call("cls", shell=True)
        elif election == "3":  # Si se quiere consultar la sumatoria de los montos de los lotes ya comprados se llama
            # a la función "Sumatoria de montos finiquitados"
            sum_of_settled_amounts(cursor)
            subprocess.call("cls", shell=True)
        elif election == "4":  # Si se quiere consultar la sumatoria de los abonos de los lotes en proceso de compra
            # se llama a la función correspondiente
            sum_of_payments_for_lots_to_be_sold(cursor)
            subprocess.call("cls", shell=True)
        elif election == "5":  # Si se quiere consultar el saldo de un lote en proceso de compra se llama a la función
            # "Consulta de saldo"
            balance_consultation(cursor)
            subprocess.call("cls", shell=True)
        elif election == "6":  # Si se quiere consultar los datos de un cliente en específico se llama a la función
            # "Consulta de cliente"
            client_consultation(cursor)
            subprocess.call("cls", shell=True)
        else:
            break


def SQL_connection():
    # Conectar a la base de datos MySQL
    return mysql.connector.connect(
        host='localhost',
        database='gestion_de_lotes',
        user='root',
        password='mysql24$^ui(yuAs'
    )


def get_connection():
    global connection
    if not connection.is_connected():
        connection = SQL_connection()
    return connection


#################################################

try:
    connection = SQL_connection()
    connection.autocommit = False
except Error as e:
    print("(1)Error al conectar a MySQL", e)

if __name__ == "__main__":
    if connection.is_connected():  # Si la conexión ha sido exitosa
        cursor = connection.cursor()  #
        # ajuste_de_informacion(cursor, connection)
        update_dollar_price(cursor)
        main_menu(cursor)

        # Confirmar los cambios en la base de datos
        connection.commit()
        cursor.close()
        connection.close()
        print("Conexión a MySQL cerrada")
