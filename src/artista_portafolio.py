#artista_crear_biografia.py
from usuario import Usuario, hash_password
import session
from usuario import Visitante
from usuario import Artista
from usuario import Moderador
from obras import Obras
from reportes import Reportes
from salas import Salas
from comentarios import Comentarios

import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
import subprocess
import sys
import os

def mostrar_portafolio():
    #crear objeto del artista usando su ID en sesión
    artista = Artista(session.usuario_id)

    try:
        obras = artista.ver_portafolio()
    except Exception as e:
        messagebox.showerror("Error", f"No se pudo obtener el portafolio:\n{e}")
        return

    listbox.delete(0, tk.END)

    #mostrar todas las obras
    if not obras:
        listbox.insert(tk.END, "No tienes obras registradas")
        return

    for obra in obras:
        obra_id, titulo, descripcion = obra
        listbox.insert(tk.END, f"{obra_id} - {titulo} | {descripcion}")

def ejecutar_archivo(nombre_archivo):
    ruta = os.path.join(os.path.dirname(__file__), nombre_archivo)
    subprocess.Popen([sys.executable, ruta])
    root.destroy()

#ventana
root = tk.Tk()
root.title("Mi Portafolio")
root.geometry("500x300")

btn_cargar = tk.Button(root, text="Cargar Portafolio", command=mostrar_portafolio)
btn_cargar.pack(pady=10)

listbox = tk.Listbox(root, width=60, height=15)
listbox.pack()

btn_regresar = tk.Button(root, text="Regresar", font=("Arial", 10), command=lambda: ejecutar_archivo("artista_main_window.py"))
btn_regresar.pack(pady=10)

root.mainloop()
