from flask import Flask, render_template, request
from Conexión import *

app = Flask(__name__, static_folder='Productos')

# Ruta para la página principal
@app.route('/')
def home():
    categorias = getTop5Categorias()
    promociones = getPromocionesInicio()
    return render_template('index.html', 
                           categorias=categorias,
                           promociones=promociones)

# Ruta para procesar datos del formulario (opcional)
@app.route('/inicio', methods=['POST'])
def inicio():
    correo = request.form.get('correo')
    contrasena= request.form.get('contraseña')
    usuario =validarUsuario(correo,contrasena)
    if  usuario != False:
        categorias = getNombresCategorias()
        marcas = getNombresMarcas()
        productos= getProductos(3)
        return render_template('productos.html',
                               usuario = usuario,
                               categorias=categorias,
                               marcas=marcas,
                               productos=productos)
    else:
        categorias = getTop5Categorias()
        promociones = getPromocionesInicio()
        return render_template('index.html',
                                mensaje="Usuario no registrado o credenciales incorrectas.",
                                categorias=categorias,
                                promociones=promociones)

# Ruta para manejar acción 2
#@app.route('/accion2', methods=['POST'])
#def accion2():
#    otro_dato = request.form.get('otro_dato')
#    return f"Acción 2 ejecutada con: {otro_dato}"


if __name__ == '__main__':
    app.run(debug=True)