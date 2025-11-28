# artista_subir_obra
import session
from obras import Obras

import json
import tkinter as tk
from tkinter import messagebox


def abrir_ventana_subir_obra(parent=None):

    ventana = tk.Toplevel(parent)
    ventana.title("Subir Obra")
    ventana.geometry("400x420")
    ventana.focus()

    #widgets
    label_titulo = tk.Label(ventana, text="Título de la Obra:")
    label_titulo.pack(pady=5)
    entry_titulo = tk.Entry(ventana, width=30)
    entry_titulo.pack()

    label_descripcion = tk.Label(ventana, text="Descripción de la Obra:")
    label_descripcion.pack(pady=5)
    entry_descripcion = tk.Entry(ventana, width=30)
    entry_descripcion.pack()

    label_archivo = tk.Label(ventana, text="Link de la Obra:")
    label_archivo.pack(pady=5)
    entry_archivo = tk.Entry(ventana, width=30)
    entry_archivo.pack()

    label_miniatura = tk.Label(ventana, text="Link de la Miniatura:")
    label_miniatura.pack(pady=5)
    entry_miniatura = tk.Entry(ventana, width=30)
    entry_miniatura.pack()

    label_tags = tk.Label(ventana, text="Tags (separados por comas):")
    label_tags.pack(pady=5)
    entry_tags = tk.Entry(ventana, width=30)
    entry_tags.pack()

    def guardar_obra():
        titulo = entry_titulo.get().strip()
        descripcion = entry_descripcion.get().strip()
        archivo_url = entry_archivo.get().strip()
        miniatura_url = entry_miniatura.get().strip()
        tags_texto = entry_tags.get().strip()

        if not titulo or not descripcion or not archivo_url or not miniatura_url or not tags_texto:
            messagebox.showerror("Error", "Todos los campos son obligatorios")
            return

        tags_lista = [t.strip() for t in tags_texto.split(",") if t.strip()]
        #tags_json = json.dumps(tags_lista)

        Obras.crear_obra(
            titulo,
            descripcion,
            session.usuario_id,
            archivo_url,
            miniatura_url,
            tags_lista
        )

        messagebox.showinfo("Éxito", "Obra subida exitosamente")
        ventana.destroy()

    btn_guardar = tk.Button(
        ventana,
        text="Subir Obra",
        font=("Arial", 12),
        command=guardar_obra
    )
    btn_guardar.pack(pady=20)


    btn_cerrar = tk.Button(
        ventana,
        text="Cerrar",
        font=("Arial", 10),
        command=ventana.destroy
    )
    btn_cerrar.pack(pady=10)
