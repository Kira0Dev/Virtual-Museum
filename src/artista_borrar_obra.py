# artista_borrar_obra.py
import session
from obras import Obras

import tkinter as tk
from tkinter import messagebox


def abrir_ventana_borrar_obra(parent=None):

    ventana = tk.Toplevel(parent)
    ventana.title("Borrar Obra")
    ventana.geometry("400x300")
    ventana.focus()

    #widgets
    label_info = tk.Label(ventana, text="Aquí puedes borrar una obra")
    label_info.pack(pady=20)

    label_obra_nombre = tk.Label(ventana, text="Nombre de la obra a borrar:")
    label_obra_nombre.pack(pady=5)
    entry_obra_nombre = tk.Entry(ventana, width=30)
    entry_obra_nombre.pack()

    label_borrar = tk.Label(ventana, text="Escribe 'BORRAR' para confirmar:")
    label_borrar.pack(pady=5)
    entry_borrar = tk.Entry(ventana, width=30)
    entry_borrar.pack()

    #función borrar
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
            messagebox.showinfo(
                "Éxito",
                f"La obra '{nombre_obra}' ha sido borrada exitosamente"
            )
            ventana.destroy()
        else:
            messagebox.showerror(
                "Error",
                "No se pudo eliminar la obra. Verifica los datos."
            )

    btn_borrar = tk.Button(
        ventana,
        text="Borrar Obra",
        font=("Arial", 10),
        command=borrar_obra
    )
    btn_borrar.pack(pady=20)

    btn_cancelar = tk.Button(
        ventana,
        text="Cancelar",
        font=("Arial", 10),
        command=ventana.destroy
    )
    btn_cancelar.pack(pady=10)
