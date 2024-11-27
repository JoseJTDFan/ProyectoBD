from flask import Flask, render_template, request, session, redirect, url_for,jsonify
from Conexión import *

app = Flask(__name__, static_folder='Productos')
app.secret_key = "1234"

# Ruta para la página principal
@app.route('/')
def home():
    session.clear()
    categorias = getTop5Categorias()
    promociones = getPromocionesInicio()
    return render_template('index.html', 
                           categorias=categorias,
                           promociones=promociones)

# Ruta para procesar datos del formulario (opcional)
@app.route('/inicio', methods=['GET', 'POST'])
def inicio():
    if request.method == 'POST':
        correo = request.form.get('correo')
        contrasena = request.form.get('contraseña')
        usuario = validarUsuario(correo, contrasena)
        print(usuario)
        if usuario:
            pagina = 1
            session["id"] = usuario[0]
            session["nombre"] = usuario[1]
            session["apellido"] = usuario[2]
            session["correo"] = usuario[3]
            session["contrasena"] = usuario[4]
            session["telefono"] = usuario[5]
            session["fecha"] = usuario[6]
            session["tipo"] = usuario[7]
            session["estado"] = usuario[8]
            session["direccion"] = usuario[9]
            crearCarrito(usuario[0])
        else:
            categorias = getTop5Categorias()
            promociones = getPromocionesInicio()
            return render_template(
                'index.html',
                mensaje="Usuario no registrado o credenciales incorrectas.",
                categorias=categorias,
                promociones=promociones
            )
    else:
        # Obtener la página desde el parámetro GET si es una solicitud de cambio de página
        pagina = request.args.get('pagina', 1, type=int)
        # Simular un usuario autenticado (o manejar sesión para persistencia)
        usuario = []
        usuario.append(session["id"])
        usuario.append(session["nombre"])
        usuario.append(session["apellido"])
        usuario.append(session["correo"])
        usuario.append(session["contrasena"])
        usuario.append(session["telefono"])
        usuario.append(session["fecha"])
        usuario.append(session["tipo"])
        usuario.append(session["estado"])
        usuario.append(session["direccion"])

    # Obtener datos necesarios para renderizar la página
    categorias = getNombresCategorias()
    marcas = getNombresMarcas()
    productos = getProductos(pagina)

    # Calcular paginación
    total_productos = getTotalProductos()  # Una función que obtiene el número total de productos
    elementos_por_pagina = 10
    hay_siguiente = (pagina * elementos_por_pagina) < total_productos
    hay_anterior = pagina > 1

    if session["tipo"] == 'admin':
        return render_template(
            'admin.html',
            usuario=usuario)
    else:
        return render_template(
            'productos.html',
            usuario=usuario,
            categorias=categorias,
            marcas=marcas,
            productos=productos,
            pagina_actual=pagina,
            hay_siguiente=hay_siguiente,
            hay_anterior=hay_anterior
        )
@app.route('/registrarse')
def registro():
    return render_template('registro.html')

@app.route('/cliente/<int:id>')
def cliente(id):
    cliente=[]
    cliente.append(session["id"])
    cliente.append(session["nombre"])
    cliente.append(session["apellido"])
    cliente.append(session["correo"])
    cliente.append(session["contrasena"])
    cliente.append(session["telefono"])
    cliente.append(session["fecha"])
    cliente.append(session["tipo"])
    cliente.append(session["estado"])
    cliente.append(session["direccion"])
    print(cliente)
    if (session["tipo"] == "cliente"):
        return render_template('cliente.html', cliente=cliente, opcion=1)
    else:
        return render_template('cliente.html', cliente=cliente, opcion=2)

# Ruta para los detalles de un producto
@app.route('/producto_detalle/<int:producto_id>')
def producto_detalle(producto_id):
    producto = getProductoDetalle(producto_id)
    reseñas = getReseñasPorProducto(producto_id)
    prodSimilares = getProductosSimilares(producto["Categoria"], producto["id"])
    return render_template('producto_detalle.html',
                            producto=producto,
                            reseñas=reseñas,
                            prodSimilares= prodSimilares)

