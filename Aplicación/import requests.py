import requests
from io import BytesIO
from PIL import Image, ImageTk
import tkinter as tk

def obtener_id_google_drive(link):
    """Extrae el ID del archivo desde un enlace de Google Drive."""
    partes = link.split("/")
    if "drive.google.com" in partes:
        for parte in partes:
            if len(parte) == 33:  # El ID típico de Google Drive tiene 33 caracteres
                return parte
    return None

def descargar_imagen(drive_id):
    """Descarga la imagen desde Google Drive usando su ID."""
    url = f"https://drive.google.com/file/d/1QgR58fcLm2wbHSwOqqpwZBOE7YOxtGzB/view?usp=sharing={drive_id}"
    respuesta = requests.get(url)
    if respuesta.status_code == 200:
        return BytesIO(respuesta.content)
    else:
        raise Exception("No se pudo descargar la imagen.")

def mostrar_imagen(link_drive):
    """Muestra la imagen desde el enlace de Google Drive."""
    drive_id = obtener_id_google_drive(link_drive)
    if not drive_id:
        print("Enlace de Google Drive inválido.")
        return

    try:
        imagen_bytes = descargar_imagen(drive_id)
        imagen = Image.open(imagen_bytes)

        # Configuración de la ventana de Tkinter
        ventana = tk.Tk()
        ventana.title("Imagen desde Google Drive")
        
        # Convertir imagen a formato compatible con Tkinter
        imagen_tk = ImageTk.PhotoImage(imagen)
        etiqueta = tk.Label(ventana, image=imagen_tk)
        etiqueta.image = imagen_tk
        etiqueta.pack()

        ventana.mainloop()
    except Exception as e:
        print(f"Error: {e}")

# Enlace de la imagen
enlace_google_drive = "https://drive.google.com/file/d/1HAum5ufQXKg_xF6j1xKWdDfz9IgrHwf5/view?usp=drive_link"
mostrar_imagen(enlace_google_drive)