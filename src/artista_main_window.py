# artista_main_window.py
import session

import tkinter as tk
from tkinter import messagebox


def abrir_ventana_artista():
    ventana = tk.Toplevel()
    ventana.title("Ventana Principal - Artista")
    ventana.geometry("600x400")

    label_bienvenida = tk.Label(ventana, text=f"Bienvenido, {session.usuario_nombre}!", font=("Arial", 16))
    label_bienvenida.pack(pady=20)

    def abrir_biografia():
        import artista_biografia
        artista_biografia.abrir_ventana_biografia()

    def abrir_portafolio():
        import artista_portafolio
        artista_portafolio.abrir_ventana_portafolio()

    def abrir_subir_obra():
        import artista_subir_obra
        artista_subir_obra.abrir_ventana_subir_obra()

    def abrir_borrar_obra():
        import artista_borrar_obra
        artista_borrar_obra.abrir_ventana_borrar_obra()

    btn_actualizar_biografia = tk.Button(
        ventana,
        text="Actualizar Biografía",
        font=("Arial", 12),
        command=abrir_biografia
    )
    btn_actualizar_biografia.pack(pady=10)

    btn_ver_portafolio = tk.Button(
        ventana,
        text="Ver Portafolio",
        font=("Arial", 12),
        command=abrir_portafolio
    )
    btn_ver_portafolio.pack(pady=10)

    btn_subir_obra = tk.Button(
        ventana,
        text="Crear Nueva Obra",
        font=("Arial", 12),
        command=abrir_subir_obra
    )
    btn_subir_obra.pack(pady=10)

    btn_borrar_obra = tk.Button(
        ventana,
        text="Borrar Obra",
        font=("Arial", 12),
        command=abrir_borrar_obra
    )
    btn_borrar_obra.pack(pady=10)




