#artista_crear_biografia.py
import session
from obras import Obras

import json
import tkinter as tk
from tkinter import messagebox
import subprocess
import sys
import os

def guardar_obra():
    titulo = entry_titulo.get()
    descripcion = entry_descripcion.get()
    archivo_url = entry_archivo.get()
    miniatura_url = entry_miniatura.get()

    #convertir texto → lista → JSON
    tags_texto = entry_tags.get()
    tags_lista = [t.strip() for t in tags_texto.split(",") if t.strip()]  #limpia espacios

    tags_json = json.dumps(tags_lista)

    if not titulo or not descripcion or not archivo_url or not miniatura_url or not tags_texto:
        messagebox.showerror("Error", "Todos los campos son obligatorios")
        return
    
    Obras.crear_obra(session.usuario_id, titulo, descripcion, archivo_url, miniatura_url, tags_json)
    messagebox.showinfo("Éxito", "Obra subida exitosamente")
    ejecutar_archivo("artista_main_window.py")

def ejecutar_archivo(nombre_archivo):
    ruta = os.path.join(os.path.dirname(__file__), nombre_archivo)
    subprocess.Popen([sys.executable, ruta])
    root.destroy()


#window
root = tk.Tk()
root.title("Subir Obra")
root.geometry("400x300")

#widgets
label_titulo = tk.Label(root, text="Título de la Obra:")
label_titulo.pack(pady=5)
entry_titulo = tk.Entry(root, width=30)
entry_titulo.pack()

label_descripcion = tk.Label(root, text="Descripción de la Obra:")
label_descripcion.pack(pady=5)
entry_descripcion = tk.Entry(root, width=30)
entry_descripcion.pack()

label_archivo = tk.Label(root, text="Link de la Obra:")
label_archivo.pack(pady=5)
entry_archivo = tk.Entry(root, width=30)
entry_archivo.pack()

label_miniatura = tk.Label(root, text="Link de la Miniatura:")
label_miniatura.pack(pady=5)
entry_miniatura = tk.Entry(root, width=30)
entry_miniatura.pack()

label_tags = tk.Label(root, text="Tags (separados por comas):")
label_tags.pack(pady=5)
entry_tags = tk.Entry(root, width=30)
entry_tags.pack()

btn_guardar = tk.Button(root, text="Subir Obra", font=("Arial", 12), command=guardar_obra)
btn_guardar.pack(pady=20)

btn_regresar = tk.Button(root, text="Regresar", font=("Arial", 10), command=lambda: ejecutar_archivo("artista_main_window.py"))
btn_regresar.pack(pady=10)

root.mainloop()