@app.route('/carrito/<int:id>')
def carrito(id):
    cliente=[]
    cliente.append(session["id"])
    cliente.append(session["nombre"])
    cliente.append(session["apellido"])
    cliente.append(session["correo"])
    cliente.append(session["contrasena"])
    cliente.append(session["telefono"])
    cliente.append(session["fecha"])
    cliente.append(session["tipo"])
    cliente.append(session["direccion"])
    productos = getProductosCarrito(id)
    precioTotal= 0
    for producto in productos:
        precioTotal += producto['precio'] * producto['cantidad']
    return render_template('carrito.html', cliente=cliente,
                           productos= productos,
                           precioTotal= precioTotal)
# Ruta para la página de reportes
@app.route('/reportes')
def reportes():
    usuario = {
        "id": session.get("id"),
        "nombre": session.get("nombre"),
        "apellido": session.get("apellido"),
        "correo": session.get("correo"),
        "telefono": session.get("telefono"),
        "fecha": session.get("fecha"),
        "tipo": session.get("tipo")
    }
    return render_template('reportes.html', usuario=usuario)

@app.route('/actualizar_usuario', methods=['POST'])
def actualizar_usuario():
    # Catch form data
    id_cliente = request.form.get('id_cliente')
    nonbre = request.form.get('nombre')
    apellido = request.form.get('apellido')
    correo = request.form.get('correo')
    contra = request.form.get('contra')
    telefono = request.form.get('telefono')
    tipo = request.form.get('tipo')
    direccion = request.form.get('direccion')
    estado = request.form.get('estado')
    estado_value = 1 if estado == "True" else 0


    # Perform the necessary actions with the data
    # For example, update the database or perform validations
    print(f"Cliente ID: {id_cliente}")
    print(f"Nombre: {nonbre}")
    print(f"Apellido: {apellido}")
    print(f"Correo: {correo}")
    print(f"Contraseña: {contra}")
    print(f"Teléfono: {telefono}")
    print(f"Tipo: {tipo}")
    print(f"Estado: {estado_value}")
    print(f"Dirección: {direccion}")

    update = actualizarUsuario(
        id_cliente, nonbre, apellido, correo, contra, telefono, tipo, estado_value, direccion
    )

    usuario = validarUsuario(correo, contra)
    if usuario:
        pagina = 1
        session["id"] = usuario[0]
        session["nombre"] = usuario[1]
        session["apellido"] = usuario[2]
        session["correo"] = usuario[3]
        session["contrasena"] = usuario[4]
        session["telefono"] = usuario[5]
        session["fecha"] = usuario[6]
        session["tipo"] = usuario[7]
        session["estado"] = usuario[8]
        session["direccion"] = usuario[9]
    else:
        categorias = getTop5Categorias()
        promociones = getPromocionesInicio()
        return render_template(
            'index.html',
            mensaje="Usuario no registrado o credenciales incorrectas.",
            categorias=categorias,
            promociones=promociones
        )
    return redirect(url_for('cliente', id=id_cliente))

@app.route('/exito', methods=['POST'])
def exito():
    nombre = request.form.get('nombre')
    apellido = request.form.get('apellido')
    correo = request.form.get('correo')
    contrasena = request.form.get('contraseña')
    telefono = request.form.get('telefono')
    tipo = request.form.get('tipo')
    if request.form.get('tipo') == "1":
        tipo = 'cliente'
    else:
        tipo = 'admin'
    direccion = request.form.get('direccion')

    if crearUsuario(nombre, apellido, correo, contrasena, telefono, tipo, direccion) == True:
        if session.get("tipo") is None  or session["tipo"] == "cliente":
            return render_template(
                        'index.html',
                        mensaje2="Usuario registrado exitosamente",
                        categorias=getTop5Categorias(),
                        promociones=getPromocionesInicio()
                    )
        else:
             return redirect(url_for('usuarios'))
    else:
        return render_template('registro.html',
                               mensaje="Usuario no registrado")
    
