# artista_crear_biografia.py
import tkinter as tk
from tkinter import messagebox
from usuario import Artista
import session

def abrir_ventana_biografia():
    ventana = tk.Toplevel()
    ventana.title("Crear Biografía de Artista")
    ventana.geometry("400x300")

    label_biografia = tk.Label(ventana, text="Por favor, escribe tu Biografía:")
    label_biografia.pack(pady=10)

    text_biografia = tk.Text(ventana, width=40, height=10)
    text_biografia.pack()

    def crear_biografia():
        biografia = text_biografia.get("1.0", tk.END).strip()

        if not biografia:
            messagebox.showerror("Error", "La biografía no puede estar vacía")
            return

        Artista.agregar_biografia(session.usuario_id, biografia)

        messagebox.showinfo("Éxito", "Biografía guardada exitosamente")
        ventana.destroy()  # Cerramos esta ventana
        import artista_main_window
        artista_main_window.abrir_ventana_artista()

    btn_guardar = tk.Button(ventana, text="Guardar Biografía", command=crear_biografia)
    btn_guardar.pack(pady=10)
