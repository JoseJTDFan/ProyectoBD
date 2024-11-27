import pyodbc

SERVER_NAME = "RAYO\SQLEXPRESS"
DATABASE_NAME = "Ecommerce"
USER = "user"
PASSWORD = "1234"

def getTop5Categorias():
    try:
        connection = pyodbc.connect(f'DRIVER={{SQL Server}};SERVER={SERVER_NAME};DATABASE={DATABASE_NAME};UID={USER};PWD={PASSWORD}')
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
        connection = pyodbc.connect(f'DRIVER={{SQL Server}};SERVER={SERVER_NAME};DATABASE={DATABASE_NAME};UID={USER};PWD={PASSWORD}')
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
        connection = pyodbc.connect(f'DRIVER={{SQL Server}};SERVER={SERVER_NAME};DATABASE={DATABASE_NAME};UID={USER};PWD={PASSWORD}')
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
        connection = pyodbc.connect(f'DRIVER={{SQL Server}};SERVER={SERVER_NAME};DATABASE={DATABASE_NAME};UID={USER};PWD={PASSWORD}')
        cursor = connection.cursor()
        cursor.execute("EXEC ObtenerCategorias")
        rows = cursor.fetchall()
        return rows
    except Exception as ex:
        print("Error durante la conexión: {}".format(ex))
    finally:
        connection.close()

def getNombresMarcas():
    try:
        connection = pyodbc.connect(f'DRIVER={{SQL Server}};SERVER={SERVER_NAME};DATABASE={DATABASE_NAME};UID={USER};PWD={PASSWORD}')
        cursor = connection.cursor()
        cursor.execute("EXEC ObtenerMarcas")
        rows = cursor.fetchall()
        return rows
    except Exception as ex:
        print("Error durante la conexión: {}".format(ex))
    finally:
        connection.close()

def getProductos(num):
    try:
        connection = pyodbc.connect(f'DRIVER={{SQL Server}};SERVER={SERVER_NAME};DATABASE={DATABASE_NAME};UID={USER};PWD={PASSWORD}')
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
        connection = pyodbc.connect(f'DRIVER={{SQL Server}};SERVER={SERVER_NAME};DATABASE={DATABASE_NAME};UID={USER};PWD={PASSWORD}')
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
        connection = pyodbc.connect(f'DRIVER={{SQL Server}};SERVER={SERVER_NAME};DATABASE={DATABASE_NAME};UID={USER};PWD={PASSWORD}')
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
        connection = pyodbc.connect(f'DRIVER={{SQL Server}};SERVER={SERVER_NAME};DATABASE={DATABASE_NAME};UID={USER};PWD={PASSWORD}')
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

def actualizarUsuario(
    id_usuario, nombre, apellido, correo_electronico, contrasena, 
    telefono, tipo_usuario, estado, direccion_envio
):
    connection = None
    try:
        # Connect to SQL Server
        connection = pyodbc.connect(
            'DRIVER={SQL Server};SERVER=WINDOWS-0GERP4M;DATABASE=Ecommerce;UID=user;PWD=1234'
        )
        cursor = connection.cursor()

        # Call the stored procedure
        cursor.execute(
            "EXEC spActualizarUsuario @id_usuario = ?, @nombre = ?, @apellido = ?, @correo_electronico = ?, "
            "@contrasena = ?, @telefono = ?, @tipo_usuario = ?, @estado = ?, @direccion_envio = ?",
            id_usuario, nombre, apellido, correo_electronico, contrasena,
            telefono, tipo_usuario, estado, direccion_envio
        )
        
        # Commit changes
        connection.commit()

        return {"success": True, "message": "User updated successfully"}
    except Exception as ex:
        print(f"Error during the operation: {ex}")
        return {"success": False, "message": f"Error: {ex}"}
    finally:
        if connection:
            connection.close()

def crearUsuario(nombre, apellido, correo_electronico, contrasena, telefono, tipo, direccion):
    try:
        # Conexión a la base de datos
        connection = pyodbc.connect(f'DRIVER={{SQL Server}};SERVER={SERVER_NAME};DATABASE={DATABASE_NAME};UID={USER};PWD={PASSWORD}')
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



def registrarMarca(nombre, descripcion):
    try:
        connection = pyodbc.connect(f'DRIVER={{SQL Server}};SERVER={SERVER_NAME};DATABASE={DATABASE_NAME};UID={USER};PWD={PASSWORD}')
        cursor = connection.cursor()
        cursor.execute("EXEC spRegistrarMarca @nombre = ?, @descripcion = ?", nombre, descripcion)
        connection.commit()
    except Exception as ex:
        print("Error durante la conexión: {}".format(ex))
    finally:
        if 'connection' in locals():
            connection.close()




