from flask import Flask, render_template, request, session
from Conexión import *

app = Flask(__name__, static_folder='Productos')
app.secret_key = "1234"

# Ruta para la página principal
@app.route('/')
def home():
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
            session["direccion"] = usuario[8]
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
    cliente.append(session["direccion"])
    return render_template('cliente.html', cliente=cliente)

# Ruta para los detalles de un producto
@app.route('/producto_detalle/<int:producto_id>')
def producto_detalle(producto_id):
    producto = getProductoDetalle(producto_id)
    return render_template('producto_detalle.html', producto=producto)

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
    return render_template('carrito.html', cliente=cliente)

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
        return render_template(
                    'index.html',
                    mensaje2="Usuario registrado exitosamente",
                    categorias=getTop5Categorias(),
                    promociones=getPromocionesInicio()
                )
    else:
        return render_template('registro.html',
                               mensaje="Usuario no registrado")



if __name__ == '__main__':
    app.run(debug=True)