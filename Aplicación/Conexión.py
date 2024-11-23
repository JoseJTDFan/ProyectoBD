import pyodbc

def prueba():
    try:
        connection = pyodbc.connect('DRIVER={SQL Server};SERVER=WINDOWS-0GERP4M;DATABASE=Ecommerce;UID=user;PWD=1234')
        print("Conexión exitosa.")
        cursor = connection.cursor()
        cursor.execute("SELECT @@version;")
        row = cursor.fetchone()
        print("Versión del servidor de SQL Server: {}".format(row))
        cursor.execute("SELECT * FROM Marcas")
        rows = cursor.fetchall()
        for row in rows:
            print(row)
    except Exception as ex:
        print("Error durante la conexión: {}".format(ex))
    finally:
        connection.close()  # Se cerró la conexión a la BD.
        print("La conexión ha finalizado.")

def getTop5Categorias():
    try:
        connection = pyodbc.connect('DRIVER={SQL Server};SERVER=WINDOWS-0GERP4M;DATABASE=Ecommerce;UID=user;PWD=1234')
        cursor = connection.cursor()
        cursor.execute("EXEC ObtenerTop5Categorias")
        rows = cursor.fetchall()
        lista=[]
        for row in rows:
           lista.append(row[0])
        return lista
    except Exception as ex:
        print("Error durante la conexión: {}".format(ex))
    finally:
        connection.close()

def getPromocionesInicio():
    try:
        connection = pyodbc.connect('DRIVER={SQL Server};SERVER=WINDOWS-0GERP4M;DATABASE=Ecommerce;UID=user;PWD=1234')
        cursor = connection.cursor()
        cursor.execute("EXEC ObtenerPromocionInicio")
        rows = cursor.fetchall()
        lista=[]
        for row in rows:
            lista.append({
                'nombre': row[0],
                'precio': float(row[1]),  # Convertir Decimal a float
                'descuento': float(row[2]),  # Convertir Decimal a float
                'fecha': row[3].strftime('%d/%m/%Y'),  # Formatear fecha
                'imagen': row[4]
            })
        return lista
    except Exception as ex:
        print("Error durante la conexión: {}".format(ex))
    finally:
        connection.close()

def validarUsuario(correo,contrasena):
    try:
        connection = pyodbc.connect('DRIVER={SQL Server};SERVER=WINDOWS-0GERP4M;DATABASE=Ecommerce;UID=user;PWD=1234')
        cursor = connection.cursor()
        cursor.execute("EXEC ValidarUsuario @correo_electronico = ?, @contrasena = ?", correo, contrasena)
        result = cursor.fetchone()
        if result:
            return result
        else:
            return False
    except Exception as ex:
        print("Error durante la conexión: {}".format(ex))
    finally:
        connection.close()