#artista_borrar_obra.py
import session
from obras import Obras

import tkinter as tk
from tkinter import messagebox
import subprocess
import sys
import os

def borrar_obra():
    nombre_obra = entry_obra_nombre.get().strip()
    confirmacion = entry_borrar.get().strip()

    if not nombre_obra or not confirmacion:
        messagebox.showerror("Error", "Todos los campos son obligatorios")
        return

    if confirmacion != "BORRAR":
        messagebox.showerror("Error", "Debes escribir 'BORRAR' para confirmar")
        return

    artista_id = session.usuario_id
    if Obras.eliminar_obra_por_titulo(nombre_obra, artista_id):
        messagebox.showinfo("Éxito", f"La obra '{nombre_obra}' ha sido borrada exitosamente")
        ejecutar_archivo("artista_main_window.py")
    else:
        messagebox.showerror("Error", f"No se pudo eliminar, verifica los campos")

def ejecutar_archivo(nombre_archivo):
    ruta = os.path.join(os.path.dirname(__file__), nombre_archivo)
    subprocess.Popen([sys.executable, ruta])
    root.destroy()


#ventana
root = tk.Tk()
root.title("Borrar Obra")
root.geometry("400x300")

#widgets
label_info = tk.Label(root, text="Aquí puedes borrar una obra")
label_info.pack(pady=20)

label_obra_nombre = tk.Label(root, text="Nombre de la obra a borrar:")
label_obra_nombre.pack(pady=5)
entry_obra_nombre = tk.Entry(root, width=30)
entry_obra_nombre.pack()

label_borrar = tk.Label(root, text="Escribe 'BORRAR' para confirmar:")
label_borrar.pack(pady=5)
entry_borrar = tk.Entry(root, width=30)
entry_borrar.pack()

btn_borrar = tk.Button(root, text="Borrar Obra", font=("Arial", 10), command=borrar_obra)
btn_borrar.pack(pady=20)

btn_cancelar = tk.Button(root, text="Cancelar", font=("Arial", 10), command=lambda: ejecutar_archivo("artista_main_window.py"))
btn_cancelar.pack(pady=10)

