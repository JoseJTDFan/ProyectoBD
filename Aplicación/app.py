from flask import Flask, render_template, request

app = Flask(__name__)

# Ruta para la página principal
@app.route('/')
def home():
    return render_template('index.html')

# Ruta para procesar datos del formulario (opcional)
@app.route('/accion1', methods=['POST'])
def accion1():
    dato = request.form.get('dato')
    return f"Acción 1 ejecutada con: {dato}"

# Ruta para manejar acción 2
@app.route('/accion2', methods=['POST'])
def accion2():
    otro_dato = request.form.get('otro_dato')
    return f"Acción 2 ejecutada con: {otro_dato}"


if __name__ == '__main__':
    app.run(debug=True)