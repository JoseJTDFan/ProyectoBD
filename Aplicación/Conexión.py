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

def getNombresCategorias():
    try:
        connection = pyodbc.connect('DRIVER={SQL Server};SERVER=WINDOWS-0GERP4M;DATABASE=Ecommerce;UID=user;PWD=1234')
        cursor = connection.cursor()
        cursor.execute("EXEC ObtenerCategorias")
        rows = cursor.fetchall()
        lista=[]
        for row in rows:
           lista.append(row[0])
        return lista
    except Exception as ex:
        print("Error durante la conexión: {}".format(ex))
    finally:
        connection.close()

def getNombresMarcas():
    try:
        connection = pyodbc.connect('DRIVER={SQL Server};SERVER=WINDOWS-0GERP4M;DATABASE=Ecommerce;UID=user;PWD=1234')
        cursor = connection.cursor()
        cursor.execute("EXEC ObtenerMarcas")
        rows = cursor.fetchall()
        lista=[]
        for row in rows:
           lista.append(row[0])
        return lista
    except Exception as ex:
        print("Error durante la conexión: {}".format(ex))
    finally:
        connection.close()

def getOfertas():
    try:
        connection = pyodbc.connect('DRIVER={SQL Server};SERVER=WINDOWS-0GERP4M;DATABASE=Ecommerce;UID=user;PWD=1234')
        cursor = connection.cursor()
        cursor.execute("EXEC ObtenerOfertas")
        rows = cursor.fetchall()
        lista=[]
        for row in rows:
            lista.append({
                'id': row[0],
                'nombre': row[1],
                'precio': float(row[2]),  # Convertir Decimal a float
                'descuento': float(row[3]),  # Convertir Decimal a float
                'imagen': row[4]
            })
        return lista
    except Exception as ex:
        print("Error durante la conexión: {}".format(ex))
    finally:
        connection.close()

def getProductoSinOferta():
    try:
        connection = pyodbc.connect('DRIVER={SQL Server};SERVER=WINDOWS-0GERP4M;DATABASE=Ecommerce;UID=user;PWD=1234')
        cursor = connection.cursor()
        cursor.execute("EXEC ObtenerProductoSinOferta")
        rows = cursor.fetchall()
        lista=[]
        for row in rows:
            lista.append({
                'id': row[0],
                'nombre': row[1],
                'precio': float(row[2]),  # Convertir Decimal a float
                'imagen': row[3]
            })
        return lista
    except Exception as ex:
        print("Error durante la conexión: {}".format(ex))
    finally:
        connection.close()

def getProductos(num):
    try:
        connection = pyodbc.connect('DRIVER={SQL Server};SERVER=WINDOWS-0GERP4M;DATABASE=Ecommerce;UID=user;PWD=1234')
        cursor = connection.cursor()
        cursor.execute("EXEC ObtenerProductosPaginados @PageNumber=?",  (num))
        rows = cursor.fetchall()
        lista=[]
        for row in rows:
            lista.append({
                'id': row[0],
                'nombre': row[1],
                'precio': float(row[2]),  # Convertir Decimal a float
                'descuento': float(row[3]),  # Convertir Decimal a float
                'imagen': row[4],
                'tienedesc': row[5]
            })
        return lista
    except Exception as ex:
        print("Error durante la conexión: {}".format(ex))

    finally:
        connection.close()

def getUsuario(id):
    try:
        connection = pyodbc.connect('DRIVER={SQL Server};SERVER=WINDOWS-0GERP4M;DATABASE=Ecommerce;UID=user;PWD=1234')
        cursor = connection.cursor()
        cursor.execute("EXEC spBuscarUsuario @id = ?", id)
        result = cursor.fetchone()
        if result:
            return result
        else:
            return False
    except Exception as ex:
        print("Error durante la conexión: {}".format(ex))
    finally:
        connection.close()

def getTotalProductos():
    try:
        connection = pyodbc.connect('DRIVER={SQL Server};SERVER=WINDOWS-0GERP4M;DATABASE=Ecommerce;UID=user;PWD=1234')
        cursor = connection.cursor()
        cursor.execute("EXEC obtenerTotalProductos")
        result = cursor.fetchone()
        return result[0]
    except Exception as ex:
        print("Error durante la conexión: {}".format(ex))
    finally:
        connection.close()

def getProductoDetalle(producto_id):
    connection = None
    try:
        connection = pyodbc.connect('DRIVER={SQL Server};SERVER=WINDOWS-0GERP4M;DATABASE=Ecommerce;UID=user;PWD=1234')
        cursor = connection.cursor()
        cursor.execute("EXEC spLeerProductoPorId @idProducto = ?", producto_id)
        row = cursor.fetchone()
        if row:
            return {
                'id': row[0],
                'Codigo': row[1],
                'nombre': row[2],
                'Categoria': row[3],
                'Marca': row[4],
                'precio': float(row[6]),
                'Stock': row[7],
                'popularidad': row[10],
                'descripcion': row[11],
                'imagen': row[12]
            }
        else:
            return False
    except Exception as ex:
        print("Error durante la conexión: {}".format(ex))
        return None
    finally:
        connection.close()

def crearUsuario(nombre, apellido, correo_electronico, contrasena, telefono, tipo, direccion):
    try:
        # Conexión a la base de datos
        connection = pyodbc.connect('DRIVER={SQL Server};SERVER=WINDOWS-0GERP4M;DATABASE=Ecommerce;UID=user;PWD=1234')
        cursor = connection.cursor()
        
        # Ejecución del procedimiento almacenado
        cursor.execute("""
            EXEC spCrearUsuario 
            @nombre = ?, 
            @apellido = ?, 
            @correo_electronico = ?, 
            @contrasena = ?, 
            @telefono = ?, 
            @tipo_usuario = ?, 
            @direccion_envio = ?
        """, (nombre, apellido, correo_electronico, contrasena, telefono, tipo, direccion))
        
        # Confirmar los cambios
        connection.commit()
        print("Usuario creado exitosamente.")
        return True
    except Exception as ex:
        print("Error durante la ejecución: {}".format(ex))
        return False
    finally:
        if 'connection' in locals() and connection:
            connection.close()