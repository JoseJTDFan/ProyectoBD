#Elaborado por: José Julián Brenes Garro 
#               Cristhian Daniel Rivas Zuñiga	
#               Gabriel Jesus Gutiérrez Mata	
#               Natalia Sofia Rodriguez Solano	
#Fecha de creación: 14/11/2024
#Versión 3.12.1

import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk  # Necesario para cargar imágenes en tkinter

# Crear ventana principal
root = tk.Tk()
root.title("Interfaz de Imágenes y Login")
root.geometry("800x400")

# Cargar la imagen de fondo
fondo_img = Image.open("fondo.png")
fondo_img = fondo_img.resize((800, 400), Image.Resampling.LANCZOS)
fondo_photo = ImageTk.PhotoImage(fondo_img)

# Crear un Label para la imagen de fondo
fondo_label = tk.Label(root, image=fondo_photo)
fondo_label.place(x=0, y=0, relwidth=1, relheight=1)


# Frame para las imágenes y etiquetas
image_frame = tk.Frame(root, bg='#FEF9D9')
image_frame.grid(row=0, column=0, padx=10, pady=10)

# Cargar imágenes de ejemplo
# Reemplaza "ruta_imagenX.jpg" con la ruta de tus imágenes
image_paths = ["Productos/cuidado personal/Espuma de afeitar.png", "Acetaminofen.png", "Aerosol.png", "Aretes.png"]
images = []

# Crear espacio para las imágenes y etiquetas
for i in range(4):
    # Cargar y redimensionar la imagen
    img = Image.open(image_paths[i])
    img = img.resize((100, 100), Image.Resampling.LANCZOS)
    img = ImageTk.PhotoImage(img)
    images.append(img)

    # Crear Label para mostrar la imagen
    img_label = tk.Label(image_frame, image=images[i], bg='#FEF9D9')
    img_label.grid(row=0, column=i, padx=10, pady=5)

    # Crear etiquetas debajo de cada imagen
    label1 = tk.Label(image_frame, text=f"Imagen {i + 1}", bg='#FEF9D9')
    label1.grid(row=1, column=i)
    label2 = tk.Label(image_frame, text=f"Descripción {i + 1}", bg='#FEF9D9')
    label2.grid(row=2, column=i)

# Frame para el formulario de login
login_frame = tk.Frame(root, bg='#FEF9D9')
login_frame.grid(row=0, column=1, padx=20, pady=10, sticky="n")

# Etiquetas y entradas para el correo y la contraseña
email_label = tk.Label(login_frame, text="Correo:", bg='#FEF9D9')
email_label.grid(row=0, column=0, pady=5, sticky="w")
email_entry = tk.Entry(login_frame, width=25)
email_entry.grid(row=0, column=1, pady=5)

password_label = tk.Label(login_frame, text="Contraseña:", bg='#FEF9D9')
password_label.grid(row=1, column=0, pady=5, sticky="w")
password_entry = tk.Entry(login_frame, show="*", width=25)
password_entry.grid(row=1, column=1, pady=5)

# Botón de login
login_button = tk.Button(login_frame, text="Iniciar Sesión")
login_button.grid(row=2, column=0, columnspan=2, pady=10)

# Ejecutar la aplicación
root.mainloop()