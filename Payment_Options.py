from datetime import datetime
import inspect


class PaymentOptions:
    # def __init__(self):
    #     pass

    @staticmethod
    def cash_payment(cursor, lote, manzana, sqm_price, client_id):
        # Consulta para obtener los metros cuadrados del lote a comprar
        lot_data_query = f"SELECT MtsCuadrados FROM gestion_de_lotes.Lotes WHERE NoManzana = {manzana} AND NoLote = {lote}"
        cursor.execute(lot_data_query)  # Ejecución de la consulta
        square_meters = cursor.fetchone()[0]  # Obtención del dato usando un índice
        lot_price = sqm_price * float(square_meters)  # Multiplicación del costo por metro cuadrado por los metros
        # cuadrados del lote para obtener el precio total
        print(lot_price)
        payment = float(input("¿Cuánto se pagó? Ingrese la cantidad: "))  # Ingreso de la cantidad de dinero que se pagó
        print(f"Cambio: ${payment - lot_price} pesos")  # Cantidad de dinero excedente
        from Data_Import_and_processing import get_connection  # Se importa la instancia de la conexión de la base de
        # datos para el guardado de los cambios
        connection = get_connection()
        connection.autocommit = False
        # aux_cursor = connection.cursor() ??????
        # Consulta para actualizar el registro del lote a comprar: se almacena el costo por metro cuadrado que se
        # pactó, el precio total resultante de la multiplicación previa y el cambio del estatus a "comprado"
        lot_edition_query = (f"UPDATE gestion_de_lotes.Lotes SET CostoMetroCuadrado = {sqm_price}, PrecioTotal = "
                             f"{lot_price}, Estatus = 'Comprado' WHERE NoManzana = {manzana} AND NoLote = {lote}")
        cursor.execute(lot_edition_query)  # Ejecución de la consulta
        connection.commit()  # Guardado de los cambios
        PaymentOptions.purchase_table_row_insertion(connection, cursor, lote, manzana, sqm_price, client_id)
        print("Presione enter")
        input()
        connection.rollback()
        print("Operación hecha.")

    @staticmethod
    def payment_by_installments(cursor, lote, manzana, sqm_price, client_id):
        while True:
            try:
                partial_payment = float(input("Ingrese el anticipo que se pagó: $"))
                break
            except ValueError:
                print("Ingrese una cantidad válida.")
        current_date = datetime.now()  # Fecha y hora actuales
        formatted_date = current_date.strftime("%Y-%m-%d")  # Formateo de la fecha en el formato: Año-Mes-Día
        # query = (f"INSERT INTO gestion_de_lotes.Abonos (Fecha, NoManzana, NoLote, NoAbono, CantidadAbonada, NoRecibo, "
        #          f"Saldo) VALUES ({formatted_date}, {manzana}, {lote}, {}, {}, {}, {})")

        from Data_Import_and_processing import connection  # Se importa la instancia de la conexión de la base de datos
        # para el guardado de los cambios
        PaymentOptions.purchase_table_row_insertion(connection, cursor, lote, manzana, sqm_price, client_id)

    @staticmethod
    def payment_in_kind(cursor, lote, manzana, sqm_price, client_id):
        from Data_Import_and_processing import connection  # Se importa la instancia de la conexión de la base de datos
        # para el guardado de los cambios
        PaymentOptions.purchase_table_row_insertion(connection, cursor, lote, manzana, sqm_price, client_id)

    @staticmethod
    def purchase_table_row_insertion(connection, cursor, lote, manzana, sqm_price, client_id):
        caller = inspect.stack()[1].function
        if caller == "cash_payment":
            print("Cash payment")
        elif caller == "payment_by_installments":
            print("Payment by installments")
        elif caller == "payment_in_kind":
            print("Payment in kind")

        purchase_edition_query = f"UPDATE gestion_de_lotes.Compras"