def getReseñasPorProducto(id_producto):
    try:
        # Conexión a la base de datos
        connection = pyodbc.connect(f'DRIVER={{SQL Server}};SERVER={SERVER_NAME};DATABASE={DATABASE_NAME};UID={USER};PWD={PASSWORD}')
        cursor = connection.cursor()
        cursor.execute("EXEC spObtenerReseñasPorProducto ?", id_producto)
        rows = cursor.fetchall()
        reseñas = []
        for row in rows:
            reseñas.append({
                'producto': row[0],
                'usuario': row[1]+" "+row[2],
                'calificacion': row[3],
                'comentario': row[4],
                'fecha_reseña': row[5]
            })
        return reseñas
    except Exception as ex:
        print(f"Error durante la conexión: {ex}")
        return []
    finally:
        if 'connection' in locals():
            connection.close()

def getProductosFiltrados(precio_min, precio_max, categoria, marca, calif_min, calif_max):
    try:
        # Conexión a la base de datos
        connection = pyodbc.connect(f'DRIVER={{SQL Server}};SERVER={SERVER_NAME};DATABASE={DATABASE_NAME};UID={USER};PWD={PASSWORD}')
        cursor = connection.cursor()
        
        # Ejecución del procedimiento almacenado
        cursor.execute("""
            EXEC [dbo].[ObtenerProductosFiltrados] 
            @PrecioMin = ?, 
            @PrecioMax = ?, 
            @IdCategoria = ?, 
            @IdMarca = ?, 
            @CalifMin = ?, 
            @CalifMax = ?;
        """, (precio_min, precio_max, categoria, marca, calif_min, calif_max))
        
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
        print("Error durante la ejecución: {}".format(ex))
    finally:
        if 'connection' in locals() and connection:
            connection.close()


def getMarcas():
    try:
        connection = pyodbc.connect(f'DRIVER={{SQL Server}};SERVER={SERVER_NAME};DATABASE={DATABASE_NAME};UID={USER};PWD={PASSWORD}')
        cursor = connection.cursor()
        cursor.execute("EXEC ObtenerMarcas")
        result = cursor.fetchall()
        return result
    except Exception as ex:
        print("Error durante la conexión: {}".format(ex))
        return []
    finally:
        if 'connection' in locals():
            connection.close()

def getMarcaById(id):
    try:
        connection = pyodbc.connect(f'DRIVER={{SQL Server}};SERVER={SERVER_NAME};DATABASE={DATABASE_NAME};UID={USER};PWD={PASSWORD}')
        cursor = connection.cursor()
        cursor.execute("SELECT id, nombre, descripcion FROM Marcas WHERE id = ?", id)
        row = cursor.fetchone()
        if row:
            return {
                'id': row[0],
                'nombre': row[1],
                'descripcion': row[2]
            }
        return None
    except Exception as ex:
        print("Error durante la conexión: {}".format(ex))
    finally:
        if 'connection' in locals():
            connection.close()

def actualizarMarca(idMarca, nombre, descripcion):
    try:
        connection = pyodbc.connect(f'DRIVER={{SQL Server}};SERVER={SERVER_NAME};DATABASE={DATABASE_NAME};UID={USER};PWD={PASSWORD}')
        cursor = connection.cursor()
        cursor.execute("EXEC spActualizarMarca @idMarca = ?, @nombre = ?, @descripcion = ?", idMarca, nombre, descripcion)
        connection.commit()
    except Exception as ex:
        print("Error durante la conexión: {}".format(ex))
    finally:
        if 'connection' in locals():
            connection.close()
            
def getUsuarios():
    try:
        connection = pyodbc.connect(f'DRIVER={{SQL Server}};SERVER={SERVER_NAME};DATABASE={DATABASE_NAME};UID={USER};PWD={PASSWORD}')
        cursor = connection.cursor()
        cursor.execute("exec [dbo].[spLeerUsuarios]")
        rows = cursor.fetchall()
        return rows
    except Exception as ex:
        print("Error durante la conexión: {}".format(ex))
    finally:
        connection.close()

def obtenerOCrearCarrito(id_usuario):
    import pyodbc
    try:
        # Conexión a la base de datos
        connection = pyodbc.connect(f'DRIVER={{SQL Server}};SERVER={SERVER_NAME};DATABASE={DATABASE_NAME};UID={USER};PWD={PASSWORD}')
        cursor = connection.cursor()

        # Ejecutar el procedimiento almacenado
        cursor.execute("""
            EXEC sp_RevisarOCrearCarrito @idUsuario = ?;
        """, (id_usuario,))  # Usa una tupla incluso para un solo parámetro

        # Obtener el resultado
        result = cursor.fetchone()

        # Verificar si hay un resultado
        if result:
            id_carrito = result[0]  # El idCarrito es el primer valor de la tupla
            print(f"Carrito ID: {id_carrito}")
            return id_carrito
        else:
            print("No se obtuvo un resultado del procedimiento almacenado.")
            return None
    except pyodbc.Error as ex:
        print(f"Error durante la conexión o ejecución: {ex}")
        return None
    finally:
        if 'connection' in locals():
            connection.close()

obtenerOCrearCarrito(1)