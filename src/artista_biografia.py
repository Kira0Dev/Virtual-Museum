# artista_biografia.py
import session
from usuario import Artista

import tkinter as tk
from tkinter import messagebox

def abrir_ventana_biografia(parent=None):
    ventana = tk.Toplevel(parent)
    ventana.title("Actualizar Biografía")
    ventana.geometry("400x300")
    ventana.focus() 

    artista_biografia = Artista.obtener_biografia(session.usuario_id)

    #widgets
    label_biografia = tk.Label(ventana, text="Esta es tu Biografía:")
    label_biografia.pack(pady=10)

    text_biografia = tk.Text(ventana, width=40, height=10)
    text_biografia.pack()
    text_biografia.insert(tk.END, artista_biografia)

    #función interna para guardar
    def guardar_biografia():
        nueva_biografia = text_biografia.get("1.0", tk.END).strip()
        if Artista.cambiar_biografia(session.usuario_id, nueva_biografia):
            messagebox.showinfo("Éxito", "Biografía actualizada correctamente")
            ventana.destroy()
        else:
            messagebox.showerror("Error", "No se pudo actualizar la biografía")

    btn_actualizar = tk.Button(
        ventana,
        text="Guardar Biografía",
        font=("Arial", 12),
        command=guardar_biografia
    )
    btn_actualizar.pack(pady=10)

    btn_regresar = tk.Button(
        ventana,
        text="Regresar",
        font=("Arial", 12),
        command=ventana.destroy
    )

    btn_regresar.pack(pady=10)