@app.route('/filtrado', methods=['GET'])
def filtro():
    # Obtener los valores de los filtros desde los argumentos de la URL
    precio_min = request.args.get('precio_min') 
    precio_max = request.args.get('precio_max')
    categoria = request.args.get('categoria')   
    marca = request.args.get('marca')        
    calif_min = request.args.get('calif_min') 
    calif_max = request.args.get('calif_max') 

    precio_min = int(precio_min) if precio_min else None
    precio_max = int(precio_max) if precio_max else None
    calif_min = int(calif_min) if calif_min else None
    calif_max = int(calif_max) if calif_max else None
    categoria = int(categoria) if categoria else None
    marca = int(marca) if marca else None  

    productos = getProductosFiltrados(precio_min, precio_max, categoria, marca, calif_min, calif_max)
    usuario = []
    usuario.append(session["id"])
    usuario.append(session["nombre"])
    usuario.append(session["apellido"])
    usuario.append(session["correo"])
    usuario.append(session["contrasena"])
    usuario.append(session["telefono"])
    usuario.append(session["fecha"])
    usuario.append(session["tipo"])
    usuario.append(session["estado"])
    usuario.append(session["direccion"])
    return render_template('filtros.html',
                               productos=productos,
                               usuario=usuario)

@app.route('/filtrobusqueda', methods=['POST', 'GET'])
def filtrobusqueda():
    # Obtener los valores de los filtros desde los argumentos de la URL
    busqueda = request.form.get('query')
    productos = getProductosFiltradosporQuery(busqueda)
    print(busqueda)
    usuario = []
    usuario.append(session["id"])
    usuario.append(session["nombre"])
    usuario.append(session["apellido"])
    usuario.append(session["correo"])
    usuario.append(session["contrasena"])
    usuario.append(session["telefono"])
    usuario.append(session["fecha"])
    usuario.append(session["tipo"])
    usuario.append(session["estado"])
    usuario.append(session["direccion"])
    return render_template('filtros.html',
                               productos=productos,
                               usuario=usuario)

@app.route('/usuarios')
def usuarios():
    usuarios = getUsuarios()
    return render_template('usuarios.html',
                           usuarios=usuarios) 

@app.route('/subir_reseña/<int:idProducto>', methods=['POST','GET'])
def subirReseña(idProducto):
    reseña = request.args.get('reseña')
    calificacion = request.args.get('calificacion')
    agregarReseña(idProducto,session["id"], calificacion, reseña)
    return redirect(url_for('producto_detalle', producto_id=idProducto))

@app.route('/añadir_carrito/<int:id>', methods=['POST'])
def agregarCarrito(id):
    carrito = obtenerCarrito(session["id"])
    cantidad = int(request.form.get('cantidad'))
    if añadirProducto(id, carrito[0], cantidad):
        return redirect(url_for('producto_detalle', producto_id=id))
    else:
        return "Error al añadir el producto al carrito", 400

@app.route('/actualizar_cantidad', methods=['POST'])
def actualizarCantidad():
    idDetalle = int(request.form.get('id'))
    cantidad = int(request.form.get('cantidad'))
    actualizarCantidadDetalle(idDetalle,cantidad)
    return redirect(url_for('carrito', id = session["id"]))

@app.route('/eliminar/<int:detalleid>')
def eliminarCarrito(detalleid):
    borrarDetalle(detalleid)
    return redirect(url_for('carrito', id = session["id"]))
    

@app.route('/logout')
def logout():
    session.clear()  # Limpia la sesión
    return redirect(url_for('home'))  # Redirige a la función 'home'

# Ruta para la página de marcas
@app.route('/brand')
def brands():
    marcas = getMarcas()
    return render_template('marcas.html', marcas=marcas)

# Ruta para registrar una nueva marca
@app.route('/registrarMarca', methods=['GET', 'POST'])
def registrar_marca():
    if request.method == 'POST':
        nombre = request.form.get('nombre')
        descripcion = request.form.get('descripcion')
        registrarMarca(nombre, descripcion)
        return redirect(url_for('brands'))
    return render_template('registrarMarca.html')


@app.route('/editarMarca', methods=['GET'])
def editar_marca():
    idMarca = request.args.get('id')
    nombre = request.args.get('nombre')
    descripcion = request.args.get('descripcion')
    if idMarca and nombre and descripcion:
        actualizarMarca(idMarca, nombre, descripcion)
        return redirect(url_for('brands'))
    return render_template('editarMarca.html')

