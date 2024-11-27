import pyodbc

SERVER_NAME = ""
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

def getProductosSimilares(categoria, idproducto):
    try:
        connection = pyodbc.connect(f'DRIVER={{SQL Server}};SERVER={SERVER_NAME};DATABASE={DATABASE_NAME};UID={USER};PWD={PASSWORD}')
        cursor = connection.cursor()
        cursor.execute("EXEC spObtenerProductosSimilares @categoria = ?, @idproducto = ?",  (categoria, idproducto))
        rows = cursor.fetchall()
        lista=[]
        for row in rows:
            print(row)
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

def getUsuarios():
    try:
        connection = pyodbc.connect(f'DRIVER={{SQL Server}};SERVER={SERVER_NAME};DATABASE={DATABASE_NAME};UID={USER};PWD={PASSWORD}')
        cursor = connection.cursor()
        cursor.execute("EXEC spLeerUsuarios")
        rows = cursor.fetchall()
        return rows
    except Exception as ex:
        print("Error durante la conexión: {}".format(ex))
        return []
    finally:
        if 'connection' in locals():
            connection.close()

def obtenerOCrearCarrito(id_usuario):
    import pyodbc
    try:
        # Conexión a la base de datos
        connection = pyodbc.connect(f'DRIVER={{SQL Server}};SERVER={SERVER_NAME};DATABASE={DATABASE_NAME};UID={USER};PWD={PASSWORD}')
        cursor = connection.cursor()
        cursor.execute("EXEC spCrearCarrito @idUsuario = ?", (id_usuario,))
        connection.commit()
        print("Carrito creado exitosamente.")
        return True

    except pyodbc.Error as ex:
        print(f"Error al conectar o ejecutar el procedimiento: {ex}")
        return False

    finally:
        if 'connection' in locals():
            connection.close()

def obtenerCarrito(idUsuario):
    try:
        connection = pyodbc.connect(f'DRIVER={{SQL Server}};SERVER={SERVER_NAME};DATABASE={DATABASE_NAME};UID={USER};PWD={PASSWORD}')
        cursor = connection.cursor()
        cursor.execute("EXEC [dbo].[spObtenerCarrito] @idUsuario = ?", idUsuario)
        result = cursor.fetchone()
        if result:
            return result
        else:
            return False
    except Exception as ex:
        print("Error durante la conexión: {}".format(ex))
    finally:
        connection.close()

def añadirProducto(id, idCarrito, cantidad):
    try:
        connection = pyodbc.connect(f'DRIVER={{SQL Server}};SERVER={SERVER_NAME};DATABASE={DATABASE_NAME};UID={USER};PWD={PASSWORD}')
        cursor = connection.cursor()
        cursor.execute("EXEC [dbo].[spAgregarDetalleCarrito] @idProducto = ?, @idCarrito = ?, @cantidad = ?", 
                       (id, idCarrito, cantidad))
        connection.commit()
        if cursor.rowcount > 0:
            print("Producto añadido exitosamente.")
            return True
        else:
            print("No se pudo añadir el producto.")
            return False
    except pyodbc.Error as ex:  # Error específico de la base de datos
        print("Error durante la ejecución: {}".format(ex))
        return False
    except Exception as ex:  # Otros errores de Python
        print("Error durante la conexión o ejecución: {}".format(ex))
        return False
    finally:
        if 'connection' in locals():
            connection.close()



def eliminarMarca(idMarca):
    try:
        connection = pyodbc.connect(f'DRIVER={{SQL Server}};SERVER={SERVER_NAME};DATABASE={DATABASE_NAME};UID={USER};PWD={PASSWORD}')
        cursor = connection.cursor()
        cursor.execute("EXEC spEliminarMarca @idMarca = ?", idMarca)
        connection.commit()
    except Exception as ex:
        print("Error durante la conexión: {}".format(ex))
    finally:
        if 'connection' in locals():
            connection.close()



def getCategorias():
    try:
        connection = pyodbc.connect(f'DRIVER={{SQL Server}};SERVER={SERVER_NAME};DATABASE={DATABASE_NAME};UID={USER};PWD={PASSWORD}')
        cursor = connection.cursor()
        cursor.execute("EXEC spObtenerCategorias")
        result = cursor.fetchall()
        return result
    except Exception as ex:
        print("Error durante la conexión: {}".format(ex))
        return []
    finally:
        if 'connection' in locals():
            connection.close()

def registrarCategoria(nombre, descripcion):
    try:
        connection = pyodbc.connect(f'DRIVER={{SQL Server}};SERVER={SERVER_NAME};DATABASE={DATABASE_NAME};UID={USER};PWD={PASSWORD}')
        cursor = connection.cursor()
        cursor.execute("EXEC spRegistrarCategoria @nombre = ?, @descripcion = ?", nombre, descripcion)
        connection.commit()
    except Exception as ex:
        print("Error durante la conexión: {}".format(ex))
    finally:
        if 'connection' in locals():
            connection.close()

