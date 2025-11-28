#artista_biografia.py
import session
from usuario import Artista

import tkinter as tk
from tkinter import messagebox
import subprocess
import sys
import os

def ejecutar_archivo(nombre_archivo):
    ruta = os.path.join(os.path.dirname(__file__), nombre_archivo)
    subprocess.Popen([sys.executable, ruta])
    root.destroy()

def guardar_biografia():
    nueva_biografia = text_biografia.get("1.0", tk.END).strip()
    if Artista.cambiar_biografia(session.usuario_id, nueva_biografia):
        messagebox.showinfo("Éxito", "Biografía actualizada correctamente")
    else:
        messagebox.showerror("Error", "No se pudo actualizar la biografía")

artista_biografia = Artista.obtener_biografia(session.usuario_id)

#ventana
root = tk.Tk()
root.title("Actualizar Biografía")
root.geometry("400x300")

#widgets
label_biografia = tk.Label(root, text="Esta es tu Biografía:")
label_biografia.pack(pady=10)

text_biografia = tk.Text(root, width=40, height=10)
text_biografia.pack()

text_biografia.insert(tk.END, artista_biografia)

btn_actualizar_biografia = tk.Button(root, text="Guardar Biografía", font=("Arial", 12), command=guardar_biografia)
btn_actualizar_biografia.pack(pady=10)