# Ruta para eliminar una marca
@app.route('/eliminarMarca', methods=['GET'])
def eliminar_marca():
    idMarca = request.args.get('id')
    if idMarca:
        eliminarMarca(idMarca)
        return redirect(url_for('brands'))
    return render_template('eliminarMarca.html')



# Ruta para la página de categorías
@app.route('/category')
def category():
    categorias = getCategorias()
    return render_template('categorias.html', categorias=categorias)

# Ruta para registrar una nueva categoría
@app.route('/registrarCategoria', methods=['GET', 'POST'])
def registrar_categoria():
    if request.method == 'POST':
        nombre = request.form.get('nombre')
        descripcion = request.form.get('descripcion')
        registrarCategoria(nombre, descripcion)
        return redirect(url_for('category'))
    return render_template('registrarCategoria.html')


@app.route('/editarCategoria', methods=['GET', 'POST'])
def editar_categoria():
    if request.method == 'POST':
        idCategoria = request.form.get('id')
        nombre = request.form.get('nombre')
        descripcion = request.form.get('descripcion')
        actualizarCategoria(idCategoria, nombre, descripcion)
        return redirect(url_for('category'))
    else:
        idCategoria = request.args.get('id')
        nombre = request.args.get('nombre')
        descripcion = request.args.get('descripcion')
        if idCategoria and nombre and descripcion:
            return render_template('editarCategoria.html', id=idCategoria, nombre=nombre, descripcion=descripcion)
        return redirect(url_for('category'))

# Ruta para eliminar una categoría
@app.route('/eliminarCategoria', methods=['GET'])
def eliminar_categoria():
    idCategoria = request.args.get('id')
    if idCategoria:
        eliminarCategoria(idCategoria)
        return redirect(url_for('category'))
    return render_template('eliminarCategoria.html')


@app.route('/editarUsuario', methods=['GET', 'POST'])
def editar_usuario():
    if request.method == 'POST':
        idUsuario = request.form.get('id')
        nombre = request.form.get('nombre')
        apellido = request.form.get('apellido')
        correo = request.form.get('correo')
        telefono = request.form.get('telefono')
        direccion = request.form.get('direccion')
        if idUsuario and nombre and apellido and correo and telefono and direccion:
            modificarUsuario(idUsuario, nombre, apellido, correo, telefono, direccion)
            return redirect(url_for('usuarios'))
    else:
        idUsuario = request.args.get('id')
        nombre = request.args.get('nombre')
        apellido = request.args.get('apellido')
        correo = request.args.get('correo')
        telefono = request.args.get('telefono')
        direccion = request.args.get('direccion')
        if idUsuario and nombre and apellido and correo and telefono and direccion:
            return render_template('editarUsuario.html', id=idUsuario, nombre=nombre, apellido=apellido, correo=correo, telefono=telefono, direccion=direccion)
    return redirect(url_for('usuarios'))

# Ruta para eliminar un usuario
@app.route('/eliminarUsuario', methods=['GET'])
def eliminar_usuario():
    idUsuario = request.args.get('id')
    if idUsuario:
        eliminarUsuario(idUsuario)
        return redirect(url_for('usuarios'))
    return render_template('eliminarUsuario.html')




    # Ruta para la página de productos
@app.route('/product')
def productos():
    productos = getProductoss()
    return render_template('productosAdmin.html', productos=productos)




# Ruta para registrar un nuevo producto
@app.route('/registrarProducto', methods=['GET', 'POST'])
def registrar_producto():
    if request.method == 'POST':
        codigo_producto = request.form.get('codigo_producto')
        nombre = request.form.get('nombre')
        descripcion = request.form.get('descripcion')
        precio = request.form.get('precio')
        stock = request.form.get('stock')
        idCategoria = request.form.get('idCategoria')
        idMarca = request.form.get('idMarca')
        registrarProducto(codigo_producto, nombre, descripcion, precio, stock, idCategoria, idMarca)
        return redirect(url_for('productos'))
    categorias = getCategorias()
    marcas = getMarcas()
    return render_template('registrarProducto.html', categorias=categorias, marcas=marcas)
    