def actualizarCategoria(idCategoria, nombre, descripcion):
    try:
        connection = pyodbc.connect(f'DRIVER={{SQL Server}};SERVER={SERVER_NAME};DATABASE={DATABASE_NAME};UID={USER};PWD={PASSWORD}')
        cursor = connection.cursor()
        cursor.execute("EXEC spActualizarCategoria @idCategoria = ?, @nombre = ?, @descripcion = ?", idCategoria, nombre, descripcion)
        connection.commit()
    except Exception as ex:
        print("Error durante la conexión: {}".format(ex))
    finally:
        if 'connection' in locals():
            connection.close()

def eliminarCategoria(idCategoria):
    try:
        connection = pyodbc.connect(f'DRIVER={{SQL Server}};SERVER={SERVER_NAME};DATABASE={DATABASE_NAME};UID={USER};PWD={PASSWORD}')
        cursor = connection.cursor()
        cursor.execute("EXEC spEliminarCategoria @idCategoria = ?", idCategoria)
        connection.commit()
    except Exception as ex:
        print("Error durante la conexión: {}".format(ex))
    finally:
        if 'connection' in locals():
            connection.close()

def eliminarUsuario(idUsuario):
    try:
        connection = pyodbc.connect(f'DRIVER={{SQL Server}};SERVER={SERVER_NAME};DATABASE={DATABASE_NAME};UID={USER};PWD={PASSWORD}')
        cursor = connection.cursor()
        cursor.execute("EXEC spEliminarUsuario @idUsuario = ?", idUsuario)
        connection.commit()
    except Exception as ex:
        print("Error durante la conexión: {}".format(ex))
    finally:
        if 'connection' in locals():
            connection.close()


def modificarUsuario(idUsuario, nombre, apellido, correo, telefono, direccion):
    try:
        connection = pyodbc.connect(f'DRIVER={{SQL Server}};SERVER={SERVER_NAME};DATABASE={DATABASE_NAME};UID={USER};PWD={PASSWORD}')
        cursor = connection.cursor()
        cursor.execute("EXEC spActualizarUsuario @idUsuario = ?, @nombre = ?, @apellido = ?, @correo = ?, @telefono = ?, @direccion = ?", idUsuario, nombre, apellido, correo, telefono, direccion)
        connection.commit()
    except Exception as ex:
        print("Error durante la conexión: {}".format(ex))
    finally:
        if 'connection' in locals():
            connection.close()


def getProductoss():
    try:
        connection = pyodbc.connect(f'DRIVER={{SQL Server}};SERVER={SERVER_NAME};DATABASE={DATABASE_NAME};UID={USER};PWD={PASSWORD}')
        cursor = connection.cursor()
        cursor.execute("EXEC spObtenerProductos")
        result = cursor.fetchall()
        return result
    except Exception as ex:
        print("Error durante la conexión: {}".format(ex))
        return []
    finally:
        if 'connection' in locals():
            connection.close()



def registrarProducto(codigo_producto, nombre, descripcion, precio, stock, idCategoria, idMarca):
    try:
        connection = pyodbc.connect(f'DRIVER={{SQL Server}};SERVER={SERVER_NAME};DATABASE={DATABASE_NAME};UID={USER};PWD={PASSWORD}')
        cursor = connection.cursor()
        cursor.execute("EXEC spRegistrarProducto @codigo_producto = ?, @nombre = ?, @descripcion = ?, @precio = ?, @stock = ?, @idCategoria = ?, @idMarca = ?", codigo_producto, nombre, descripcion, precio, stock, idCategoria, idMarca)
        connection.commit()
    except Exception as ex:
        print("Error durante la conexión: {}".format(ex))
    finally:
        if 'connection' in locals():
            connection.close()
            
def actualizarProducto(idProducto, nombre, descripcion, precio, stock, idCategoria, idMarca):
    try:
        connection = pyodbc.connect(f'DRIVER={{SQL Server}};SERVER={SERVER_NAME};DATABASE={DATABASE_NAME};UID={USER};PWD={PASSWORD}')
        cursor = connection.cursor()
        cursor.execute("EXEC spActualizarProducto @idProducto = ?, @nombre = ?, @descripcion = ?, @precio = ?, @stock = ?, @idCategoria = ?, @idMarca = ?", idProducto, nombre, descripcion, precio, stock, idCategoria, idMarca)
        connection.commit()
    except Exception as ex:
        print("Error durante la conexión: {}".format(ex))
    finally:
        if 'connection' in locals():
            connection.close()

def eliminarProducto(idProducto):
    try:
        connection = pyodbc.connect(f'DRIVER={{SQL Server}};SERVER={SERVER_NAME};DATABASE={DATABASE_NAME};UID={USER};PWD={PASSWORD}')
        cursor = connection.cursor()
        cursor.execute("EXEC spEliminarProducto @idProducto = ?", idProducto)
        connection.commit()
    except Exception as ex:
        print("Error durante la conexión: {}".format(ex))
    finally:
        if 'connection' in locals():
            connection.close()