# Ruta para editar un producto
@app.route('/editarProducto', methods=['GET', 'POST'])
def editar_producto():
    if request.method == 'POST':
        idProducto = request.form.get('id')
        nombre = request.form.get('nombre')
        descripcion = request.form.get('descripcion')
        precio = request.form.get('precio')
        stock = request.form.get('stock')
        idCategoria = request.form.get('idCategoria')
        idMarca = request.form.get('idMarca')
        actualizarProducto(idProducto, nombre, descripcion, precio, stock, idCategoria, idMarca)
        return redirect(url_for('productos'))
    else:
        idProducto = request.args.get('id')
        nombre = request.args.get('nombre')
        descripcion = request.args.get('descripcion')
        precio = request.args.get('precio')
        stock = request.args.get('stock')
        idCategoria = request.args.get('idCategoria')
        idMarca = request.args.get('idMarca')
        categorias = getCategorias()
        marcas = getMarcas()
        if idProducto and nombre and descripcion and precio and stock and idCategoria and idMarca:
            return render_template('editarProducto.html', id=idProducto, nombre=nombre, descripcion=descripcion, precio=precio, stock=stock, idCategoria=idCategoria, idMarca=idMarca, categorias=categorias, marcas=marcas)
    return redirect(url_for('productos'))

# Ruta para eliminar un producto
@app.route('/eliminarProducto', methods=['GET'])
def eliminar_producto():
    idProducto = request.args.get('id')
    if idProducto:
        eliminarProducto(idProducto)
        return redirect(url_for('productos'))
    return render_template('eliminarProducto.html')




# Ruta para la página de promociones y ofertas
@app.route('/promociones')
def promociones():
    promociones = getPromociones()
    return render_template('promociones.html', promociones=promociones)

# Ruta para registrar una nueva promoción u oferta
@app.route('/registrarPromocion', methods=['GET', 'POST'])
def registrar_promocion():
    if request.method == 'POST':
        idProducto = request.form.get('idProducto')
        tipo = request.form.get('tipo')
        descuento = request.form.get('descuento')
        fechaInicio = request.form.get('fechaInicio')
        fechaFinal = request.form.get('fechaFinal')
        registrarPromocion(idProducto, tipo, descuento, fechaInicio, fechaFinal)
        return redirect(url_for('promociones'))
    productos = getProductoss()
    return render_template('registrarPromocion.html', productos=productos)

# Ruta para editar una promoción u oferta
@app.route('/editarPromocion', methods=['GET', 'POST'])
def editar_promocion():
    if request.method == 'POST':
        idPromocion = request.form.get('id')
        idProducto = request.form.get('idProducto')
        tipo = request.form.get('tipo')
        descuento = request.form.get('descuento')
        fechaInicio = request.form.get('fechaInicio')
        fechaFinal = request.form.get('fechaFinal')
        actualizarPromocion(idPromocion, idProducto, tipo, descuento, fechaInicio, fechaFinal)
        return redirect(url_for('promociones'))
    else:
        idPromocion = request.args.get('id')
        idProducto = request.args.get('idProducto')
        tipo = request.args.get('tipo')
        descuento = request.args.get('descuento')
        fechaInicio = request.args.get('fechaInicio')
        fechaFinal = request.args.get('fechaFinal')
        if idPromocion and idProducto and tipo and descuento and fechaInicio and fechaFinal:
            return render_template('editarPromocion.html', id=idPromocion, idProducto=idProducto, tipo=tipo, descuento=descuento, fechaInicio=fechaInicio, fechaFinal=fechaFinal)
    return redirect(url_for('promociones'))

# Ruta para eliminar una promoción u oferta
@app.route('/eliminarPromocion', methods=['GET'])
def eliminar_promocion():
    idPromocion = request.args.get('id')
    if idPromocion:
        eliminarPromocion(idPromocion)
        return redirect(url_for('promociones'))
    return render_template('eliminarPromocion.html')


@app.route('/getproductos')
def get_productos():
    return jsonify(getProductoseID())

if __name__ == '__main__':
    app.run(debug=True)