def getPromociones():
    try:
        connection = pyodbc.connect(f'DRIVER={{SQL Server}};SERVER={SERVER_NAME};DATABASE={DATABASE_NAME};UID={USER};PWD={PASSWORD}')
        cursor = connection.cursor()
        cursor.execute("EXEC spObtenerPromociones")
        result = cursor.fetchall()
        return result
    except Exception as ex:
        print("Error durante la conexión: {}".format(ex))
        return []
    finally:
        if 'connection' in locals():
            connection.close()

def registrarPromocion(idProducto, tipo, descuento, fechaInicio, fechaFinal):
    try:
        connection = pyodbc.connect(f'DRIVER={{SQL Server}};SERVER={SERVER_NAME};DATABASE={DATABASE_NAME};UID={USER};PWD={PASSWORD}')
        cursor = connection.cursor()
        cursor.execute("EXEC spRegistrarPromocion @idProducto = ?, @tipo = ?, @descuento = ?, @fechaInicio = ?, @fechaFinal = ?", idProducto, tipo, descuento, fechaInicio, fechaFinal)
        connection.commit()
    except Exception as ex:
        print("Error durante la conexión: {}".format(ex))
    finally:
        if 'connection' in locals():
            connection.close()

def actualizarPromocion(id, idProducto, tipo, descuento, fechaInicio, fechaFinal):
    try:
        connection = pyodbc.connect(f'DRIVER={{SQL Server}};SERVER={SERVER_NAME};DATABASE={DATABASE_NAME};UID={USER};PWD={PASSWORD}')
        cursor = connection.cursor()
        cursor.execute("EXEC spActualizarPromocion @id = ?, @idProducto = ?, @tipo = ?, @descuento = ?, @fechaInicio = ?, @fechaFinal = ?", id, idProducto, tipo, descuento, fechaInicio, fechaFinal)
        connection.commit()
    except Exception as ex:
        print("Error durante la conexión: {}".format(ex))
    finally:
        if 'connection' in locals():
            connection.close()

def eliminarPromocion(id):
    try:
        connection = pyodbc.connect(f'DRIVER={{SQL Server}};SERVER={SERVER_NAME};DATABASE={DATABASE_NAME};UID={USER};PWD={PASSWORD}')
        cursor = connection.cursor()
        cursor.execute("EXEC spEliminarPromocion @id = ?", id)
        connection.commit()
    except Exception as ex:
        print("Error durante la conexión: {}".format(ex))
    finally:
        if 'connection' in locals():
            connection.close()

def getProductosCarrito(id):
    try:
        connection = pyodbc.connect(f'DRIVER={{SQL Server}};SERVER={SERVER_NAME};DATABASE={DATABASE_NAME};UID={USER};PWD={PASSWORD}')
        cursor = connection.cursor()
        cursor.execute("exec spObtenerCarritoPorUsuario @idUsuario = ?", id)
        rows = cursor.fetchall()
        lista=[]
        for row in rows:
                lista.append({
                    'fecha': row[0].strftime('%d/%m/%Y'),
                    'idProducto': row[1],  # Convertir Decimal a float
                    'cantidad': row[2],  # Convertir Decimal a float
                    'precio': row[4],  # Formatear fecha
                    'nombre': row[5],
                    'imagen': row[6],
                    'id': row[7],
                    'stock': row[8]
                })
        return lista
    except Exception as ex:
        print("Error durante la conexión: {}".format(ex))
    finally:
        connection.close()

def borrarDetalle(id):
    try:
        connection = pyodbc.connect(f'DRIVER={{SQL Server}};SERVER={SERVER_NAME};DATABASE={DATABASE_NAME};UID={USER};PWD={PASSWORD}')
        cursor = connection.cursor()
        cursor.execute("exec spBorrarDetalle @idDetalle = ?", id)
        connection.commit()
        if cursor.rowcount > 0:
            print("Producto eliminado exitosamente.")
            return True
        else:
            print("No se pudo eliminar el producto.")
            return False
    except Exception as ex:
        print("Error durante la conexión: {}".format(ex))
    finally:
        connection.close()

def actualizarCantidadDetalle(id,cantidad):
    try:
        connection = pyodbc.connect(f'DRIVER={{SQL Server}};SERVER={SERVER_NAME};DATABASE={DATABASE_NAME};UID={USER};PWD={PASSWORD}')
        cursor = connection.cursor()
        cursor.execute("exec actualizarCantidadDetalle @idDetalle = ?, @cantidad = ?", (id,cantidad))
        connection.commit()
        return True
    except Exception as ex:
        print("Error durante la conexión: {}".format(ex))
        return False
    finally:
        connection.close()

def agregarReseña(idProducto,idUsuario, calificacion, comentario):
    try:
        connection = pyodbc.connect(f'DRIVER={{SQL Server}};SERVER={SERVER_NAME};DATABASE={DATABASE_NAME};UID={USER};PWD={PASSWORD}')
        cursor = connection.cursor()
        cursor.execute("exec [dbo].[spAgregarReseña] @id_producto = ?, @id_usuario = ?, @calificacion= ?, @comentario= ?", (idProducto,idUsuario, calificacion, comentario))
        connection.commit()
        return True
    except Exception as ex:
        print("Error durante la conexión: {}".format(ex))
        return False
    finally:
        connection.close()



